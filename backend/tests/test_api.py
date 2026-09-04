"""
API Integration Tests for AI ScamShield Backend Endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "AI ScamShield"

def test_scan_scam_message_api():
    payload = {
        "text": "URGENT: Your SBI account is suspended due to pending KYC. Click http://sbi-kyc-update.xyz now or face ₹10,000 penalty."
    }
    response = client.post("/api/scan/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["risk_score"] >= 75
    assert data["risk_level"] in ["HIGH", "CRITICAL"]
    assert "explanation" in data
    assert len(data["explanation"]["attributions"]) > 0
    assert sum(a["percentage"] for a in data["explanation"]["attributions"]) == 100

def test_scan_normal_message_api():
    payload = {
        "text": "Your Swiggy order from Chai Point is on the way! Delivery partner Ramesh is arriving in 12 minutes."
    }
    response = client.post("/api/scan/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["risk_score"] <= 25
    assert data["risk_level"] == "LOW"
    assert data["explanation"]["status_headline"] == "Low Observed Risk"

def test_dashboard_stats_and_history():
    stats_res = client.get("/api/stats/dashboard")
    assert stats_res.status_code == 200
    stats = stats_res.json()
    assert stats["total_scans"] >= 2
    assert "distribution" in stats

    history_res = client.get("/api/history")
    assert history_res.status_code == 200
    history = history_res.json()
    assert len(history) >= 2

def test_user_feedback():
    history_res = client.get("/api/history")
    scan_id = history_res.json()[0]["id"]
    
    fb_res = client.post("/api/feedback", json={
        "scan_id": scan_id,
        "feedback_type": "CORRECT",
        "notes": "Accurate detection of bank KYC threat."
    })
    assert fb_res.status_code == 200
    assert fb_res.json()["status"] == "success"

if __name__ == "__main__":
    pytest.main(["-v", "backend/tests/test_api.py"])
