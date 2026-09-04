"""
Payment Risk Manager & 'Stop Before You Pay' Pre-Flight Safety Scorer for AI ScamShield.
Evaluates transaction parameters, behavioral anomalies, and interactive checklist responses.
Never requests or stores banking PINs, OTPs, or credentials.
"""

from typing import Dict, Any, List, Optional

def calculate_payment_risk(
    amount: float,
    is_new_recipient: bool,
    recipient_history_count: int = 0,
    transaction_hour: int = 14,
    has_urgency_pressure: bool = False,
    is_device_changed: bool = False,
    checklist_answers: Optional[Dict[str, bool]] = None
) -> Dict[str, Any]:
    """
    Computes unified payment transaction risk based on parameter anomalies
    and optional 7-point pre-payment checklist answers.
    """
    risk_score = 10
    signals = []
    factor_weights = {}

    # 1. Recipient Novelty
    if is_new_recipient or recipient_history_count == 0:
        risk_score += 25
        signals.append("Brand-New Recipient (Zero Previous Transaction History)")
        factor_weights["Recipient Novelty"] = 25
    elif recipient_history_count < 3:
        risk_score += 10
        signals.append("Infrequent Recipient (Less than 3 prior transactions)")
        factor_weights["Recipient Novelty"] = 10

    # 2. Transaction Amount Anomaly
    if amount >= 100000:
        risk_score += 35
        signals.append(f"High-Value Outflow (₹{amount:,.2f})")
        factor_weights["High Transaction Amount"] = 35
    elif amount >= 25000:
        risk_score += 20
        signals.append(f"Elevated Transaction Value (₹{amount:,.2f})")
        factor_weights["High Transaction Amount"] = 20
    elif amount >= 10000:
        risk_score += 10
        signals.append(f"Moderate Outflow (₹{amount:,.2f})")
        factor_weights["High Transaction Amount"] = 10

    # 3. Unusual Transaction Time (e.g. 1:00 AM to 5:00 AM)
    if 1 <= transaction_hour <= 5:
        risk_score += 20
        signals.append(f"Anomalous Time-of-Day ({transaction_hour:02d}:00 HRS - High Impulsivity Risk)")
        factor_weights["Temporal Anomaly"] = 20

    # 4. Psychological Urgency Pressure
    if has_urgency_pressure:
        risk_score += 25
        signals.append("External Urgency / Deadline Pressure Reported")
        factor_weights["Psychological Urgency"] = 25

    # 5. Device Change Anomaly
    if is_device_changed:
        risk_score += 15
        signals.append("Unrecognized Device / Environment Flag")
        factor_weights["Device Security"] = 15

    # 6. Interactive 7-Point "Stop Before You Pay" Checklist
    checklist_risk = 0
    if checklist_answers:
        # Q1: Personally know recipient? (False is risky)
        if not checklist_answers.get("know_recipient", True):
            checklist_risk += 15
            signals.append("Recipient Not Known Personally to User")
            factor_weights["Unknown Counterparty"] = 15

        # Q2: User initiated payment? (False is risky)
        if not checklist_answers.get("user_initiated", True):
            checklist_risk += 20
            signals.append("Payment Requested by External Counterparty")
            factor_weights["Unsolicited Request"] = 20

        # Q3: Asked to act urgently? (True is risky)
        if checklist_answers.get("act_urgently", False):
            checklist_risk += 15
            signals.append("Pressure to Complete Transaction Immediately")
            factor_weights["Urgency Coercion"] = 15

        # Q4: Asked to share OTP/PIN? (True is CRITICAL RED FLAG)
        if checklist_answers.get("share_otp_pin", False):
            checklist_risk += 45
            signals.append("CRITICAL: Requester Demanded OTP, PIN, or Verification Secret")
            factor_weights["Credential Compromise"] = 45

        # Q5: Contacted unexpectedly? (True is risky)
        if checklist_answers.get("unexpected_contact", False):
            checklist_risk += 15
            signals.append("Unexpected / Cold Initiation via Call or Chat")
            factor_weights["Cold Contact"] = 15

        # Q6: Received suspicious link? (True is risky)
        if checklist_answers.get("suspicious_link", False):
            checklist_risk += 25
            signals.append("Payment Directed Through Unverified Link")
            factor_weights["Unverified Payment Channel"] = 25

        # Q7: Promised unrealistic reward or return? (True is risky)
        if checklist_answers.get("unrealistic_reward", False):
            checklist_risk += 30
            signals.append("Transaction Linked to Guaranteed Returns or Lottery Prize")
            factor_weights["Financial Lure"] = 30

    # Combine Base Parameters with Checklist
    total_raw_risk = risk_score + checklist_risk
    final_score = int(round(min(100, max(5, total_raw_risk))))

    # Map to Risk Level
    if final_score <= 25:
        risk_level = "LOW"
        status = "LOW TRANSACTION RISK"
        recommendation = "Standard transaction parameters. Proceed with normal mindfulness."
    elif final_score <= 50:
        risk_level = "MODERATE"
        status = "CAUTION ADVISED"
        recommendation = "Double-check the account name and amount before entering your secure UPI PIN."
    elif final_score <= 75:
        risk_level = "HIGH"
        status = "HIGH PAYMENT RISK"
        recommendation = "Pause and independently contact the recipient via a known voice call before transferring funds."
    else:
        risk_level = "CRITICAL"
        status = "CRITICAL PAYMENT RISK"
        recommendation = "STOP BEFORE YOU PAY! High probability of financial fraud. Do NOT share OTP or proceed."

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
            "description": f"Contributes {pct}% to the overall payment risk score."
        })

    if not attributions:
        attributions = [
            {"factor": "Known Recipient Baseline", "percentage": 85, "description": "Established counterparty with regular transaction history."},
            {"factor": "Standard Amount & Timing", "percentage": 15, "description": "Transaction falls within routine behavioral limits."}
        ]

    return {
        "amount": amount,
        "is_new_recipient": is_new_recipient,
        "transaction_hour": transaction_hour,
        "risk_score": final_score,
        "risk_level": risk_level,
        "status": status,
        "signals": signals,
        "attributions": attributions,
        "recommendation": recommendation,
        "is_offline": True
    }
