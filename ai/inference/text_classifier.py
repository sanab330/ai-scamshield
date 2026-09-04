"""
Unified AI Text & SMS Scam Classifier for AI ScamShield.
Integrates ML model, deterministic heuristics, normal message dampener,
and the explainability engine. Runs completely offline.
"""

import os
import re
import joblib
from typing import Dict, Any

from ai.heuristics.rules_database import evaluate_heuristics
from ai.heuristics.normal_dampener import check_legitimate_indicators
from ai.explainability.explainer import generate_explanation

# Global singleton model cache
_MODEL = None
_VECTORIZER = None

def load_models():
    global _MODEL, _VECTORIZER
    if _MODEL is None or _VECTORIZER is None:
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "scam_classifier.joblib")
        vec_path = os.path.join(os.path.dirname(__file__), "..", "models", "tfidf_vectorizer.joblib")
        
        if os.path.exists(model_path) and os.path.exists(vec_path):
            _MODEL = joblib.load(model_path)
            _VECTORIZER = joblib.load(vec_path)
        else:
            raise FileNotFoundError("Model artifacts not found. Please train models first.")
    return _MODEL, _VECTORIZER

def mask_pii(text: str) -> str:
    """
    Masks sensitive personal information (phone numbers, account numbers, emails).
    Protects user privacy in storage and logging.
    """
    # Mask Indian phone numbers (10 digits starting with 6-9)
    text = re.sub(r"\b([6-9]\d{2})\d{4}(\d{3})\b", r"\1****\2", text)
    # Mask international / standard phone numbers
    text = re.sub(r"(\+\d{1,3}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", r"***-***-****", text)
    # Mask email addresses
    text = re.sub(r"\b([A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b", r"\1***@\2", text)
    # Mask 16-digit card numbers
    text = re.sub(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?(\d{4})\b", r"****-****-****-\1", text)
    return text

def analyze_message(text: str) -> Dict[str, Any]:
    """
    Performs full offline analysis on an incoming or submitted text message.
    Returns unified risk score, risk level, confidence, explainability breakdown,
    detected signals, and recommendations.
    """
    if not text or not text.strip():
        return {
            "risk_score": 0,
            "risk_level": "LOW",
            "confidence": 1.0,
            "status": "SAFE / LOW OBSERVED RISK",
            "detected_signals": [],
            "explanation": generate_explanation(0, [], 0.0),
            "recommendation": "No text provided for analysis.",
            "is_offline": True,
            "masked_preview": ""
        }

    clean_text = text.strip()
    masked_preview = mask_pii(clean_text[:120])

    # 1. Load ML models and get prediction probability
    try:
        model, vectorizer = load_models()
        X_vec = vectorizer.transform([clean_text])
        if hasattr(model, "predict_proba"):
            ml_prob = float(model.predict_proba(X_vec)[0, 1])
        elif hasattr(model, "decision_function"):
            raw_decision = float(model.decision_function(X_vec)[0])
            # Sigmoid calibration
            import math
            ml_prob = 1.0 / (1.0 + math.exp(-raw_decision))
        else:
            ml_prob = float(model.predict(X_vec)[0])
    except Exception as e:
        # Fallback to pure rule-based evaluation if model file is unavailable
        ml_prob = 0.5

    # 2. Evaluate Deterministic Heuristic Rules
    heuristic_res = evaluate_heuristics(clean_text)
    matched_rules = heuristic_res["matched_rules"]
    heuristic_score = heuristic_res["composite_heuristic_score"]

    # 3. Check for Suspicious Links
    has_suspicious_url = bool(re.search(r"(?i)https?://[a-zA-Z0-9.-]+\.(xyz|top|click|site|cc|pw|me|info|online|icu)\b", clean_text))

    # 4. Check Normal Message Dampener
    legit_check = check_legitimate_indicators(clean_text)

    # 5. Signal Fusion & Risk Scoring
    base_ml_score = ml_prob * 100.0

    if matched_rules:
        highest_rule_weight = max(r["weight"] for r in matched_rules)
        # Blend ML probability with heuristic score
        raw_combined = (base_ml_score * 0.40) + (heuristic_score * 0.60)
        final_score = max(raw_combined, float(highest_rule_weight))
    else:
        final_score = base_ml_score * 0.75  # Without explicit rules, cap uncorroborated ML score

    # 6. Apply Normal Message Dampener if applicable
    if legit_check["is_legitimate_candidate"] and not matched_rules:
        dampening = legit_check["dampening_factor"]
        final_score = final_score * (1.0 - dampening)
        # Ensure routine legitimate messages never exceed LOW RISK boundary
        final_score = min(final_score, 18.0)

    # Bound score between 0 and 100
    final_score = int(round(max(0.0, min(100.0, final_score))))

    # 7. Map to Risk Levels (0-25: LOW, 26-50: MODERATE, 51-75: HIGH, 76-100: CRITICAL)
    if final_score <= 25:
        risk_level = "LOW"
        status_label = "SAFE / LOW OBSERVED RISK"
        default_rec = "Normal interaction. No typical scam or phishing patterns observed."
    elif final_score <= 50:
        risk_level = "MODERATE"
        status_label = "CAUTION ADVISED"
        default_rec = "Verify the identity of the sender independently before clicking any links or responding."
    elif final_score <= 75:
        risk_level = "HIGH"
        status_label = "HIGH RISK"
        default_rec = "Do not click links, download files, or send funds. Independently contact the organization."
    else:
        risk_level = "CRITICAL"
        status_label = "CRITICAL RISK"
        default_rec = "Immediate scam risk detected! Do not share OTPs, PINs, or make any payment. Block the sender."

    recommendation = heuristic_res["top_recommendation"] or default_rec

    # 8. Detected Signals Summary List
    detected_signals = [r["signal"] for r in matched_rules]
    if has_suspicious_url and "High-Risk Top-Level Domain" not in str(detected_signals):
        detected_signals.append("Suspicious Domain Structure")
    if ml_prob > 0.85 and "Statistical Linguistic Anomaly" not in detected_signals:
        detected_signals.append("High Statistical Linguistic Anomaly")

    # 9. Compute Confidence Score (0.80 to 0.99)
    if matched_rules:
        confidence = round(0.85 + (len(matched_rules) * 0.03), 2)
    elif legit_check["is_legitimate_candidate"]:
        confidence = 0.92
    else:
        confidence = round(0.80 + abs(ml_prob - 0.5) * 0.3, 2)
    confidence = min(confidence, 0.99)

    # 10. Generate Explainability Attribution
    explanation = generate_explanation(
        risk_score=final_score,
        matched_rules=matched_rules,
        ml_probability=ml_prob,
        has_suspicious_url=has_suspicious_url,
        is_dampened=legit_check["is_legitimate_candidate"]
    )

    return {
        "risk_score": final_score,
        "risk_level": risk_level,
        "status": status_label,
        "confidence": confidence,
        "detected_signals": detected_signals,
        "explanation": explanation,
        "recommendation": recommendation,
        "is_offline": True,
        "masked_preview": masked_preview
    }
