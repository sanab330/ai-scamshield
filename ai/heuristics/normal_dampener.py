"""
Normal Message Dampener for AI ScamShield.
Reduces false-positive risk scores for routine transactional, OTP, delivery, and conversational messages.
"""

import re

LEGITIMATE_PATTERNS = [
    # E-Commerce & Delivery status
    {
        "id": "LEGIT_DELIVERY_UPDATE",
        "pattern": r"(?i)\b(order|package|shipment)\b.*\b(dispatched|delivered|arrived|out for delivery|doorstep|arriving in \d+ mins)\b",
        "dampening_factor": 0.85
    },
    # Cab & Ride Hail
    {
        "id": "LEGIT_RIDE_SHARE",
        "pattern": r"(?i)\b(driver|cab|ride|uber|ola)\b.*\b(arriving in \d+|swift dzire|pin is \d+|otp \d+ to start)\b",
        "dampening_factor": 0.90
    },
    # Standard Authentic 2FA / OTP (without asking user to forward it or pay)
    {
        "id": "LEGIT_STANDARD_OTP",
        "pattern": r"(?i)\b\d{4,8}\b.*\b(secret otp|verification code|one time password)\b.*\b(do not share|valid for \d+ mins?)\b",
        "dampening_factor": 0.80
    },
    # Bank Debit Alert (standard format: debited by ... Avl Bal ... Report unauthorized: 1800...)
    {
        "id": "LEGIT_BANK_DEBIT",
        "pattern": r"(?i)\b(a/c|account)\b.*\b(debited|credited|avl bal|available balance)\b.*\b(1800\d+|report fraud)\b",
        "dampening_factor": 0.85
    },
    # Everyday friendly conversation
    {
        "id": "LEGIT_CASUAL_CHAT",
        "pattern": r"(?i)\b(hey|hello|hi|good morning|happy birthday|congratulations on|lunch|coffee|dinner|call me back|reach home|traffic|pick up)\b",
        "dampening_factor": 0.70
    },
    # Railway & Flight travel tickets
    {
        "id": "LEGIT_TRAVEL_TICKET",
        "pattern": r"(?i)\b(pnr|irctc|flight|boarding|coach|berth|seat)\b.*\b(confirmed|departs?|gate \d+)\b",
        "dampening_factor": 0.90
    }
]

def check_legitimate_indicators(text: str):
    """
    Checks for presence of authentic, routine message patterns.
    Returns matched legitimate rules and combined dampening power.
    """
    # Check if text contains high-risk words first
    has_high_risk_words = bool(re.search(r"(?i)\b(blocked|suspended|disconnect|kyc|apk|lottery|winner|cbi|arrest|urgent|immediately)\b", text))
    has_external_link = bool(re.search(r"(?i)https?://(?!www\.amazon\.|www\.flipkart\.|v\.whatsapp\.com)\S+", text))
    
    # If high risk or unverified link is present, dampener is disabled for safety
    if has_high_risk_words or has_external_link:
        return {
            "is_legitimate_candidate": False,
            "dampening_factor": 0.0,
            "matched_legit_patterns": []
        }

    matched = []
    max_dampening = 0.0

    for rule in LEGITIMATE_PATTERNS:
        if re.search(rule["pattern"], text):
            matched.append(rule["id"])
            if rule["dampening_factor"] > max_dampening:
                max_dampening = rule["dampening_factor"]

    return {
        "is_legitimate_candidate": len(matched) > 0,
        "dampening_factor": max_dampening,
        "matched_legit_patterns": matched
    }
