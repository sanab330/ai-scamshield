"""
API Router for Multi-Turn Conversation Analysis & Early Warning Detection.
"""

import uuid
import hashlib
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from backend.app.schemas.pydantic_models import ConversationScanRequest, ConversationScanResponse
from ai.inference.conversation_analyzer import analyze_conversation
from backend.app.database.models import save_scan_record

router = APIRouter()

@router.post("/scan/conversation", response_model=ConversationScanResponse)
def scan_conversation_endpoint(payload: ConversationScanRequest):
    if not payload.conversation_text or not payload.conversation_text.strip():
        raise HTTPException(status_code=400, detail="Conversation text cannot be empty.")

    res = analyze_conversation(payload.conversation_text)
    scan_id = str(uuid.uuid4())
    content_hash = hashlib.sha256(payload.conversation_text.strip().encode("utf-8")).hexdigest()
    created_at = datetime.now(timezone.utc).isoformat()

    # Persist to SQLite
    save_scan_record(
        record_id=scan_id,
        scan_type="CONVERSATION",
        content_preview=payload.conversation_text[:120].replace("\n", " "),
        content_hash=content_hash,
        risk_score=res["conversation_risk"],
        risk_level=res["risk_level"],
        confidence=0.92,
        detected_signals=res["escalation_stages"],
        explanation={"attributions": [], "summary": res["early_warning_message"]},
        recommendation=res["recommendation"],
        is_offline=True
    )

    return ConversationScanResponse(
        id=scan_id,
        conversation_risk=res["conversation_risk"],
        risk_level=res["risk_level"],
        status=res["status"],
        early_warning_triggered=res["early_warning_triggered"],
        early_warning_turn=res["early_warning_turn"],
        early_warning_message=res["early_warning_message"],
        escalation_stages=res["escalation_stages"],
        turns_analysis=res["turns_analysis"],
        total_turns=res["total_turns"],
        recommendation=res["recommendation"],
        created_at=created_at
    )
