"""
Generate Synthetic Dataset for SovereigntyAI Cloud Compliance Project.
Creates a documented, reproducible synthetic dataset of cross-border cloud deployment scenarios
to train and evaluate a scikit-learn baseline model.

Dataset is saved to dataset/processed/synthetic_compliance_data.csv.
"""

import csv
import random
from pathlib import Path
import sys

# Ensure parent directory is in Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config
from policy_engine import PolicyEngine
from risk_assessment import RiskAssessmentEngine

def generate_synthetic_dataset(num_samples: int = 1200, seed: int = 42) -> Path:
    """Generate reproducible synthetic compliance dataset evaluated by the policy engine."""
    random.seed(seed)
    
    jurisdictions = ["EU_EEA", "IN", "US_FED", "US_CA", "UK", "GLOBAL_OTHER"]
    data_categories = ["non_personal", "personal", "financial", "healthcare", "sensitive_personal"]
    aws_regions = list(config.AWS_REGIONS.keys())
    transfer_mechanisms = list(config.TRANSFER_MECHANISMS.keys())
    frameworks = ["GDPR", "DPDP Act 2023", "HIPAA", "PCI-DSS / ISO 27001", "Cross-Border Standard"]

    engine = PolicyEngine()
    output_path = config.BASE_DIR / "dataset" / "processed" / "synthetic_compliance_data.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    headers = [
        "scenario_id",
        "origin_jurisdiction",
        "data_category",
        "storage_region",
        "backup_region",
        "cross_border",
        "transfer_mechanism",
        "encryption_at_rest",
        "access_control",
        "audit_logging",
        "framework",
        "risk_score",
        "risk_category",
        "compliance_status"
    ]

    for i in range(1, num_samples + 1):
        origin = random.choice(jurisdictions)
        cat = random.choice(data_categories)
        storage = random.choice(aws_regions)
        backup = random.choice([""] + aws_regions)
        
        # Determine if destination region is cross-border
        native_regions = config.JURISDICTIONS.get(origin, {}).get("native_regions", [])
        is_cross_border = (storage not in native_regions) if native_regions else random.choice([True, False])
        
        # Bias transfer mechanism realistically
        if is_cross_border:
            transfer_mech = random.choice(transfer_mechanisms)
        else:
            transfer_mech = random.choice(["adequate_country", "scc", "none_unverified"])

        # Security controls
        enc = random.choice([1, 1, 1, 0])  # 75% adoption
        acc = random.choice([1, 1, 1, 0])
        log = random.choice([1, 1, 0, 0])  # 50% adoption
        
        fw = random.choice(frameworks)

        payload = {
            "origin_jurisdiction": origin,
            "data_category": cat,
            "storage_region": storage,
            "backup_region": backup,
            "cross_border": is_cross_border,
            "transfer_mechanism": transfer_mech,
            "encryption_at_rest": bool(enc),
            "access_control": bool(acc),
            "audit_logging": bool(log),
            "framework": fw
        }

        # Evaluate through policy & risk engine to produce ground truth labels
        policy_results = engine.evaluate(payload)
        risk_result = RiskAssessmentEngine.calculate_risk(payload, policy_results)

        rows.append([
            f"SYN-{i:05d}",
            origin,
            cat,
            storage,
            backup if backup else "none",
            1 if is_cross_border else 0,
            transfer_mech,
            enc,
            acc,
            log,
            fw,
            risk_result["risk_score"],
            risk_result["risk_category"],
            risk_result["compliance_status"]
        ])

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"[Dataset] Generated {num_samples} synthetic scenarios to {output_path}")
    return output_path

if __name__ == "__main__":
    generate_synthetic_dataset()
