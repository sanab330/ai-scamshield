"""
Curated Scam Signatures & Deterministic Rules Database for AI ScamShield.
High-precision regex patterns mapped to threat categories and severity scores.
"""

import re

# Threat rules with regex pattern, category, base weight (0-100), and explanation
SCAM_RULES = [
    {
        "id": "RULE_OTP_PIN_SOLICIT",
        "category": "Credential Harvesting",
        "pattern": r"(?i)\b(share|enter|send|verify|provide)\b.*\b(otp|one.?time.?password|upi.?pin|atm.?pin|cvv|password)\b",
        "weight": 85,
        "signal": "Direct Request for OTP / PIN / Credentials",
        "recommendation": "Never share OTP, UPI PIN, or banking passwords with anyone under any circumstance."
    },
    {
        "id": "RULE_KYC_ACCOUNT_SUSPENSION",
        "category": "Bank Impersonation",
        "pattern": r"(?i)\b(kyc|aadhaar|pan)\b.*\b(block\w*|suspend\w*|deactivat\w*|expir\w*|restrict\w*|freeze|terminat\w*)\b",
        "weight": 80,
        "signal": "Threat of Account / KYC Suspension",
        "recommendation": "Banks never ask you to update KYC via third-party SMS links. Visit your official branch or mobile banking app."
    },
    {
        "id": "RULE_ELECTRICITY_DISCONNECTION",
        "category": "Utility Scam",
        "pattern": r"(?i)\b(electricity|power|power.?supply|gas.?connection|meter)\b.*\b(disconnect\w*|cut.?off|suspend\w*|blackout)\b.*\b(tonight|immediately|bill|officer)\b",
        "weight": 85,
        "signal": "Immediate Power Disconnection Threat",
        "recommendation": "Government electricity boards do not send disconnection threats from personal numbers. Check your bill on the official state discom portal."
    },
    {
        "id": "RULE_LOTTERY_PRIZE_LURE",
        "category": "Lottery / Prize Scam",
        "pattern": r"(?i)\b(won|winner|lucky.?draw|congratulations|prize|kbc|diwali.?mega.?win)\b.*\b(lakh|crore|car|iphone|cash|£|\$|₹)\b",
        "weight": 75,
        "signal": "Unrealistic Lottery / Prize Win Notification",
        "recommendation": "Legitimate lotteries do not select random phone numbers for multi-lakh prizes. Never pay 'claim fees'."
    },
    {
        "id": "RULE_PART_TIME_JOB_TELEGRAM",
        "category": "Employment Fraud",
        "pattern": r"(?i)\b(part.?time|work.?from.?home|daily.?income|daily.?payout)\b.*\b(like.?youtube|rate.?hotels|telegram|whatsapp|task)\b",
        "weight": 75,
        "signal": "Task-Based Part-Time Job / Telegram Scam",
        "recommendation": "Prepaid review tasks and Telegram earnings schemes are common investment traps. Never deposit money to unlock tasks."
    },
    {
        "id": "RULE_PARCEL_REDELIVERY_FEE",
        "category": "Delivery Phishing",
        "pattern": r"(?i)\b(parcel|package|shipment|fedex|indiapost|bluedart|dhl)\b.*\b(on.?hold|failed|reschedule|redelivery|address|customs)\b.*\b(pay|fee|charge|rs|₹)\b",
        "weight": 70,
        "signal": "Fake Delivery Fee / Missing Address Phishing",
        "recommendation": "Couriers do not require micro-payments via SMS links to update addresses. Track solely on official courier websites."
    },
    {
        "id": "RULE_APK_DOWNLOAD_LINK",
        "category": "Malicious Software",
        "pattern": r"(?i)https?://\S+\.apk\b|\bdownload.*\.apk\b",
        "weight": 90,
        "signal": "Direct Unverified APK Application Download",
        "recommendation": "Never install unknown APKs from SMS or chat. They often contain remote banking trojans."
    },
    {
        "id": "RULE_URGENCY_MANIPULATION",
        "category": "Social Engineering",
        "pattern": r"(?i)\b(immediately|urgent|within\s+(15|30|60|\d+)\s+(mins|minutes|hours)|today\s+only|last\s+chance|expire\s+tonight)\b",
        "weight": 40,
        "signal": "Psychological Urgency & Pressure",
        "recommendation": "Scammers create artificial urgency to prevent you from thinking clearly or consulting others."
    },
    {
        "id": "RULE_POLICE_CYBER_THREAT",
        "category": "Authority Impersonation",
        "pattern": r"(?i)\b(cbi|cyber.?crime|police|arrest.?warrant|court|legal.?action|tax.?evasion|trai)\b.*\b(arrest|fine|penalty|prosecution|warrant)\b",
        "weight": 85,
        "signal": "Law Enforcement / Cyber Police Intimidation Threat",
        "recommendation": "Police, CBI, and RBI never demand immediate money transfer or conduct arrests via WhatsApp / SMS."
    },
    {
        "id": "RULE_SUSPICIOUS_TLD",
        "category": "Phishing Infrastructure",
        "pattern": r"(?i)https?://[a-zA-Z0-9.-]+\.(xyz|top|click|site|cc|pw|me|info|online|icu|buzz|club|app)\b",
        "weight": 50,
        "signal": "High-Risk Top-Level Domain Commonly Exploited in Phishing",
        "recommendation": "Be cautious when clicking obscure domain extensions (.xyz, .top, .click) impersonating reputable organizations."
    }
]

def evaluate_heuristics(text: str):
    """
    Evaluates text against curated deterministic rules.
    Returns matched rules, highest rule weight, and composite heuristic score.
    """
    matched = []
    total_weight = 0
    
    for rule in SCAM_RULES:
        if re.search(rule["pattern"], text):
            matched.append({
                "id": rule["id"],
                "category": rule["category"],
                "weight": rule["weight"],
                "signal": rule["signal"],
                "recommendation": rule["recommendation"]
            })
            total_weight += rule["weight"]

    # Diminishing return aggregation: 1 - product(1 - w_i / 100)
    if not matched:
        return {"matched_rules": [], "composite_heuristic_score": 0, "top_recommendation": None}

    prob_complement = 1.0
    for m in matched:
        prob_complement *= (1.0 - (m["weight"] / 100.0))
    
    heuristic_score = int(round((1.0 - prob_complement) * 100))
    # Pick recommendation of the highest weighted matched rule
    matched.sort(key=lambda x: x["weight"], reverse=True)
    top_recommendation = matched[0]["recommendation"]

    return {
        "matched_rules": matched,
        "composite_heuristic_score": min(heuristic_score, 100),
        "top_recommendation": top_recommendation
    }
