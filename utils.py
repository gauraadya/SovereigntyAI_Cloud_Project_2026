"""
Utility functions for SovereigntyAI.
Provides input validation, payload normalization, ID generation,
and formatting utilities for presentation layers.
"""

import re
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional
import config

def generate_assessment_id() -> str:
    """Generate a readable, unique compliance assessment ID."""
    short_uuid = uuid.uuid4().hex[:8].upper()
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"SOV-{date_str}-{short_uuid}"

def sanitize_text(text: Optional[str], max_len: int = 500) -> str:
    """Sanitize and trim arbitrary string input to prevent injection."""
    if not text:
        return ""
    # Strip dangerous HTML tags
    cleaned = re.sub(r"<[^>]*?>", "", str(text))
    return cleaned.strip()[:max_len]

def normalize_payload(form_data: Dict[str, Any]) -> Tuple[bool, Optional[str], Dict[str, Any]]:
    """
    Validate and normalize input payload from Web Form or JSON API.
    Returns (is_valid, error_message, clean_payload).
    """
    origin_jurisdiction = form_data.get("origin_jurisdiction", "").strip()
    data_category = form_data.get("data_category", "").strip()
    storage_region = form_data.get("storage_region", "").strip()
    backup_region = form_data.get("backup_region", "").strip()
    source_org = sanitize_text(form_data.get("source_org", "University Cloud Lab"), max_len=120)
    framework = form_data.get("framework", "General Data Sovereignty").strip()
    notes = sanitize_text(form_data.get("notes", ""), max_len=1000)

    # Basic validations
    if not origin_jurisdiction or origin_jurisdiction not in config.JURISDICTIONS:
        return False, f"Invalid or missing origin jurisdiction: '{origin_jurisdiction}'.", {}

    if not data_category or data_category not in config.DATA_CATEGORIES:
        return False, f"Invalid or missing data category: '{data_category}'.", {}

    if not storage_region or storage_region not in config.AWS_REGIONS:
        return False, f"Invalid or missing AWS storage region: '{storage_region}'.", {}

    if backup_region and backup_region not in config.AWS_REGIONS:
        return False, f"Invalid AWS backup region: '{backup_region}'.", {}

    # Boolean normalization
    def parse_bool(val: Any) -> bool:
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return bool(val)
        if isinstance(val, str):
            return val.lower() in ["1", "true", "yes", "on", "checked"]
        return False

    cross_border = parse_bool(form_data.get("cross_border", False))
    encryption_at_rest = parse_bool(form_data.get("encryption_at_rest", False))
    access_control = parse_bool(form_data.get("access_control", False))
    audit_logging = parse_bool(form_data.get("audit_logging", False))
    
    transfer_mechanism = form_data.get("transfer_mechanism", "none_unverified").strip()
    if transfer_mechanism not in config.TRANSFER_MECHANISMS:
        transfer_mechanism = "none_unverified"

    clean_payload = {
        "id": form_data.get("id") or generate_assessment_id(),
        "timestamp": form_data.get("timestamp") or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "source_org": source_org,
        "origin_jurisdiction": origin_jurisdiction,
        "data_category": data_category,
        "storage_region": storage_region,
        "backup_region": backup_region if backup_region else "None",
        "cross_border": cross_border,
        "transfer_mechanism": transfer_mechanism,
        "encryption_at_rest": encryption_at_rest,
        "access_control": access_control,
        "audit_logging": audit_logging,
        "framework": framework,
        "notes": notes
    }

    return True, None, clean_payload

def get_status_badge(status: str) -> str:
    """Return CSS badge class corresponding to compliance status."""
    if status == config.STATUS_COMPLIANT:
        return "badge-compliant"
    elif status == config.STATUS_NON_COMPLIANT:
        return "badge-noncompliant"
    return "badge-review"
