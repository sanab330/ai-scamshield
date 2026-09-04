"""
API Router for URL & Phishing Link Inspection.
"""

import uuid
import hashlib
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from backend.app.schemas.pydantic_models import UrlScanRequest, UrlScanResponse
from ai.inference.url_analyzer import analyze_url
from backend.app.database.models import save_scan_record

router = APIRouter()

@router.post("/scan/url", response_model=UrlScanResponse)
def scan_url_endpoint(payload: UrlScanRequest):
    if not payload.url or not payload.url.strip():
        raise HTTPException(status_code=400, detail="URL cannot be empty.")

    res = analyze_url(payload.url)
    scan_id = str(uuid.uuid4())
    content_hash = hashlib.sha256(payload.url.strip().encode("utf-8")).hexdigest()
    created_at = datetime.now(timezone.utc).isoformat()

    # Persist to SQLite
    save_scan_record(
        record_id=scan_id,
        scan_type="URL",
        content_preview=payload.url[:120],
        content_hash=content_hash,
        risk_score=res["risk_score"],
        risk_level=res["risk_level"],
        confidence=res["confidence"],
        detected_signals=res["signals"],
        explanation={"attributions": res["attribution"], "summary": res["status"]},
        recommendation=res["recommendation"],
        is_offline=res["is_offline"]
    )

    return UrlScanResponse(
        id=scan_id,
        url=res["url"],
        hostname=res["hostname"],
        risk_score=res["risk_score"],
        risk_level=res["risk_level"],
        status=res["status"],
        confidence=res["confidence"],
        signals=res["signals"],
        attribution=res["attribution"],
        recommendation=res["recommendation"],
        is_offline=res["is_offline"],
        is_https=res["is_https"],
        impersonated_brand=res.get("impersonated_brand"),
        created_at=created_at
    )
