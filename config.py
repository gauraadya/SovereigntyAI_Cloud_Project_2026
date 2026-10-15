"""
Configuration settings for the SovereigntyAI Compliance Framework.
Provides centralized path configuration, AWS region mapping, jurisdiction metadata,
and risk scoring thresholds.
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "data" / "sovereignty_ai.db"
POLICIES_PATH = BASE_DIR / "policies" / "policy_rules.json"
SCENARIOS_PATH = BASE_DIR / "dataset" / "sample_scenarios.json"
ML_MODEL_PATH = BASE_DIR / "src" / "ml_model" / "sovereignty_risk_model.joblib"
ML_METRICS_PATH = BASE_DIR / "results" / "model_metrics.json"

# Ensure runtime directories exist
(BASE_DIR / "data").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "results").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "policies").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "dataset" / "raw").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "dataset" / "processed").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "src" / "ml_model").mkdir(parents=True, exist_ok=True)

# Application secret and debug settings
SECRET_KEY = os.environ.get("SECRET_KEY", "sovereignty-ai-academic-prototype-key-2026")
DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
PORT = int(os.environ.get("PORT", 5001))

# Supported Jurisdictions and their ISO / Regional Codes
JURISDICTIONS = {
    "EU_EEA": {
        "name": "European Union / European Economic Area",
        "primary_law": "General Data Protection Regulation (GDPR)",
        "native_regions": [
            "eu-central-1", "eu-central-2", "eu-west-1",
            "eu-west-2", "eu-west-3", "eu-north-1", "eu-south-1", "eu-south-2"
        ],
        "adequate_jurisdictions": ["EU_EEA", "UK", "CH", "JP", "CA", "NZ", "KR"],
        "notes": "GDPR Chapter V governs cross-border transfers. Adequacy decisions or Article 46 safeguards (SCCs) are mandatory for external transfers."
    },
    "IN": {
        "name": "India",
        "primary_law": "Digital Personal Data Protection Act, 2023 (DPDP Act)",
        "native_regions": ["ap-south-1", "ap-south-2"],
        "adequate_jurisdictions": ["IN"],  # Blacklist approach pending central govt notification
        "notes": "DPDP Act Sec 16 allows cross-border transfers except to countries restricted by the Central Government. Security safeguards under Sec 8 are mandatory."
    },
    "US_FED": {
        "name": "United States (Federal / Sectoral)",
        "primary_law": "Sectoral Privacy Framework (HIPAA, GLBA, FedRAMP)",
        "native_regions": ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "us-gov-east-1", "us-gov-west-1"],
        "adequate_jurisdictions": ["US_FED", "US_CA"],
        "notes": "Sectoral requirements apply based on data category (e.g., HIPAA Security Rule for PHI, GLBA Safeguards Rule for financial data)."
    },
    "US_CA": {
        "name": "United States (California)",
        "primary_law": "California Consumer Privacy Act / CPRA",
        "native_regions": ["us-east-1", "us-east-2", "us-west-1", "us-west-2"],
        "adequate_jurisdictions": ["US_FED", "US_CA"],
        "notes": "Consumer privacy disclosures, purpose limitation, and service provider contract requirements apply."
    },
    "UK": {
        "name": "United Kingdom",
        "primary_law": "UK GDPR & Data Protection Act 2018",
        "native_regions": ["eu-west-2"],
        "adequate_jurisdictions": ["UK", "EU_EEA"],
        "notes": "International Data Transfer Agreement (IDTA) or UK Addendum required for third-country transfers without adequacy."
    },
    "GLOBAL_OTHER": {
        "name": "Other / International Jurisdiction",
        "primary_law": "Local Privacy & Sovereignty Regulations",
        "native_regions": [],
        "adequate_jurisdictions": [],
        "notes": "Baseline international best-practice privacy and data security rules apply."
    }
}

# AWS Region Metadata
AWS_REGIONS = {
    "eu-central-1": {"location": "Frankfurt, Germany", "jurisdiction": "EU_EEA", "sovereign_cloud_ready": True},
    "eu-central-2": {"location": "Zurich, Switzerland", "jurisdiction": "EU_EEA", "sovereign_cloud_ready": True},
    "eu-west-1": {"location": "Dublin, Ireland", "jurisdiction": "EU_EEA", "sovereign_cloud_ready": True},
    "eu-west-2": {"location": "London, United Kingdom", "jurisdiction": "UK", "sovereign_cloud_ready": True},
    "eu-west-3": {"location": "Paris, France", "jurisdiction": "EU_EEA", "sovereign_cloud_ready": True},
    "eu-north-1": {"location": "Stockholm, Sweden", "jurisdiction": "EU_EEA", "sovereign_cloud_ready": True},
    "eu-south-1": {"location": "Milan, Italy", "jurisdiction": "EU_EEA", "sovereign_cloud_ready": True},
    "ap-south-1": {"location": "Mumbai, India", "jurisdiction": "IN", "sovereign_cloud_ready": True},
    "ap-south-2": {"location": "Hyderabad, India", "jurisdiction": "IN", "sovereign_cloud_ready": True},
    "us-east-1": {"location": "N. Virginia, USA", "jurisdiction": "US_FED", "sovereign_cloud_ready": False},
    "us-east-2": {"location": "Ohio, USA", "jurisdiction": "US_FED", "sovereign_cloud_ready": False},
    "us-west-1": {"location": "N. California, USA", "jurisdiction": "US_CA", "sovereign_cloud_ready": False},
    "us-west-2": {"location": "Oregon, USA", "jurisdiction": "US_FED", "sovereign_cloud_ready": False},
    "ap-southeast-1": {"location": "Singapore", "jurisdiction": "GLOBAL_OTHER", "sovereign_cloud_ready": False},
    "ap-northeast-1": {"location": "Tokyo, Japan", "jurisdiction": "GLOBAL_OTHER", "sovereign_cloud_ready": False},
    "ap-southeast-2": {"location": "Sydney, Australia", "jurisdiction": "GLOBAL_OTHER", "sovereign_cloud_ready": False},
    "me-south-1": {"location": "Bahrain", "jurisdiction": "GLOBAL_OTHER", "sovereign_cloud_ready": False},
    "af-south-1": {"location": "Cape Town, South Africa", "jurisdiction": "GLOBAL_OTHER", "sovereign_cloud_ready": False},
    "sa-east-1": {"location": "São Paulo, Brazil", "jurisdiction": "GLOBAL_OTHER", "sovereign_cloud_ready": False}
}

# Data Categories and Sensitivity Levels
DATA_CATEGORIES = {
    "non_personal": {
        "label": "Non-Personal / Public Telemetry",
        "sensitivity_weight": 5,
        "description": "Anonymized technical telemetry, public logs, aggregated system statistics."
    },
    "personal": {
        "label": "Standard Personal Data",
        "sensitivity_weight": 20,
        "description": "Direct identifiers such as customer names, email addresses, phone numbers, and profile data."
    },
    "financial": {
        "label": "Financial / Payment Data",
        "sensitivity_weight": 35,
        "description": "Payment card details (PCI-DSS), bank account numbers, transaction histories, credit scores."
    },
    "healthcare": {
        "label": "Protected Health Information (PHI) / Medical Records",
        "sensitivity_weight": 40,
        "description": "Medical histories, diagnostic records, biometric identifiers, health insurance information."
    },
    "sensitive_personal": {
        "label": "Special Category / Sensitive Personal Data",
        "sensitivity_weight": 40,
        "description": "Biometrics, genetic data, racial/ethnic origin, religious beliefs, trade union membership."
    }
}

# Transfer Mechanisms
TRANSFER_MECHANISMS = {
    "adequate_country": "Adequacy Decision (Article 45 GDPR or Equivalent)",
    "scc": "Standard Contractual Clauses (SCCs / Model Contract)",
    "bcr": "Binding Corporate Rules (BCR)",
    "explicit_consent": "Explicit Informed Consent of Data Subject",
    "statutory_exemption": "Statutory / Legal / Public Interest Exemption",
    "none_unverified": "None / Unverified Transfer Mechanism"
}

# Risk Scoring Bands (0 - 100)
RISK_BANDS = {
    "Low": {"min": 0, "max": 25, "badge_class": "badge-success", "color": "#10b981"},
    "Moderate": {"min": 26, "max": 50, "badge_class": "badge-info", "color": "#3b82f6"},
    "High": {"min": 51, "max": 75, "badge_class": "badge-warning", "color": "#f59e0b"},
    "Critical": {"min": 76, "max": 100, "badge_class": "badge-danger", "color": "#ef4444"}
}

# Final Compliance Status Values
STATUS_COMPLIANT = "COMPLIANT"
STATUS_NON_COMPLIANT = "NON_COMPLIANT"
STATUS_NEEDS_REVIEW = "NEEDS_REVIEW"
