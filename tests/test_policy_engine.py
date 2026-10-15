"""
Unit tests for Policy Intelligence Engine.
Tests evaluation of GDPR, DPDP Act 2023, HIPAA, PCI-DSS, and backup rules.
"""

import unittest
from policy_engine import PolicyEngine

class TestPolicyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PolicyEngine()

    def test_rules_loaded(self):
        """Ensure policy rules are loaded successfully from JSON."""
        rules = self.engine.get_all_rules()
        self.assertGreater(len(rules), 0, "Policy rules list should not be empty")

    def test_gdpr_intra_eea_pass(self):
        """GDPR compliant when storage region is inside the EEA."""
        payload = {
            "origin_jurisdiction": "EU_EEA",
            "data_category": "personal",
            "storage_region": "eu-central-1",
            "cross_border": False,
            "transfer_mechanism": "none_unverified",
            "encryption_at_rest": True,
            "access_control": True,
            "audit_logging": True
        }
        results = self.engine.evaluate(payload)
        gdpr_rule = next((r for r in results if r["rule_id"] == "POL-GDPR-001"), None)
        self.assertIsNotNone(gdpr_rule)
        self.assertEqual(gdpr_rule["status"], "PASS")

    def test_gdpr_cross_border_fail_without_mechanism(self):
        """GDPR fails when transferring to non-EEA region without transfer mechanism."""
        payload = {
            "origin_jurisdiction": "EU_EEA",
            "data_category": "personal",
            "storage_region": "us-east-1",
            "cross_border": True,
            "transfer_mechanism": "none_unverified",
            "encryption_at_rest": True,
            "access_control": True,
            "audit_logging": True
        }
        results = self.engine.evaluate(payload)
        gdpr_rule = next((r for r in results if r["rule_id"] == "POL-GDPR-001"), None)
        self.assertIsNotNone(gdpr_rule)
        self.assertEqual(gdpr_rule["status"], "FAIL")

    def test_gdpr_cross_border_pass_with_scc(self):
        """GDPR passes when transferring outside EEA with Standard Contractual Clauses (SCCs)."""
        payload = {
            "origin_jurisdiction": "EU_EEA",
            "data_category": "personal",
            "storage_region": "us-east-1",
            "cross_border": True,
            "transfer_mechanism": "scc",
            "encryption_at_rest": True,
            "access_control": True,
            "audit_logging": True
        }
        results = self.engine.evaluate(payload)
        gdpr_rule = next((r for r in results if r["rule_id"] == "POL-GDPR-001"), None)
        self.assertIsNotNone(gdpr_rule)
        self.assertEqual(gdpr_rule["status"], "PASS")

    def test_dpdp_act_sec_8_security_safeguard_failure(self):
        """India DPDP Act Section 8(5) fails when reasonable security safeguards are disabled."""
        payload = {
            "origin_jurisdiction": "IN",
            "data_category": "personal",
            "storage_region": "ap-south-1",
            "cross_border": False,
            "transfer_mechanism": "none_unverified",
            "encryption_at_rest": False,  # Missing encryption
            "access_control": True,
            "audit_logging": True
        }
        results = self.engine.evaluate(payload)
        sec8_rule = next((r for r in results if r["rule_id"] == "POL-DPDP-002"), None)
        self.assertIsNotNone(sec8_rule)
        self.assertEqual(sec8_rule["status"], "FAIL")

    def test_hipaa_healthcare_technical_safeguard_failure(self):
        """Healthcare data without audit logging fails HIPAA technical safeguards."""
        payload = {
            "origin_jurisdiction": "US_FED",
            "data_category": "healthcare",
            "storage_region": "us-east-1",
            "cross_border": False,
            "transfer_mechanism": "none_unverified",
            "encryption_at_rest": True,
            "access_control": True,
            "audit_logging": False  # Missing audit logging
        }
        results = self.engine.evaluate(payload)
        hipaa_rule = next((r for r in results if r["rule_id"] == "POL-US-HIPAA-001"), None)
        self.assertIsNotNone(hipaa_rule)
        self.assertEqual(hipaa_rule["status"], "FAIL")

    def test_non_personal_data_exemption(self):
        """Non-personal data rule PASSES indicating free flow of telemetry."""
        payload = {
            "origin_jurisdiction": "EU_EEA",
            "data_category": "non_personal",
            "storage_region": "us-east-1",
            "cross_border": True,
            "transfer_mechanism": "none_unverified",
            "encryption_at_rest": False,
            "access_control": False,
            "audit_logging": False
        }
        results = self.engine.evaluate(payload)
        nonpers_rule = next((r for r in results if r["rule_id"] == "POL-NONPERS-001"), None)
        self.assertIsNotNone(nonpers_rule)
        self.assertEqual(nonpers_rule["status"], "PASS")

if __name__ == "__main__":
    unittest.main()
