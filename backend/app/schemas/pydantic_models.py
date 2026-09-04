"""
Pydantic Request & Response Schemas for AI ScamShield.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# Message Scan
class MessageScanRequest(BaseModel):
    text: str = Field(..., description="Message text to analyze for scam and fraud indicators")

class AttributionItem(BaseModel):
    factor: str
    percentage: int
    description: str

class ExplanationResponse(BaseModel):
    status_headline: str
    summary: str
    attributions: List[AttributionItem]
    key_drivers: List[str]

class ScanResponse(BaseModel):
    id: str
    scan_type: str
    risk_score: int
    risk_level: str
    status: str
    confidence: float
    detected_signals: List[str]
    explanation: ExplanationResponse
    recommendation: str
    is_offline: bool
    masked_preview: str
    created_at: str

# URL Scan
class UrlScanRequest(BaseModel):
    url: str = Field(..., description="URL / Web link to inspect for phishing")

class UrlScanResponse(BaseModel):
    id: str
    url: str
    hostname: str
    risk_score: int
    risk_level: str
    status: str
    confidence: float
    signals: List[str]
    attribution: List[AttributionItem]
    recommendation: str
    is_offline: bool
    is_https: bool
    impersonated_brand: Optional[str] = None
    created_at: str

# Conversation Scan
class ConversationScanRequest(BaseModel):
    conversation_text: str = Field(..., description="Multi-turn conversation transcript")

class TurnAnalysisItem(BaseModel):
    turn_number: int
    speaker: str
    text_preview: str
    turn_risk: int
    running_risk: int
    matched_stages: List[str]

class ConversationScanResponse(BaseModel):
    id: str
    conversation_risk: int
    risk_level: str
    status: str
    early_warning_triggered: bool
    early_warning_turn: Optional[int] = None
    early_warning_message: str
    escalation_stages: List[str]
    turns_analysis: List[TurnAnalysisItem]
    total_turns: int
    recommendation: str
    created_at: str

# Payment Risk & Pre-Payment Checklist
class PaymentRiskRequest(BaseModel):
    amount: float = Field(..., ge=0, description="Transaction amount")
    is_new_recipient: bool = Field(default=True)
    recipient_history_count: int = Field(default=0)
    transaction_hour: int = Field(default=14, ge=0, le=23)
    has_urgency_pressure: bool = Field(default=False)
    is_device_changed: bool = Field(default=False)
    checklist_answers: Optional[Dict[str, bool]] = None

class PaymentRiskResponse(BaseModel):
    id: str
    amount: float
    is_new_recipient: bool
    transaction_hour: int
    risk_score: int
    risk_level: str
    status: str
    signals: List[str]
    attributions: List[AttributionItem]
    recommendation: str
    is_offline: bool
    created_at: str

# Profile Scan
class ProfileScanRequest(BaseModel):
    username: str
    bio: Optional[str] = ""
    account_age_days: Optional[int] = 365
    followers_count: Optional[int] = 100
    following_count: Optional[int] = 100
    has_external_link: Optional[bool] = False

class ProfileScanResponse(BaseModel):
    id: str
    username: str
    risk_score: int
    risk_level: str
    status: str
    signals: List[str]
    attributions: List[AttributionItem]
    recommendation: str
    is_offline: bool
    disclaimer: str
    created_at: str

# Feedback & Stats
class FeedbackRequest(BaseModel):
    scan_id: str
    feedback_type: str = Field(..., description="'CORRECT', 'FALSE_ALARM', or 'MISSED_SCAM'")
    notes: Optional[str] = None

class DashboardStatsResponse(BaseModel):
    total_scans: int
    threats_detected: int
    safe_scans: int
    distribution: Dict[str, int]
    recent_scans: List[Dict[str, Any]]
