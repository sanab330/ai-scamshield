"""
Unit Tests for AI ScamShield Risk Engine & Text Classifier.
Verifies scam detection, false-positive suppression, and explainability breakdown.
"""

import pytest
from ai.inference.text_classifier import analyze_message

def test_kyc_scam_detection():
    msg = "Dear SBI user, your net banking is blocked today. Click http://sbi-kyc-update.xyz immediately or account will be frozen."
    res = analyze_message(msg)
    
    assert res["risk_score"] >= 75
    assert res["risk_level"] in ["HIGH", "CRITICAL"]
    assert any("KYC" in s or "Suspension" in s or "Domain" in s for s in res["detected_signals"])
    assert res["explanation"]["attributions"] is not None
    # Verify attribution percentages sum to 100
    total_pct = sum(a["percentage"] for a in res["explanation"]["attributions"])
    assert total_pct == 100

def test_power_utility_scam():
    msg = "Dear consumer, electricity power will be disconnected tonight at 9:30 PM due to unpaid bill. Call electricity officer 9876543210 immediately."
    res = analyze_message(msg)
    
    assert res["risk_score"] >= 75
    assert res["risk_level"] in ["HIGH", "CRITICAL"]
    assert "Immediate Power Disconnection Threat" in res["detected_signals"]

def test_otp_credential_solicitation():
    msg = "Paytm Support: Your refund of Rs 4,999 failed. Kindly share the 6-digit OTP received on your mobile to credit the amount."
    res = analyze_message(msg)
    
    assert res["risk_score"] >= 75
    assert "Direct Request for OTP / PIN / Credentials" in res["detected_signals"]

def test_normal_delivery_message_not_flagged():
    msg = "Your Amazon order #402-9182301 has been dispatched with delivery partner ATS. Track your package on your Amazon mobile app."
    res = analyze_message(msg)
    
    assert res["risk_score"] <= 25
    assert res["risk_level"] == "LOW"
    assert res["explanation"]["status_headline"] == "Low Observed Risk"

def test_normal_friend_chat_not_flagged():
    msg = "Hey, are we still catching up for coffee today at 4 PM near the library?"
    res = analyze_message(msg)
    
    assert res["risk_score"] <= 25
    assert res["risk_level"] == "LOW"

def test_normal_bank_debit_alert_not_flagged():
    msg = "Your SBI Account XX4829 is debited by INR 650.00 on 04-Sep-26 at Grocery Store. Avl Bal: INR 18,420.00. Report fraud: 1800112211."
    res = analyze_message(msg)
    
    assert res["risk_score"] <= 25
    assert res["risk_level"] == "LOW"

if __name__ == "__main__":
    pytest.main(["-v", "backend/tests/test_risk_engine.py"])
