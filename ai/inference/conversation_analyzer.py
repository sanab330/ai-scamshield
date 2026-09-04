"""
Multi-Turn Scam Conversation Analyzer & Early Warning Engine for AI ScamShield.
Analyzes conversational dialogue flow to detect social-engineering escalation
and trigger early warnings before financial loss occurs.
"""

import re
from typing import List, Dict, Any
from ai.inference.text_classifier import analyze_message

STAGE_PATTERNS = {
    "UNSOLICITED_CONTACT": {
        "pattern": r"(?i)\b(hello|hi|good morning|dear customer|calling from|support team|executive|officer)\b",
        "weight": 15,
        "stage_name": "Unsolicited Cold Contact"
    },
    "FEAR_AUTHORITY": {
        "pattern": r"(?i)\b(blocked|suspended|deactivated|illegal|fir|police|arrest|rbi|income tax|penalty|inquiry|violation)\b",
        "weight": 35,
        "stage_name": "Authority / Fear Induction"
    },
    "URGENCY_PRESSURE": {
        "pattern": r"(?i)\b(immediately|urgent|within \d+|today only|right now|do not delay|hurry|last warning)\b",
        "weight": 30,
        "stage_name": "Artificial Urgency Manipulation"
    },
    "LINK_DELIVERY": {
        "pattern": r"(?i)https?://\S+|\b(click here|open this link|fill the form|download app)\b",
        "weight": 35,
        "stage_name": "Phishing Link / Malicious Form Delivery"
    },
    "CREDENTIAL_PAYMENT_SOLICITATION": {
        "pattern": r"(?i)\b(otp|pin|cvv|password|pay \S+|send rs|transfer fee|small verification charge|₹\s*\d+)\b",
        "weight": 50,
        "stage_name": "Payment or Credential Solicitation"
    }
}

def parse_conversation_turns(raw_text: str) -> List[Dict[str, str]]:
    """
    Parses conversation string formatted as 'Speaker: message' into structured turns.
    """
    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
    turns = []
    
    current_speaker = "Sender"
    current_msg = []

    for line in lines:
        match = re.match(r"^(Person|Scammer|Caller|Agent|User|Me|Customer|Victim|Support|Other):\s*(.*)", line, re.IGNORECASE)
        if match:
            if current_msg:
                turns.append({"speaker": current_speaker, "text": " ".join(current_msg)})
            current_speaker = match.group(1).title()
            current_msg = [match.group(2)]
        else:
            current_msg.append(line)

    if current_msg:
        turns.append({"speaker": current_speaker, "text": " ".join(current_msg)})

    # Fallback if no speaker prefixes found: split by newline into sequential turns
    if len(turns) <= 1 and len(lines) > 1:
        turns = [{"speaker": "Message " + str(i+1), "text": l} for i, l in enumerate(lines)]

    return turns

def analyze_conversation(conversation_input: str) -> Dict[str, Any]:
    """
    Performs multi-turn conversation flow analysis, computing turn-by-turn risk trajectory,
    social-engineering escalation stages, and early warning triggers.
    """
    turns = parse_conversation_turns(conversation_input)
    if not turns:
        return {
            "conversation_risk": 0,
            "risk_level": "LOW",
            "early_warning_triggered": False,
            "turns_analysis": [],
            "escalation_stages": [],
            "recommendation": "No conversation content provided."
        }

    detected_stages = []
    running_risk = 10
    turns_analysis = []
    early_warning_triggered = False
    early_warning_turn = None
    cumulative_factors = set()

    for idx, turn in enumerate(turns):
        text = turn["text"]
        speaker = turn["speaker"]
        turn_num = idx + 1

        # Analyze individual turn
        single_res = analyze_message(text)
        turn_risk = single_res["risk_score"]

        # Check conversation progression stages
        matched_stages_in_turn = []
        for stage_key, stage_info in STAGE_PATTERNS.items():
            if re.search(stage_info["pattern"], text):
                matched_stages_in_turn.append(stage_info["stage_name"])
                if stage_info["stage_name"] not in detected_stages:
                    detected_stages.append(stage_info["stage_name"])
                cumulative_factors.add(stage_key)

        # Dynamic Escalation formula: running risk increases with progressive manipulation stages
        stage_multiplier = 1.0 + (len(detected_stages) * 0.20)
        calculated_turn_risk = int(min(100, max(turn_risk, running_risk * 0.7 + (len(matched_stages_in_turn) * 20))))
        running_risk = int(min(100, (running_risk * 0.4) + (calculated_turn_risk * 0.6) * stage_multiplier))

        # Check for Early Warning Trigger (Escalation to High Risk before direct payment/credential ask)
        if not early_warning_triggered and running_risk >= 65:
            if "CREDENTIAL_PAYMENT_SOLICITATION" not in cumulative_factors:
                early_warning_triggered = True
                early_warning_turn = turn_num

        turns_analysis.append({
            "turn_number": turn_num,
            "speaker": speaker,
            "text_preview": text[:100],
            "turn_risk": calculated_turn_risk,
            "running_risk": running_risk,
            "matched_stages": matched_stages_in_turn
        })

    final_risk = running_risk

    # Determine Risk Level
    if final_risk <= 25:
        risk_level = "LOW"
        status = "LOW CONVERSATION RISK"
        recommendation = "Standard conversation flow. No high-pressure manipulation tactics detected."
    elif final_risk <= 50:
        risk_level = "MODERATE"
        status = "CAUTION ADVISED"
        recommendation = "Some pressure or unusual inquiries detected. Do not share confidential information."
    elif final_risk <= 75:
        risk_level = "HIGH"
        status = "HIGH SOCIAL-ENGINEERING RISK"
        recommendation = "Clear manipulation and pressure detected. Discontinue this conversation immediately."
    else:
        risk_level = "CRITICAL"
        status = "CRITICAL FRAUD TRAP"
        recommendation = "Classic fraud escalation trap detected! Cease all communication and block the contact immediately."

    return {
        "conversation_risk": final_risk,
        "risk_level": risk_level,
        "status": status,
        "early_warning_triggered": early_warning_triggered,
        "early_warning_turn": early_warning_turn,
        "early_warning_message": f"Developing scam pattern identified at Turn {early_warning_turn} prior to final payment solicitation." if early_warning_triggered else "No early threat escalation detected.",
        "escalation_stages": detected_stages,
        "turns_analysis": turns_analysis,
        "total_turns": len(turns),
        "recommendation": recommendation
    }
