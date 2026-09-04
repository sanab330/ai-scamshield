"""
SQLite Database Models for AI ScamShield.
Stores local scan history, explanations, and user feedback.
Contains NO sensitive credentials or unmasked secrets.
"""

import sqlite3
import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "scamshield.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes SQLite schema if not present."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Scan History Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id TEXT PRIMARY KEY,
            scan_type TEXT NOT NULL,
            content_preview TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            risk_level TEXT NOT NULL,
            confidence REAL NOT NULL,
            detected_signals TEXT NOT NULL,
            explanation_json TEXT NOT NULL,
            recommendation TEXT NOT NULL,
            is_offline INTEGER DEFAULT 1,
            created_at TEXT NOT NULL
        );
        """)

        # User Feedback Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_feedback (
            id TEXT PRIMARY KEY,
            scan_id TEXT NOT NULL,
            feedback_type TEXT NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(scan_id) REFERENCES scan_history(id) ON DELETE CASCADE
        );
        """)

        conn.commit()

# Ensure schema exists on module load
init_db()

def save_scan_record(
    record_id: str,
    scan_type: str,
    content_preview: str,
    content_hash: str,
    risk_score: int,
    risk_level: str,
    confidence: float,
    detected_signals: List[str],
    explanation: Dict[str, Any],
    recommendation: str,
    is_offline: bool = True
):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        created_at = datetime.now(timezone.utc).isoformat()
        cursor.execute("""
        INSERT INTO scan_history (
            id, scan_type, content_preview, content_hash, risk_score,
            risk_level, confidence, detected_signals, explanation_json,
            recommendation, is_offline, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record_id,
            scan_type,
            content_preview,
            content_hash,
            risk_score,
            risk_level,
            confidence,
            json.dumps(detected_signals),
            json.dumps(explanation),
            recommendation,
            1 if is_offline else 0,
            created_at
        ))
        conn.commit()

def get_scan_history(limit: int = 50) -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM scan_history ORDER BY created_at DESC LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        
        results = []
        for r in rows:
            results.append({
                "id": r["id"],
                "scan_type": r["scan_type"],
                "content_preview": r["content_preview"],
                "risk_score": r["risk_score"],
                "risk_level": r["risk_level"],
                "confidence": r["confidence"],
                "detected_signals": json.loads(r["detected_signals"]),
                "explanation": json.loads(r["explanation_json"]),
                "recommendation": r["recommendation"],
                "is_offline": bool(r["is_offline"]),
                "created_at": r["created_at"]
            })
        return results

def get_dashboard_stats() -> Dict[str, Any]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM scan_history")
        total_scans = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM scan_history WHERE risk_score >= 51")
        threats_detected = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM scan_history WHERE risk_score <= 25")
        safe_scans = cursor.fetchone()[0]

        cursor.execute("""
        SELECT risk_level, COUNT(*) as count FROM scan_history GROUP BY risk_level
        """)
        level_counts = {row["risk_level"]: row["count"] for row in cursor.fetchall()}

        cursor.execute("SELECT * FROM scan_history ORDER BY created_at DESC LIMIT 5")
        recent = []
        for r in cursor.fetchall():
            recent.append({
                "id": r["id"],
                "scan_type": r["scan_type"],
                "content_preview": r["content_preview"],
                "risk_score": r["risk_score"],
                "risk_level": r["risk_level"],
                "created_at": r["created_at"]
            })

        return {
            "total_scans": total_scans,
            "threats_detected": threats_detected,
            "safe_scans": safe_scans,
            "distribution": {
                "LOW": level_counts.get("LOW", 0),
                "MODERATE": level_counts.get("MODERATE", 0),
                "HIGH": level_counts.get("HIGH", 0),
                "CRITICAL": level_counts.get("CRITICAL", 0),
            },
            "recent_scans": recent
        }

def clear_scan_history():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scan_history")
        cursor.execute("DELETE FROM user_feedback")
        conn.commit()

def record_feedback(scan_id: str, feedback_type: str, notes: Optional[str] = None):
    import uuid
    with get_db_connection() as conn:
        cursor = conn.cursor()
        fid = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()
        cursor.execute("""
        INSERT INTO user_feedback (id, scan_id, feedback_type, notes, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (fid, scan_id, feedback_type, notes or "", created_at))
        conn.commit()
