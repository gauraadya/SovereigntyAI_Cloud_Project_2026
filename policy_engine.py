"""
Policy Intelligence Engine for SovereigntyAI.
Evaluates submitted cloud deployment parameters against structured, configurable rules
covering GDPR, DPDP Act 2023, HIPAA, PCI-DSS, and backup data sovereignty.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
import config

class PolicyEngine:
    """Evaluates cloud deployment configurations against compliance policies."""
    
    def __init__(self, rules_path: Path = config.POLICIES_PATH):
        self.rules_path = rules_path
        self.metadata, self.rules = self._load_rules()

    def _load_rules(self) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Load policy definitions from the JSON file."""
        if not self.rules_path.exists():
            return {}, []
        try:
            with open(self.rules_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("framework_metadata", {}), data.get("rules", [])
        except Exception as e:
            print(f"[PolicyEngine] Error loading rules: {e}")
            return {}, []

    def get_all_rules(self) -> List[Dict[str, Any]]:
        """Return all loaded policy rules."""
        return self.rules

    def get_rule_by_id(self, rule_id: str) -> Dict[str, Any]:
        """Find a single rule by its unique rule ID."""
        for r in self.rules:
            if r.get("rule_id") == rule_id:
                return r
        return {}

    def evaluate(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evaluate all applicable policy rules against the submitted deployment payload.
        Returns a list of check results with status, detailed explanation, and remediation.
        """
        results = []
        origin_jurisdiction = payload.get("origin_jurisdiction", "")
        data_category = payload.get("data_category", "personal")
        storage_region = payload.get("storage_region", "")
        backup_region = payload.get("backup_region", "")
        cross_border = bool(payload.get("cross_border", False))
        transfer_mechanism = payload.get("transfer_mechanism", "none_unverified")
        encryption_at_rest = bool(payload.get("encryption_at_rest", False))
        access_control = bool(payload.get("access_control", False))
        audit_logging = bool(payload.get("audit_logging", False))

        # Determine if destination region is native to origin jurisdiction
        jurisdiction_info = config.JURISDICTIONS.get(origin_jurisdiction, {})
        native_regions = jurisdiction_info.get("native_regions", [])
        storage_region_info = config.AWS_REGIONS.get(storage_region, {})
        destination_jurisdiction = storage_region_info.get("jurisdiction", "GLOBAL_OTHER")

        is_destination_native = storage_region in native_regions
        
        # Cross-border inference: if destination is not in native regions, cross-border is effectively active
        effective_cross_border = cross_border or (len(native_regions) > 0 and not is_destination_native)

        for rule in self.rules:
            rule_id = rule["rule_id"]
            app_cats = rule.get("applicable_categories", [])
            rule_jurisdiction = rule.get("jurisdiction", "GLOBAL_OTHER")
            
            # Check applicability
            if app_cats and data_category not in app_cats:
                results.append({
                    "rule_id": rule_id,
                    "rule_name": rule["rule_name"],
                    "framework": rule["framework"],
                    "severity": rule["severity"],
                    "rule_type": rule.get("rule_type", "DEMONSTRATION_RULE"),
                    "status": "SKIPPED",
                    "explanation": f"Rule not applicable to data category '{data_category}'.",
                    "remediation": "N/A",
                    "legal_reference": rule.get("legal_reference", ""),
                    "reference_url": rule.get("reference_url", "")
                })
                continue

            # Evaluate individual rules
            status = "PASS"
            explanation = rule.get("explanation_pass", "")
            remediation = rule.get("remediation", "")

            # POL-GDPR-001: Chapter V International Transfers
            if rule_id == "POL-GDPR-001":
                if origin_jurisdiction == "EU_EEA":
                    if effective_cross_border and not is_destination_native:
                        if transfer_mechanism == "none_unverified":
                            status = "FAIL"
                            explanation = (
                                f"Data originating in EU/EEA is configured for storage in non-EEA region '{storage_region}' "
                                f"without a verified Article 45 Adequacy Decision, Article 46 SCCs, or BCR."
                            )
                        elif transfer_mechanism in ["adequate_country", "scc", "bcr", "explicit_consent", "statutory_exemption"]:
                            status = "PASS"
                            explanation = (
                                f"Cross-border transfer from EU/EEA to '{storage_region}' is safeguarded by "
                                f"verified transfer mechanism '{config.TRANSFER_MECHANISMS.get(transfer_mechanism, transfer_mechanism)}'."
                            )
                    else:
                        status = "PASS"
                        explanation = f"Storage region '{storage_region}' is located within the EU/EEA. Intra-EEA transfer principles apply."
                else:
                    status = "SKIPPED"
                    explanation = f"Rule only triggers for EU/EEA origin; current origin is '{origin_jurisdiction}'."

            # POL-GDPR-002: Article 9 Special Category Data
            elif rule_id == "POL-GDPR-002":
                if origin_jurisdiction == "EU_EEA" and data_category in ["sensitive_personal", "healthcare"]:
                    if effective_cross_border and not is_destination_native:
                        missing = []
                        if not encryption_at_rest:
                            missing.append("encryption at rest")
                        if not access_control:
                            missing.append("least-privilege access control")
                        if not audit_logging:
                            missing.append("audit logging")
                        if transfer_mechanism == "none_unverified":
                            missing.append("verified transfer mechanism")

                        if missing:
                            status = "FAIL"
                            explanation = (
                                f"Special category ({data_category}) data transferred outside EEA lacks essential "
                                f"supplementary measures mandated under EDPB Recommendations 01/2020: {', '.join(missing)}."
                            )
                        else:
                            status = "PASS"
                            explanation = (
                                f"Special category ({data_category}) data satisfies enhanced technical and contractual safeguards."
                            )
                    else:
                        # Local EEA storage
                        if not (encryption_at_rest and access_control):
                            status = "NEEDS_REVIEW"
                            explanation = "Special category data inside EEA should maintain encryption and access controls under Article 32."
                        else:
                            status = "PASS"
                            explanation = "Special category data stored within EEA with encryption and access controls."
                else:
                    status = "SKIPPED"
                    explanation = "Applicable only to EU/EEA special category or healthcare data."

            # POL-DPDP-001: India Section 16 Cross-border Transfer
            elif rule_id == "POL-DPDP-001":
                if origin_jurisdiction == "IN":
                    if effective_cross_border and not is_destination_native:
                        if transfer_mechanism == "none_unverified":
                            status = "FAIL"
                            explanation = (
                                f"Data originating in India is proposed for transfer to foreign region '{storage_region}' "
                                "without documented bilateral agreement, transfer mechanism, or validated authorization."
                            )
                        else:
                            status = "PASS"
                            explanation = (
                                f"Transfer outside India to '{storage_region}' is covered by mechanism "
                                f"'{config.TRANSFER_MECHANISMS.get(transfer_mechanism, transfer_mechanism)}'."
                            )
                    else:
                        status = "PASS"
                        explanation = f"Data remains hosted within Indian AWS sovereign region '{storage_region}'."
                else:
                    status = "SKIPPED"
                    explanation = f"Applies to India data origin; current origin is '{origin_jurisdiction}'."

            # POL-DPDP-002: India Section 8 Reasonable Security Safeguards
            elif rule_id == "POL-DPDP-002":
                if origin_jurisdiction == "IN":
                    missing = []
                    if not encryption_at_rest:
                        missing.append("encryption at rest")
                    if not access_control:
                        missing.append("access controls")
                    if missing:
                        status = "FAIL"
                        explanation = (
                            f"Violation of DPDP Act 2023 Sec 8(5): Data Fiduciary failed to configure reasonable security safeguards: {', '.join(missing)}."
                        )
                    else:
                        status = "PASS"
                        explanation = "Reasonable security safeguards (encryption and access control) are active per Section 8(5)."
                else:
                    status = "SKIPPED"
                    explanation = "Applies to India data fiduciary obligations."

            # POL-US-HIPAA-001: HIPAA Security Rule Technical Safeguards
            elif rule_id == "POL-US-HIPAA-001":
                if data_category == "healthcare":
                    missing = []
                    if not encryption_at_rest:
                        missing.append("encryption at rest (45 CFR § 164.312(a)(2)(iv))")
                    if not access_control:
                        missing.append("unique user access control (45 CFR § 164.312(a)(1))")
                    if not audit_logging:
                        missing.append("hardware/software audit controls (45 CFR § 164.312(b))")
                    if missing:
                        status = "FAIL"
                        explanation = f"Healthcare data configuration lacks HIPAA technical safeguards: {'; '.join(missing)}."
                    else:
                        status = "PASS"
                        explanation = "Meets HIPAA technical safeguards requirements (encryption, access control, audit controls)."
                else:
                    status = "SKIPPED"
                    explanation = "Applicable strictly to Protected Health Information (PHI)."

            # POL-FIN-PCI-001: Financial Data Cryptographic Safeguards
            elif rule_id == "POL-FIN-PCI-001":
                if data_category == "financial":
                    missing = []
                    if not encryption_at_rest:
                        missing.append("encryption at rest")
                    if not audit_logging:
                        missing.append("audit trail logging")
                    if missing:
                        status = "FAIL"
                        explanation = f"Financial data repository lacks critical controls: {', '.join(missing)}."
                    else:
                        status = "PASS"
                        explanation = "Financial data is secured with encryption at rest and audit logging."
                else:
                    status = "SKIPPED"
                    explanation = "Applicable only to financial and cardholder data."

            # POL-BACKUP-001: Disaster Recovery Backup Sovereignty Alignment
            elif rule_id == "POL-BACKUP-001":
                if backup_region:
                    backup_info = config.AWS_REGIONS.get(backup_region, {})
                    backup_jurisdiction = backup_info.get("jurisdiction", "GLOBAL_OTHER")
                    
                    if origin_jurisdiction in ["EU_EEA", "IN"] and backup_jurisdiction != origin_jurisdiction:
                        if transfer_mechanism == "none_unverified":
                            status = "FAIL"
                            explanation = (
                                f"Disaster recovery backup region '{backup_region}' ({backup_jurisdiction}) is in a different "
                                f"jurisdiction from data origin '{origin_jurisdiction}' with no verified transfer mechanism."
                            )
                        else:
                            status = "NEEDS_REVIEW"
                            explanation = (
                                f"Backup region '{backup_region}' involves cross-jurisdiction replication. Verify that backup "
                                "snapshots are encrypted with separate regional KMS keys."
                            )
                    else:
                        status = "PASS"
                        explanation = f"Backup region '{backup_region}' aligns with primary sovereignty domain."
                else:
                    status = "PASS"
                    explanation = "No secondary cross-region backup configured."

            # POL-SEC-LOG-001: Continuous Audit Logging
            elif rule_id == "POL-SEC-LOG-001":
                if not audit_logging and data_category != "non_personal":
                    status = "FAIL"
                    explanation = "Audit logging is disabled for personal/regulated workload, impeding compliance forensics and non-repudiation."
                else:
                    status = "PASS"
                    explanation = "Audit logging is actively configured for the deployment."

            # POL-NONPERS-001: Non-personal Data Exemption
            elif rule_id == "POL-NONPERS-001":
                if data_category == "non_personal":
                    status = "PASS"
                    explanation = "Non-personal technical/telemetry data is exempt from personal data residency restrictions."
                else:
                    status = "SKIPPED"
                    explanation = "Applies only to non-personal telemetry data."

            # POL-AMBIG-001: Ambiguous Jurisdiction & Incomplete Specification
            elif rule_id == "POL-AMBIG-001":
                if effective_cross_border and transfer_mechanism == "none_unverified":
                    status = "NEEDS_REVIEW"
                    explanation = (
                        "Cross-border deployment has unverified or undocumented transfer mechanisms. "
                        "Automated compliance requires qualified human legal review."
                    )
                else:
                    status = "PASS"
                    explanation = "Transfer mechanism and jurisdiction parameters are documented."

            results.append({
                "rule_id": rule_id,
                "rule_name": rule["rule_name"],
                "framework": rule["framework"],
                "severity": rule["severity"],
                "rule_type": rule.get("rule_type", "DEMONSTRATION_RULE"),
                "status": status,
                "explanation": explanation,
                "remediation": remediation,
                "legal_reference": rule.get("legal_reference", ""),
                "reference_url": rule.get("reference_url", "")
            })

        return results
