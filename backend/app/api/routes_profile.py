"""
API Router for Social Media Fake Account & Impersonation Inspector.
"""

import uuid
import hashlib
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from backend.app.schemas.pydantic_models import ProfileScanRequest, ProfileScanResponse
from ai.inference.profile_analyzer import analyze_profile
from backend.app.database.models import save_scan_record

router = APIRouter()

@router.post("/scan/profile", response_model=ProfileScanResponse)
def scan_profile_endpoint(payload: ProfileScanRequest):
    if not payload.username or not payload.username.strip():
        raise HTTPException(status_code=400, detail="Username cannot be empty.")

    res = analyze_profile(
        username=payload.username,
        bio=payload.bio or "",
        account_age_days=payload.account_age_days or 365,
        followers_count=payload.followers_count or 100,
        following_count=payload.following_count or 100,
        has_external_link=payload.has_external_link or False
    )

    scan_id = str(uuid.uuid4())
    content_preview = f"Profile @{payload.username} (Age: {payload.account_age_days}d): {(payload.bio or '')[:60]}"
    content_hash = hashlib.sha256(content_preview.encode("utf-8")).hexdigest()
    created_at = datetime.now(timezone.utc).isoformat()

    # Persist to SQLite
    save_scan_record(
        record_id=scan_id,
        scan_type="PROFILE",
        content_preview=content_preview,
        content_hash=content_hash,
        risk_score=res["risk_score"],
        risk_level=res["risk_level"],
        confidence=0.90,
        detected_signals=res["signals"],
        explanation={"attributions": res["attributions"], "summary": res["status"]},
        recommendation=res["recommendation"],
        is_offline=res["is_offline"]
    )

    return ProfileScanResponse(
        id=scan_id,
        username=res["username"],
        risk_score=res["risk_score"],
        risk_level=res["risk_level"],
        status=res["status"],
        signals=res["signals"],
        attributions=res["attributions"],
        recommendation=res["recommendation"],
        is_offline=res["is_offline"],
        disclaimer=res["disclaimer"],
        created_at=created_at
    )
