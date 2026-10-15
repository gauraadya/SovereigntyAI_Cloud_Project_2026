"""
Integration tests for the 6 pre-configured sample scenarios.
Ensures that each demonstration scenario evaluates to its documented expected status.
"""

import unittest
import json
import config
from policy_engine import PolicyEngine
from risk_assessment import RiskAssessmentEngine

class TestSampleScenarios(unittest.TestCase):
    def setUp(self):
        self.engine = PolicyEngine()
        with open(config.SCENARIOS_PATH, "r", encoding="utf-8") as f:
            self.scenarios = json.load(f)

    def test_scenarios_count(self):
        """Must contain at least 6 reproducible scenarios."""
        self.assertGreaterEqual(len(self.scenarios), 6)

    def test_all_scenarios_outcomes(self):
        """Verify each scenario produces its expected status."""
        for sc in self.scenarios:
            sc_id = sc["scenario_id"]
            expected = sc["expected_status"]

            payload = {
                "origin_jurisdiction": sc["origin_jurisdiction"],
                "data_category": sc["data_category"],
                "storage_region": sc["storage_region"],
                "backup_region": sc.get("backup_region", ""),
                "cross_border": sc["cross_border"],
                "transfer_mechanism": sc["transfer_mechanism"],
                "encryption_at_rest": sc["encryption_at_rest"],
                "access_control": sc["access_control"],
                "audit_logging": sc["audit_logging"],
                "framework": sc["framework"]
            }

            policy_results = self.engine.evaluate(payload)
            risk_result = RiskAssessmentEngine.calculate_risk(payload, policy_results)
            actual_status = risk_result["compliance_status"]

            self.assertEqual(
                actual_status,
                expected,
                f"Scenario {sc_id} ({sc['title']}) failed. Expected {expected}, got {actual_status}."
            )

if __name__ == "__main__":
    unittest.main()
