"""
Comprehensive Test Suite for All Modules of AI ScamShield.
Verifies URL, Conversation Early Warning, Payment Shield, and Profile Inspector.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

# 1. URL Scanner Tests
def test_url_phishing_detection():
    payload = {"url": "http://sbi-kyc-verification.xyz/login.php?verify=1"}
    response = client.post("/api/scan/url", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] >= 75
    assert data["risk_level"] in ["HIGH", "CRITICAL"]
    assert "signals" in data
    assert any("SBI" in s or "TLD" in s or "Insecure" in s for s in data["signals"])

def test_url_safe_legitimate():
    payload = {"url": "https://www.amazon.com/dp/product123"}
    response = client.post("/api/scan/url", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] <= 25
    assert data["risk_level"] == "LOW"

# 2. Multi-Turn Conversation & Early Warning Tests
def test_conversation_early_warning():
    conv_text = """
Person: Hello, I am calling from HDFC Bank Customer Support.
User: Yes, what is the matter?
Person: Your account will be permanently blocked today due to pending KYC verification.
User: Why will it be blocked? I already submitted my documents.
Person: Complete your digital verification immediately within 30 minutes to avoid penalty.
Person: Click this link to update: http://hdfc-verify.top
Person: Pay a small verification charge of Rs 10 to activate your card.
    """
    response = client.post("/api/scan/conversation", json={"conversation_text": conv_text})
    assert response.status_code == 200
    data = response.json()
    assert data["conversation_risk"] >= 75
    assert data["early_warning_triggered"] is True
    assert len(data["escalation_stages"]) >= 3

# 3. Payment Risk & Pre-Flight Checklist Tests
def test_payment_high_risk_scenario():
    payload = {
        "amount": 75000,
        "is_new_recipient": True,
        "recipient_history_count": 0,
        "transaction_hour": 3,
        "has_urgency_pressure": True,
        "checklist_answers": {
            "know_recipient": False,
            "user_initiated": False,
            "act_urgently": True,
            "share_otp_pin": True,
            "unexpected_contact": True,
            "suspicious_link": True,
            "unrealistic_reward": False
        }
    }
    response = client.post("/api/scan/payment", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] >= 80
    assert data["risk_level"] == "CRITICAL"
    assert any("OTP" in s for s in data["signals"])

def test_payment_low_risk_scenario():
    payload = {
        "amount": 350,
        "is_new_recipient": False,
        "recipient_history_count": 15,
        "transaction_hour": 14,
        "has_urgency_pressure": False,
        "checklist_answers": {
            "know_recipient": True,
            "user_initiated": True,
            "act_urgently": False,
            "share_otp_pin": False,
            "unexpected_contact": False,
            "suspicious_link": False,
            "unrealistic_reward": False
        }
    }
    response = client.post("/api/scan/payment", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] <= 25
    assert data["risk_level"] == "LOW"

# 4. Social Media Profile Analyzer Tests
def test_profile_high_risk_impersonator():
    payload = {
        "username": "sbi_official_helpdesk_849204",
        "bio": "Official 24/7 SBI customer support desk. DM to recover blocked money. WhatsApp +919876501234",
        "account_age_days": 4,
        "followers_count": 15,
        "following_count": 1200,
        "has_external_link": True
    }
    response = client.post("/api/scan/profile", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] >= 70
    assert data["risk_level"] in ["HIGH", "CRITICAL"]

def test_profile_normal_user():
    payload = {
        "username": "rahul_dev99",
        "bio": "Building open-source software and exploring machine learning. Coffee enthusiast.",
        "account_age_days": 850,
        "followers_count": 420,
        "following_count": 310,
        "has_external_link": False
    }
    response = client.post("/api/scan/profile", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] <= 25
    assert data["risk_level"] == "LOW"

if __name__ == "__main__":
    pytest.main(["-v", "backend/tests/test_all_modules.py"])
