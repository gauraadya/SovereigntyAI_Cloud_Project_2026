"""
Seed script for SovereigntyAI.
Evaluates the 6 sample scenarios and seeds them into the SQLite database
so the dashboard and history pages have live data immediately upon launch.
"""

import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
import config
import database
from policy_engine import PolicyEngine
from risk_assessment import RiskAssessmentEngine
import ai_services

def seed_database():
    database.init_db()
    
    if not config.SCENARIOS_PATH.exists():
        print("[Seed] No scenarios file found.")
        return

    with open(config.SCENARIOS_PATH, "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    engine = PolicyEngine()
    print(f"[Seed] Seeding {len(scenarios)} demonstration assessments into database...")

    for sc in scenarios:
        payload = {
            "id": f"SOV-DEMO-{sc['scenario_id']}",
            "source_org": sc.get("source_org", "Sample Enterprise"),
            "origin_jurisdiction": sc["origin_jurisdiction"],
            "data_category": sc["data_category"],
            "storage_region": sc["storage_region"],
            "backup_region": sc.get("backup_region", "None"),
            "cross_border": sc["cross_border"],
            "transfer_mechanism": sc["transfer_mechanism"],
            "encryption_at_rest": sc["encryption_at_rest"],
            "access_control": sc["access_control"],
            "audit_logging": sc["audit_logging"],
            "framework": sc["framework"],
            "notes": sc.get("notes", "")
        }

        policy_results = engine.evaluate(payload)
        risk_result = RiskAssessmentEngine.calculate_risk(payload, policy_results)
        ml_pred = ai_services.predict_compliance_ml(payload)

        record = {
            **payload,
            **risk_result,
            "policy_results": policy_results,
            "ml_prediction": ml_pred
        }

        # Check if already exists
        existing = database.get_assessment(record["id"])
        if not existing:
            database.save_assessment(record)
            print(f"  + Seeded {record['id']} ({record['compliance_status']}, Score: {record['risk_score']})")
        else:
            print(f"  * Record {record['id']} already exists in database.")

    print("[Seed] Database seeding completed successfully.")

if __name__ == "__main__":
    seed_database()
