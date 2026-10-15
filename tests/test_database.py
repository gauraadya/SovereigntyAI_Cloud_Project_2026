"""
Unit tests for Database layer.
Tests SQLite schema initialization, assessment saving, filtering, statistics, and exports.
"""

import unittest
import tempfile
from pathlib import Path
import os
import database
import config

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Use a temporary database for test isolation
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.original_db_path = config.DATABASE_PATH
        config.DATABASE_PATH = Path(self.temp_db.name)
        database.init_db()

    def tearDown(self):
        config.DATABASE_PATH = self.original_db_path
        self.temp_db.close()
        if os.path.exists(self.temp_db.name):
            try:
                os.remove(self.temp_db.name)
            except Exception:
                pass

    def test_save_and_retrieve_assessment(self):
        sample_record = {
            "id": "SOV-TEST-0001",
            "timestamp": "2026-10-15 10:00:00 UTC",
            "source_org": "Test Healthcare Clinic",
            "origin_jurisdiction": "EU_EEA",
            "data_category": "healthcare",
            "storage_region": "eu-central-1",
            "backup_region": "eu-west-1",
            "cross_border": False,
            "transfer_mechanism": "adequate_country",
            "encryption_at_rest": True,
            "access_control": True,
            "audit_logging": True,
            "framework": "GDPR",
            "compliance_status": "COMPLIANT",
            "risk_score": 15,
            "risk_category": "Low",
            "policy_results": [{"rule_id": "POL-001", "status": "PASS"}],
            "risk_factors": [{"factor": "Base", "points": 10}],
            "recommendations": ["Maintain current controls"],
            "notes": "Test case notes",
            "ml_prediction": {"predicted_status": "COMPLIANT"}
        }

        saved_id = database.save_assessment(sample_record)
        self.assertEqual(saved_id, "SOV-TEST-0001")

        retrieved = database.get_assessment("SOV-TEST-0001")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["source_org"], "Test Healthcare Clinic")
        self.assertEqual(retrieved["risk_score"], 15)
        self.assertEqual(retrieved["compliance_status"], "COMPLIANT")
        self.assertTrue(retrieved["encryption_at_rest"])
        self.assertEqual(len(retrieved["policy_results"]), 1)

    def test_dashboard_stats(self):
        sample_record = {
            "id": "SOV-TEST-0002",
            "timestamp": "2026-10-15 10:05:00 UTC",
            "source_org": "Indic Retail",
            "origin_jurisdiction": "IN",
            "data_category": "personal",
            "storage_region": "ap-south-1",
            "backup_region": "None",
            "cross_border": False,
            "transfer_mechanism": "scc",
            "encryption_at_rest": True,
            "access_control": True,
            "audit_logging": True,
            "framework": "DPDP Act 2023",
            "compliance_status": "COMPLIANT",
            "risk_score": 20,
            "risk_category": "Low",
            "policy_results": [],
            "risk_factors": [],
            "recommendations": [],
            "notes": "",
            "ml_prediction": {}
        }
        database.save_assessment(sample_record)

        stats = database.get_dashboard_stats()
        self.assertEqual(stats["total_assessments"], 1)
        self.assertEqual(stats["compliant_count"], 1)
        self.assertEqual(stats["risk_distribution"]["Low"], 1)

    def test_exports(self):
        sample_record = {
            "id": "SOV-TEST-0003",
            "timestamp": "2026-10-15 10:10:00 UTC",
            "source_org": "US FinTech",
            "origin_jurisdiction": "US_FED",
            "data_category": "financial",
            "storage_region": "us-east-1",
            "backup_region": "None",
            "cross_border": False,
            "transfer_mechanism": "scc",
            "encryption_at_rest": True,
            "access_control": True,
            "audit_logging": True,
            "framework": "PCI-DSS",
            "compliance_status": "COMPLIANT",
            "risk_score": 18,
            "risk_category": "Low",
            "policy_results": [],
            "risk_factors": [],
            "recommendations": [],
            "notes": "",
            "ml_prediction": {}
        }
        database.save_assessment(sample_record)

        json_out = database.export_assessments_json()
        self.assertIn("SOV-TEST-0003", json_out)

        csv_out = database.export_assessments_csv()
        self.assertIn("SOV-TEST-0003", csv_out)

if __name__ == "__main__":
    unittest.main()
