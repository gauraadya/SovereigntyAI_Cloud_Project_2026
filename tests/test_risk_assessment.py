"""
Unit tests for Risk Assessment Engine.
Tests risk score bounds, mitigation credits, factor breakdown, and compliance status.
"""

import unittest
from risk_assessment import RiskAssessmentEngine
import config

class TestRiskAssessment(unittest.TestCase):
    def test_score_bounds(self):
        """Risk score must always reside between 0 and 100."""
        payload = {
            "origin_jurisdiction": "EU_EEA",
            "data_category": "healthcare",
            "storage_region": "us-east-1",
            "cross_border": True,
            "transfer_mechanism": "none_unverified",
            "encryption_at_rest": False,
            "access_control": False,
            "audit_logging": False
        }
        mock_policy_results = [
            {"rule_id": "POL-GDPR-001", "status": "FAIL", "severity": "CRITICAL", "rule_name": "GDPR Chapter V", "explanation": "Failed"},
            {"rule_id": "POL-GDPR-002", "status": "FAIL", "severity": "CRITICAL", "rule_name": "Special Category", "explanation": "Failed"}
        ]
        result = RiskAssessmentEngine.calculate_risk(payload, mock_policy_results)
        self.assertGreaterEqual(result["risk_score"], 0)
        self.assertLessEqual(result["risk_score"], 100)
        self.assertEqual(result["risk_category"], "Critical")
        self.assertEqual(result["compliance_status"], config.STATUS_NON_COMPLIANT)

    def test_compliant_low_risk(self):
        """Low risk score achieved with strong mitigations and no policy violations."""
        payload = {
            "origin_jurisdiction": "EU_EEA",
            "data_category": "personal",
            "storage_region": "eu-central-1",
            "cross_border": False,
            "transfer_mechanism": "adequate_country",
            "encryption_at_rest": True,
            "access_control": True,
            "audit_logging": True
        }
        mock_policy_results = [
            {"rule_id": "POL-GDPR-001", "status": "PASS", "severity": "CRITICAL", "rule_name": "GDPR", "explanation": "Passed"}
        ]
        result = RiskAssessmentEngine.calculate_risk(payload, mock_policy_results)
        self.assertLessEqual(result["risk_score"], 25)
        self.assertEqual(result["compliance_status"], config.STATUS_COMPLIANT)
        self.assertEqual(result["risk_category"], "Low")

    def test_explainable_narrative_present(self):
        """Result must contain explainable narrative and itemized factors."""
        payload = {
            "origin_jurisdiction": "IN",
            "data_category": "financial",
            "storage_region": "ap-south-1",
            "cross_border": False,
            "transfer_mechanism": "scc",
            "encryption_at_rest": True,
            "access_control": True,
            "audit_logging": True
        }
        result = RiskAssessmentEngine.calculate_risk(payload, [])
        self.assertIn("calculation_narrative", result)
        self.assertTrue(len(result["risk_factors"]) > 0)
        self.assertIn("suggested_next_steps", result)

if __name__ == "__main__":
    unittest.main()
