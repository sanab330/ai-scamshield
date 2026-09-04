"""
API Router for AI ScamShield Scan Endpoints.
"""

import uuid
import hashlib
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from backend.app.schemas.pydantic_models import (
    MessageScanRequest,
    ScanResponse,
    FeedbackRequest,
    DashboardStatsResponse
)
from ai.inference.text_classifier import analyze_message
from backend.app.database.models import (
    save_scan_record,
    get_scan_history,
    get_dashboard_stats,
    clear_scan_history,
    record_feedback
)

router = APIRouter()

@router.post("/scan/message", response_model=ScanResponse)
def scan_message_endpoint(payload: MessageScanRequest):
    """
    Analyzes an incoming or user-submitted message for scam and fraud indicators.
    Saves the analyzed incident into local SQLite storage with PII masking.
    """
    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail="Message text cannot be empty.")

    # 1. Run Offline AI Detection Engine
    res = analyze_message(payload.text)

    # 2. Generate Unique Identifiers
    scan_id = str(uuid.uuid4())
    content_hash = hashlib.sha256(payload.text.strip().encode("utf-8")).hexdigest()
    created_at = datetime.now(timezone.utc).isoformat()

    # 3. Persist to Local SQLite Database
    save_scan_record(
        record_id=scan_id,
        scan_type="MESSAGE",
        content_preview=res["masked_preview"],
        content_hash=content_hash,
        risk_score=res["risk_score"],
        risk_level=res["risk_level"],
        confidence=res["confidence"],
        detected_signals=res["detected_signals"],
        explanation=res["explanation"],
        recommendation=res["recommendation"],
        is_offline=res["is_offline"]
    )

    return ScanResponse(
        id=scan_id,
        scan_type="MESSAGE",
        risk_score=res["risk_score"],
        risk_level=res["risk_level"],
        status=res["status"],
        confidence=res["confidence"],
        detected_signals=res["detected_signals"],
        explanation=res["explanation"],
        recommendation=res["recommendation"],
        is_offline=res["is_offline"],
        masked_preview=res["masked_preview"],
        created_at=created_at
    )

@router.get("/stats/dashboard", response_model=DashboardStatsResponse)
def get_stats_endpoint():
    """Returns local protection statistics and recent scans for the Executive Dashboard."""
    return get_dashboard_stats()

@router.get("/history")
def get_history_endpoint(limit: int = 50):
    """Returns past scans stored in the on-device SQLite database."""
    return get_scan_history(limit=limit)

@router.delete("/history")
def clear_history_endpoint():
    """Permanently purges all scan records from the local SQLite database."""
    clear_scan_history()
    return {"status": "success", "message": "Local history successfully wiped."}

@router.post("/feedback")
def submit_feedback_endpoint(feedback: FeedbackRequest):
    """Stores user feedback (CORRECT / FALSE_ALARM / MISSED_SCAM) for local risk learning."""
    record_feedback(
        scan_id=feedback.scan_id,
        feedback_type=feedback.feedback_type,
        notes=feedback.notes
    )
    return {"status": "success", "message": "Feedback recorded locally."}
