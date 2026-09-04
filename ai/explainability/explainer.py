"""
Explainable AI (XAI) Attribution Engine for AI ScamShield.
Calculates percentage attributions for detected risk factors and generates
human-readable explanations of why an interaction was flagged.
"""

from typing import List, Dict, Any

FACTOR_DESCRIPTIONS = {
    "Urgency / Psychological Manipulation": "Uses artificial deadlines or panic to force rapid, unverified decisions.",
    "Credential Harvesting": "Attempts to solicit passwords, OTPs, PINs, or sensitive identity numbers.",
    "Bank / Organization Impersonation": "Mimics legitimate financial institutions, government portals, or tech services.",
    "Suspicious URL / Phishing Domain": "Contains unverified web links, suspicious top-level domains, or look-alike spelling.",
    "Threat / Intimidation Tactics": "Uses legal threats, police action, or immediate utility disconnections to induce fear.",
    "Unrealistic Financial Lure": "Offers large sums, lottery jackpots, or easy task earnings that are too good to be true.",
    "Unverified Software / APK Download": "Directs the user to download an external APK file that can compromise mobile security.",
    "Delivery / Courier Redelivery Fee": "Demands small micro-payments to release packages, a classic credit card harvesting trick.",
    "Statistical & Linguistic Anomaly": "Unusual punctuation patterns, high capitalization density, and irregular syntax."
}

def generate_explanation(
    risk_score: int,
    matched_rules: List[Dict[str, Any]],
    ml_probability: float,
    has_suspicious_url: bool = False,
    is_dampened: bool = False
) -> Dict[str, Any]:
    """
    Generates a proportional feature attribution breakdown that sums to 100%,
    paired with simple human-readable explanations.
    """
    if risk_score <= 25:
        return {
            "status_headline": "Low Observed Risk",
            "summary": "This interaction displays standard communication patterns without recognized scam indicators.",
            "attributions": [
                {
                    "factor": "Routine Communication Patterns",
                    "percentage": 85,
                    "description": "Standard vocabulary, natural grammar, and absence of deceptive solicitations."
                },
                {
                    "factor": "Absence of High-Risk Indicators",
                    "percentage": 15,
                    "description": "No requests for OTPs, passwords, or immediate payments detected."
                }
            ],
            "key_drivers": ["Normal wording", "No suspicious links", "No credential requests"]
        }

    # High / Moderate / Critical Risk Attribution
    factor_weights = {}

    # Accumulate weights from matched rules
    for r in matched_rules:
        category = r.get("category", "Other Signals")
        factor_name = map_category_to_display(category)
        weight = r.get("weight", 30)
        factor_weights[factor_name] = factor_weights.get(factor_name, 0) + weight

    # If ML model confidence is high, attribute statistical linguistic anomaly
    if ml_probability > 0.70:
        factor_weights["Statistical & Linguistic Anomaly"] = factor_weights.get("Statistical & Linguistic Anomaly", 0) + 25

    if has_suspicious_url:
        factor_weights["Suspicious URL / Phishing Domain"] = factor_weights.get("Suspicious URL / Phishing Domain", 0) + 35

    # If somehow empty but risk score is elevated
    if not factor_weights:
        factor_weights["Suspicious Content Patterns"] = 50
        factor_weights["Linguistic Pressure"] = 50

    total_weight = sum(factor_weights.values())

    attributions = []
    accumulated_pct = 0
    items = sorted(factor_weights.items(), key=lambda x: x[1], reverse=True)

    for i, (factor, weight) in enumerate(items):
        if i == len(items) - 1:
            # Ensure exact 100% sum
            pct = max(1, 100 - accumulated_pct)
        else:
            pct = int(round((weight / total_weight) * 100))
            accumulated_pct += pct

        attributions.append({
            "factor": factor,
            "percentage": pct,
            "description": FACTOR_DESCRIPTIONS.get(factor, "Observed characteristic associated with common scam vectors.")
        })

    headline = (
        "Critical Threat Patterns Detected" if risk_score >= 76 else
        "High Risk Indicators Identified" if risk_score >= 51 else
        "Caution Advised — Potential Risk"
    )

    drivers = [a["factor"] for a in attributions[:3]]

    return {
        "status_headline": headline,
        "summary": f"This message scored {risk_score}/100 primarily driven by {drivers[0] if drivers else 'threat indicators'}.",
        "attributions": attributions,
        "key_drivers": drivers
    }

def map_category_to_display(category: str) -> str:
    mapping = {
        "Credential Harvesting": "Credential Harvesting",
        "Bank Impersonation": "Bank / Organization Impersonation",
        "Utility Scam": "Threat / Intimidation Tactics",
        "Lottery / Prize Scam": "Unrealistic Financial Lure",
        "Employment Fraud": "Unrealistic Financial Lure",
        "Delivery Phishing": "Delivery / Courier Redelivery Fee",
        "Malicious Software": "Unverified Software / APK Download",
        "Social Engineering": "Urgency / Psychological Manipulation",
        "Authority Impersonation": "Threat / Intimidation Tactics",
        "Phishing Infrastructure": "Suspicious URL / Phishing Domain"
    }
    return mapping.get(category, "Suspicious Content Patterns")
