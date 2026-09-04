"""
Social Media Profile & Impersonation Risk Analyzer for AI ScamShield.
Analyzes publicly visible profile metadata, bio language, and account indicators.
Respects platform privacy and follows strictly probabilistic safety language.
"""

import re
from typing import Dict, Any, List

IMPERSONATION_USERNAMES = [
    "official", "support", "helpdesk", "care", "admin", "service", "verified",
    "security", "desk", "refund", "assist", "manager"
]

BIO_FRAUD_KEYWORDS = [
    r"(?i)\b(earn|guaranteed|profit|crypto|forex|invest|binary|returns|daily payout|dm to double)\b",
    r"(?i)\b(whatsapp|telegram|t\.me/|wa\.me/|dm for work)\b",
    r"(?i)\b(100%|risk.?free|no loss|recover lost money|hack)\b"
]

def analyze_profile(
    username: str,
    bio: str = "",
    account_age_days: int = 365,
    followers_count: int = 100,
    following_count: int = 100,
    has_external_link: bool = False
) -> Dict[str, Any]:
    """
    Evaluates risk signals from publicly available profile metadata.
    Does NOT claim certainty; reports probabilistic risk indicators.
    """
    base_risk = 10
    signals = []
    factor_weights = {}

    clean_user = (username or "").strip().lower()
    clean_bio = (bio or "").strip()

    # 1. Check Username Patterns
    # High trailing digit count (e.g. user_849204128)
    if re.search(r"\d{5,}$", clean_user):
        base_risk += 15
        signals.append("Randomized Trailing Digits Pattern in Username")
        factor_weights["Username Randomness"] = 15

    # Check for faux authority words in username
    for keyword in IMPERSONATION_USERNAMES:
        if keyword in clean_user:
            base_risk += 25
            signals.append(f"Authority / Helpdesk Term in Username ('{keyword}')")
            factor_weights["Impersonation Nomenclature"] = factor_weights.get("Impersonation Nomenclature", 0) + 25
            break

    # 2. Check Account Age
    if account_age_days < 14:
        base_risk += 35
        signals.append(f"Very Recently Created Account ({account_age_days} days old)")
        factor_weights["Account Age Novelty"] = 35
    elif account_age_days < 60:
        base_risk += 15
        signals.append(f"Relatively New Account ({account_age_days} days old)")
        factor_weights["Account Age Novelty"] = 15

    # 3. Check Follower Ratio Anomaly (e.g. follows 2,500, followed by 12)
    if following_count > 200 and followers_count < 25:
        base_risk += 20
        signals.append("Skewed Following-to-Follower Ratio (Mass-Following Behavior)")
        factor_weights["Social Graph Anomaly"] = 20

    # 4. Check Bio Content
    matched_bio_flags = []
    for pattern in BIO_FRAUD_KEYWORDS:
        if re.search(pattern, clean_bio):
            matched_bio_flags.append(pattern)

    if matched_bio_flags:
        weight = min(40, len(matched_bio_flags) * 20)
        base_risk += weight
        signals.append("Bio Contains High-Risk Financial, Crypto, or Telegram Recruitment Lures")
        factor_weights["Bio Content Lures"] = weight

    # 5. External Link to Unverified Service
    if has_external_link or re.search(r"(?i)https?://|t\.me/|wa\.me/", clean_bio):
        base_risk += 15
        signals.append("Direct Off-Platform Contact Redirect (Telegram / WhatsApp / Link)")
        factor_weights["Off-Platform Redirection"] = 15

    final_score = int(round(min(100, max(5, base_risk))))

    # Calibrated Probabilistic Language
    if final_score <= 25:
        risk_level = "LOW"
        status = "LOW OBSERVED PROFILE RISK"
        recommendation = "Standard public profile indicators. Standard online caution applies."
    elif final_score <= 50:
        risk_level = "MODERATE"
        status = "CAUTION ADVISED"
        recommendation = "Minor profile anomalies observed. Exercise discretion before initiating private messaging."
    elif final_score <= 75:
        risk_level = "HIGH"
        status = "POTENTIALLY SUSPICIOUS PROFILE"
        recommendation = "This profile shows several potential impersonation or scam indicators. Do not send funds or engage in financial deals."
    else:
        risk_level = "CRITICAL"
        status = "CRITICAL IMPERSONATION RISK"
        recommendation = "High density of known fraud indicators. Do not communicate, share sensitive information, or transfer money."

    # Attribution Breakdown
    attributions = []
    total_w = sum(factor_weights.values()) or 1
    accum = 0
    items = sorted(factor_weights.items(), key=lambda x: x[1], reverse=True)
    for i, (k, v) in enumerate(items):
        if i == len(items) - 1:
            pct = max(1, 100 - accum)
        else:
            pct = int(round((v / total_w) * 100))
            accum += pct
        attributions.append({
            "factor": k,
            "percentage": pct,
            "description": f"Contributes {pct}% to the profile risk evaluation."
        })

    if not attributions:
        attributions = [
            {"factor": "Established Account History", "percentage": 75, "description": "Long-standing account with regular activity patterns."},
            {"factor": "Standard Profile Text", "percentage": 25, "description": "Absence of deceptive financial or impersonation keywords."}
        ]

    return {
        "username": username,
        "risk_score": final_score,
        "risk_level": risk_level,
        "status": status,
        "signals": signals,
        "attributions": attributions,
        "recommendation": recommendation,
        "is_offline": True,
        "disclaimer": "AI ScamShield provides risk assessment based on visible characteristics, not absolute identity verification."
    }
