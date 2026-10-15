"""
Database layer for SovereigntyAI.
Handles SQLite connection management, schema initialization, CRUD operations for assessments,
audit logging, statistics calculation, and export utilities.
"""

import sqlite3
import json
import csv
import io
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import config

def get_connection() -> sqlite3.Connection:
    """Establish connection to SQLite database with row factory enabled."""
    conn = sqlite3.connect(str(config.DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def managed_connection():
    """Yield a SQLite connection and always close it after use."""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize database tables for assessments and audit trails."""
    with managed_connection() as conn:
        cursor = conn.cursor()
        
        # Assessments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                source_org TEXT,
                origin_jurisdiction TEXT NOT NULL,
                data_category TEXT NOT NULL,
                storage_region TEXT NOT NULL,
                backup_region TEXT,
                cross_border INTEGER NOT NULL,
                transfer_mechanism TEXT NOT NULL,
                encryption_at_rest INTEGER NOT NULL,
                access_control INTEGER NOT NULL,
                audit_logging INTEGER NOT NULL,
                framework TEXT NOT NULL,
                compliance_status TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                risk_category TEXT NOT NULL,
                policy_results_json TEXT NOT NULL,
                factors_json TEXT NOT NULL,
                recommendations_json TEXT NOT NULL,
                notes TEXT,
                ml_prediction TEXT
            )
        """)
        
        # Audit trail table for change tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_trail (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                FOREIGN KEY (assessment_id) REFERENCES assessments (id)
            )
        """)
        conn.commit()

def save_assessment(data: Dict[str, Any]) -> str:
    """
    Persist an assessment record and create an audit log entry.
    All JSON fields are safely serialized.
    """
    assessment_id = data["id"]
    timestamp = data.get("timestamp") or datetime.now(timezone.utc).isoformat()
    
    with managed_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO assessments (
                id, timestamp, source_org, origin_jurisdiction, data_category,
                storage_region, backup_region, cross_border, transfer_mechanism,
                encryption_at_rest, access_control, audit_logging, framework,
                compliance_status, risk_score, risk_category,
                policy_results_json, factors_json, recommendations_json,
                notes, ml_prediction
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            assessment_id,
            timestamp,
            data.get("source_org", "Default Organization"),
            data["origin_jurisdiction"],
            data["data_category"],
            data["storage_region"],
            data.get("backup_region", ""),
            1 if data.get("cross_border") else 0,
            data.get("transfer_mechanism", "none_unverified"),
            1 if data.get("encryption_at_rest") else 0,
            1 if data.get("access_control") else 0,
            1 if data.get("audit_logging") else 0,
            data.get("framework", "General Data Sovereignty"),
            data["compliance_status"],
            int(data["risk_score"]),
            data["risk_category"],
            json.dumps(data.get("policy_results", [])),
            json.dumps(data.get("risk_factors", [])),
            json.dumps(data.get("recommendations", [])),
            data.get("notes", ""),
            json.dumps(data.get("ml_prediction", {}))
        ))
        
        # Add entry in audit trail
        cursor.execute("""
            INSERT INTO audit_trail (assessment_id, timestamp, action, details)
            VALUES (?, ?, ?, ?)
        """, (
            assessment_id,
            timestamp,
            "ASSESSMENT_EVALUATED",
            f"Evaluated status {data['compliance_status']} with risk score {data['risk_score']}."
        ))
        conn.commit()
    
    return assessment_id

def get_assessment(assessment_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve an assessment by ID with unpacked JSON fields."""
    with managed_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assessments WHERE id = ?", (assessment_id,))
        row = cursor.fetchone()
        if not row:
            return None
        
        d = dict(row)
        d["policy_results"] = json.loads(d["policy_results_json"]) if d["policy_results_json"] else []
        d["risk_factors"] = json.loads(d["factors_json"]) if d["factors_json"] else []
        d["recommendations"] = json.loads(d["recommendations_json"]) if d["recommendations_json"] else []
        d["ml_prediction"] = json.loads(d["ml_prediction"]) if d.get("ml_prediction") else {}
        d["cross_border"] = bool(d["cross_border"])
        d["encryption_at_rest"] = bool(d["encryption_at_rest"])
        d["access_control"] = bool(d["access_control"])
        d["audit_logging"] = bool(d["audit_logging"])
        return d

def get_assessments(
    limit: int = 50,
    offset: int = 0,
    filter_status: Optional[str] = None,
    filter_jurisdiction: Optional[str] = None,
    search_term: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieve filtered list of assessments for history view."""
    query = "SELECT * FROM assessments WHERE 1=1"
    params = []
    
    if filter_status:
        query += " AND compliance_status = ?"
        params.append(filter_status)
    
    if filter_jurisdiction:
        query += " AND origin_jurisdiction = ?"
        params.append(filter_jurisdiction)
        
    if search_term:
        query += " AND (source_org LIKE ? OR notes LIKE ? OR id LIKE ?)"
        like_term = f"%{search_term}%"
        params.extend([like_term, like_term, like_term])
        
    query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    with managed_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            d = dict(row)
            d["cross_border"] = bool(d["cross_border"])
            d["encryption_at_rest"] = bool(d["encryption_at_rest"])
            d["access_control"] = bool(d["access_control"])
            d["audit_logging"] = bool(d["audit_logging"])
            results.append(d)
        return results

def get_dashboard_stats() -> Dict[str, Any]:
    """Calculate aggregate compliance statistics and risk distributions for dashboard."""
    with managed_connection() as conn:
        cursor = conn.cursor()
        
        # Total counts
        cursor.execute("SELECT COUNT(*) FROM assessments")
        total_assessments = cursor.fetchone()[0]
        
        # Status counts
        cursor.execute("SELECT compliance_status, COUNT(*) FROM assessments GROUP BY compliance_status")
        status_counts = dict(cursor.fetchall())
        
        # Risk band counts
        cursor.execute("SELECT risk_category, COUNT(*) FROM assessments GROUP BY risk_category")
        risk_counts = dict(cursor.fetchall())
        
        # Average risk score
        cursor.execute("SELECT AVG(risk_score) FROM assessments")
        avg_score_row = cursor.fetchone()[0]
        avg_score = round(avg_score_row, 1) if avg_score_row is not None else 0.0
        
        # Recent assessments (last 5)
        cursor.execute("SELECT * FROM assessments ORDER BY timestamp DESC LIMIT 5")
        recent = [dict(r) for r in cursor.fetchall()]
        
        return {
            "total_assessments": total_assessments,
            "compliant_count": status_counts.get("COMPLIANT", 0),
            "non_compliant_count": status_counts.get("NON_COMPLIANT", 0),
            "needs_review_count": status_counts.get("NEEDS_REVIEW", 0),
            "risk_distribution": {
                "Low": risk_counts.get("Low", 0),
                "Moderate": risk_counts.get("Moderate", 0),
                "High": risk_counts.get("High", 0),
                "Critical": risk_counts.get("Critical", 0)
            },
            "average_risk_score": avg_score,
            "recent_assessments": recent
        }

def export_assessments_json() -> str:
    """Export all assessments into a JSON string."""
    with managed_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assessments ORDER BY timestamp DESC")
        rows = [dict(r) for r in cursor.fetchall()]
        for r in rows:
            if r.get("policy_results_json"):
                r["policy_results"] = json.loads(r["policy_results_json"])
            if r.get("factors_json"):
                r["risk_factors"] = json.loads(r["factors_json"])
            if r.get("recommendations_json"):
                r["recommendations"] = json.loads(r["recommendations_json"])
        return json.dumps(rows, indent=2)

def export_assessments_csv() -> str:
    """Export assessment summaries into CSV formatted string."""
    with managed_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, source_org, origin_jurisdiction, data_category,
                   storage_region, backup_region, cross_border, transfer_mechanism,
                   encryption_at_rest, access_control, audit_logging,
                   compliance_status, risk_score, risk_category
            FROM assessments ORDER BY timestamp DESC
        """)
        rows = cursor.fetchall()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Assessment ID", "Timestamp", "Organization", "Origin Jurisdiction",
            "Data Category", "Storage Region", "Backup Region", "Cross Border",
            "Transfer Mechanism", "Encryption at Rest", "Access Control",
            "Audit Logging", "Compliance Status", "Risk Score", "Risk Category"
        ])
        for row in rows:
            writer.writerow(list(row))
        return output.getvalue()
