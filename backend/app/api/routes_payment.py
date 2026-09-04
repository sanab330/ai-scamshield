"""
API Router for Payment Risk Manager, Stop Before You Pay, and What-If Simulator.
"""

import uuid
import hashlib
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from backend.app.schemas.pydantic_models import PaymentRiskRequest, PaymentRiskResponse
from ai.inference.payment_scorer import calculate_payment_risk
from backend.app.database.models import save_scan_record

router = APIRouter()

@router.post("/scan/payment", response_model=PaymentRiskResponse)
def scan_payment_endpoint(payload: PaymentRiskRequest):
    res = calculate_payment_risk(
        amount=payload.amount,
        is_new_recipient=payload.is_new_recipient,
        recipient_history_count=payload.recipient_history_count,
        transaction_hour=payload.transaction_hour,
        has_urgency_pressure=payload.has_urgency_pressure,
        is_device_changed=payload.is_device_changed,
        checklist_answers=payload.checklist_answers
    )

    scan_id = str(uuid.uuid4())
    content_preview = f"Payment ₹{payload.amount:,.2f} to {'New' if payload.is_new_recipient else 'Known'} recipient at {payload.transaction_hour:02d}:00"
    content_hash = hashlib.sha256(content_preview.encode("utf-8")).hexdigest()
    created_at = datetime.now(timezone.utc).isoformat()

    # Persist to SQLite
    save_scan_record(
        record_id=scan_id,
        scan_type="PAYMENT",
        content_preview=content_preview,
        content_hash=content_hash,
        risk_score=res["risk_score"],
        risk_level=res["risk_level"],
        confidence=0.95,
        detected_signals=res["signals"],
        explanation={"attributions": res["attributions"], "summary": res["status"]},
        recommendation=res["recommendation"],
        is_offline=res["is_offline"]
    )

    return PaymentRiskResponse(
        id=scan_id,
        amount=res["amount"],
        is_new_recipient=res["is_new_recipient"],
        transaction_hour=res["transaction_hour"],
        risk_score=res["risk_score"],
        risk_level=res["risk_level"],
        status=res["status"],
        signals=res["signals"],
        attributions=res["attributions"],
        recommendation=res["recommendation"],
        is_offline=res["is_offline"],
        created_at=created_at
    )
