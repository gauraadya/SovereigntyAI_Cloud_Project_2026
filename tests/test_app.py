"""
Integration and End-to-End tests for Flask Web Application & REST APIs.
"""

import unittest
import json
import tempfile
from pathlib import Path
import os

import app as flask_app
import config
import database

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        # Configure test client with clean isolated database
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.orig_db = config.DATABASE_PATH
        config.DATABASE_PATH = Path(self.temp_db.name)
        database.init_db()

        flask_app.app.config["TESTING"] = True
        self.client = flask_app.app.test_client()

    def tearDown(self):
        config.DATABASE_PATH = self.orig_db
        self.temp_db.close()
        if os.path.exists(self.temp_db.name):
            try:
                os.remove(self.temp_db.name)
            except Exception:
                pass

    def test_dashboard_route(self):
        """Dashboard page loads successfully (HTTP 200)."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sovereignty Compliance Dashboard", response.data)

    def test_new_assessment_get(self):
        """Assessment form page loads successfully (HTTP 200)."""
        response = self.client.get("/assessment")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Cloud Data Sovereignty Compliance Assessment", response.data)

    def test_new_assessment_post(self):
        """Submitting assessment form produces evaluated result."""
        form_payload = {
            "origin_jurisdiction": "EU_EEA",
            "source_org": "EuroTest Health",
            "data_category": "personal",
            "storage_region": "eu-central-1",
            "backup_region": "eu-west-1",
            "cross_border": "false",
            "transfer_mechanism": "adequate_country",
            "encryption_at_rest": "true",
            "access_control": "true",
            "audit_logging": "true",
            "framework": "GDPR",
            "notes": "Automated unit test evaluation."
        }
        response = self.client.post("/assessment", data=form_payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"STATUS: COMPLIANT", response.data)
        self.assertIn(b"Assessment Result", response.data)

    def test_api_create_assessment(self):
        """REST API creates assessment and returns JSON 201."""
        api_payload = {
            "origin_jurisdiction": "IN",
            "source_org": "Indic API Test Client",
            "data_category": "financial",
            "storage_region": "ap-south-1",
            "backup_region": "ap-south-2",
            "cross_border": False,
            "transfer_mechanism": "scc",
            "encryption_at_rest": True,
            "access_control": True,
            "audit_logging": True,
            "framework": "DPDP Act 2023"
        }
        response = self.client.post(
            "/api/assessments",
            data=json.dumps(api_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("assessment_id", data)
        self.assertEqual(data["data"]["compliance_status"], "COMPLIANT")
        self.assertIn("risk_score", data["data"])

    def test_api_invalid_payload(self):
        """API rejects invalid jurisdiction with 400 Bad Request."""
        bad_payload = {
            "origin_jurisdiction": "INVALID_ZONE_999",
            "storage_region": "eu-central-1"
        }
        response = self.client.post(
            "/api/assessments",
            data=json.dumps(bad_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_policies_page_and_api(self):
        """Policy explorer web and API endpoints."""
        web_res = self.client.get("/policies")
        self.assertEqual(web_res.status_code, 200)

        api_res = self.client.get("/api/policies")
        self.assertEqual(api_res.status_code, 200)
        data = api_res.get_json()
        self.assertIn("rules", data)
        self.assertGreater(len(data["rules"]), 0)

    def test_export_endpoints(self):
        """CSV and JSON export endpoints."""
        csv_res = self.client.get("/export/csv")
        self.assertEqual(csv_res.status_code, 200)
        self.assertEqual(csv_res.mimetype, "text/csv")

        json_res = self.client.get("/export/json")
        self.assertEqual(json_res.status_code, 200)
        self.assertEqual(json_res.mimetype, "application/json")

if __name__ == "__main__":
    unittest.main()
