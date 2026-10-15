"""
Explainable Risk Assessment Engine for SovereigntyAI.
Calculates a deterministic risk score (0-100) with a transparent point breakdown,
determines compliance status, avoids double-counting, and generates actionable recommendations.
"""

from typing import Dict, Any, List, Tuple
import config

class RiskAssessmentEngine:
    """Calculates risk scores, categorizes risk, and produces explainable rationales."""

    @staticmethod
    def calculate_risk(payload: Dict[str, Any], policy_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute deterministic risk evaluation.
        Returns:
            - risk_score: int (0 to 100)
            - risk_category: str ('Low', 'Moderate', 'High', 'Critical')
            - compliance_status: str ('COMPLIANT', 'NON_COMPLIANT', 'NEEDS_REVIEW')
            - factors: List[Dict] (contributing factors with points)
            - recommendations: List[str]
            - suggested_next_steps: List[str]
            - calculation_narrative: str (detailed walkthrough of the formula)
        """
        data_cat = payload.get("data_category", "personal")
        cross_border = bool(payload.get("cross_border", False))
        transfer_mechanism = payload.get("transfer_mechanism", "none_unverified")
        encryption_at_rest = bool(payload.get("encryption_at_rest", False))
        access_control = bool(payload.get("access_control", False))
        audit_logging = bool(payload.get("audit_logging", False))
        storage_region = payload.get("storage_region", "")
        backup_region = payload.get("backup_region", "")
        origin_jurisdiction = payload.get("origin_jurisdiction", "")

        factors = []
        raw_score = 0

        # 1. Baseline Risk from Data Sensitivity
        cat_meta = config.DATA_CATEGORIES.get(data_cat, {})
        base_points = cat_meta.get("sensitivity_weight", 15)
        raw_score += base_points
        factors.append({
            "factor": f"Data Sensitivity: {cat_meta.get('label', data_cat)}",
            "impact": f"+{base_points}",
            "points": base_points,
            "type": "BASE_SENSITIVITY",
            "description": f"Baseline exposure inherent to {data_cat} records."
        })

        # 2. Cross-Border Deployment Penalty
        if cross_border:
            if transfer_mechanism == "none_unverified":
                cb_points = 25
                raw_score += cb_points
                factors.append({
                    "factor": "Unverified Cross-Border Transfer",
                    "impact": f"+{cb_points}",
                    "points": cb_points,
                    "type": "CROSS_BORDER_RISK",
                    "description": "Data leaves home jurisdiction without a legally binding transfer mechanism."
                })
            elif transfer_mechanism in ["adequate_country", "scc", "bcr"]:
                cb_points = 5
                raw_score += cb_points
                factors.append({
                    "factor": "Governed Cross-Border Transfer",
                    "impact": f"+{cb_points}",
                    "points": cb_points,
                    "type": "CROSS_BORDER_RISK",
                    "description": "Cross-border data movement managed with verified legal instruments."
                })

        # 3. Policy Rule Failure Penalties
        failed_critical = 0
        failed_high = 0
        failed_medium = 0
        needs_review_count = 0

        for check in policy_results:
            status = check.get("status")
            severity = check.get("severity")
            rule_id = check.get("rule_id")

            if status == "FAIL":
                if severity == "CRITICAL":
                    penalty = 30
                    failed_critical += 1
                elif severity == "HIGH":
                    penalty = 20
                    failed_high += 1
                elif severity == "MEDIUM":
                    penalty = 10
                    failed_medium += 1
                else:
                    penalty = 5

                raw_score += penalty
                factors.append({
                    "factor": f"Policy Failure: {rule_id} ({check.get('rule_name')})",
                    "impact": f"+{penalty}",
                    "points": penalty,
                    "type": "POLICY_VIOLATION",
                    "description": check.get("explanation")
                })
            elif status == "NEEDS_REVIEW":
                needs_review_count += 1
                raw_score += 10
                factors.append({
                    "factor": f"Review Required: {rule_id}",
                    "impact": "+10",
                    "points": 10,
                    "type": "GOVERNANCE_REVIEW",
                    "description": check.get("explanation")
                })

        # 4. Security Mitigations / Credits (up to 30 points discount)
        mitigation_credits = 0
        if encryption_at_rest:
            credit = 10
            mitigation_credits += credit
            factors.append({
                "factor": "Mitigation: Encryption at Rest Enabled",
                "impact": f"-{credit}",
                "points": -credit,
                "type": "SECURITY_CREDIT",
                "description": "Cryptographic protection at rest diminishes unauthorized exposure vectors."
            })
        else:
            penalty = 15
            raw_score += penalty
            factors.append({
                "factor": "Deficiency: Plaintext Storage (No Encryption)",
                "impact": f"+{penalty}",
                "points": penalty,
                "type": "SECURITY_DEFICIENCY",
                "description": "Storage volumes and buckets are unencrypted."
            })

        if access_control:
            credit = 8
            mitigation_credits += credit
            factors.append({
                "factor": "Mitigation: Least-Privilege Access Controls",
                "impact": f"-{credit}",
                "points": -credit,
                "type": "SECURITY_CREDIT",
                "description": "Role-based access enforcement reduces insider and perimeter breach risk."
            })
        else:
            penalty = 10
            raw_score += penalty
            factors.append({
                "factor": "Deficiency: Missing Access Controls",
                "impact": f"+{penalty}",
                "points": penalty,
                "type": "SECURITY_DEFICIENCY",
                "description": "Permissive or default access policies in effect."
            })

        if audit_logging:
            credit = 7
            mitigation_credits += credit
            factors.append({
                "factor": "Mitigation: Continuous Audit Logging",
                "impact": f"-{credit}",
                "points": -credit,
                "type": "SECURITY_CREDIT",
                "description": "Immutable forensic trail via CloudTrail and CloudWatch."
            })
        else:
            penalty = 8
            raw_score += penalty
            factors.append({
                "factor": "Deficiency: Logging Disabled",
                "impact": f"+{penalty}",
                "points": penalty,
                "type": "SECURITY_DEFICIENCY",
                "description": "Lack of tamper-evident audit logging impairs regulatory inspection."
            })

        # Apply mitigations
        net_score = raw_score - mitigation_credits

        # Compliance status determination
        if failed_critical > 0 or failed_high > 1 or (failed_high >= 1 and (not encryption_at_rest or not access_control)):
            compliance_status = config.STATUS_NON_COMPLIANT
            # If non-compliant due to severe violations, floor score at 55 so it cannot appear low-risk
            if net_score < 55:
                net_score = 55
        elif failed_high == 1 or needs_review_count > 0 or (transfer_mechanism == "none_unverified" and cross_border):
            compliance_status = config.STATUS_NEEDS_REVIEW
            if net_score < 30:
                net_score = 30
        else:
            compliance_status = config.STATUS_COMPLIANT

        # Clamp between 0 and 100
        final_score = max(0, min(100, int(round(net_score))))

        # Determine risk band
        risk_category = "Low"
        for band_name, band_range in config.RISK_BANDS.items():
            if band_range["min"] <= final_score <= band_range["max"]:
                risk_category = band_name
                break

        # Generate Actionable Recommendations based on findings
        recommendations = []
        suggested_next_steps = []

        if not encryption_at_rest:
            recommendations.append(
                "Enable AWS KMS customer-managed key encryption (SSE-KMS) for all primary and backup storage assets."
            )
        if not access_control:
            recommendations.append(
                "Enforce AWS IAM least-privilege role boundaries, disable public access block, and require MFA for administrative roles."
            )
        if not audit_logging:
            recommendations.append(
                "Activate AWS CloudTrail multi-region trails and stream management/data events to a dedicated CloudWatch Log Group."
            )

        if cross_border and transfer_mechanism == "none_unverified":
            if origin_jurisdiction == "EU_EEA":
                recommendations.append(
                    "Execute European Commission Standard Contractual Clauses (SCCs) and complete a Transfer Impact Assessment (TIA)."
                )
            elif origin_jurisdiction == "IN":
                recommendations.append(
                    "Review bilateral contracts with recipient entities and verify whether the destination country is on any restricted list."
                )
            else:
                recommendations.append(
                    "Establish a formal data transfer agreement specifying jurisdiction, purpose limitations, and security standards."
                )

        if backup_region:
            backup_meta = config.AWS_REGIONS.get(backup_region, {})
            if backup_meta.get("jurisdiction") != origin_jurisdiction and origin_jurisdiction in ["EU_EEA", "IN"]:
                recommendations.append(
                    f"Consider relocating backup snapshots from '{backup_region}' to a native sovereign region (e.g., ap-south-2 for India, or eu-central-1 for EU)."
                )

        if compliance_status == config.STATUS_COMPLIANT and not recommendations:
            recommendations.append("Maintain current operational posture and schedule recurring quarterly sovereignty audits.")

        # Suggested next steps
        if compliance_status == config.STATUS_NON_COMPLIANT:
            suggested_next_steps = [
                "Halt cross-border deployment pipelines until critical policy failures are remediated.",
                "Review the specific failed policy rules shown in the evaluation table.",
                "Implement recommended cryptographic controls and update regional storage configurations."
            ]
        elif compliance_status == config.STATUS_NEEDS_REVIEW:
            suggested_next_steps = [
                "Schedule a review meeting with legal/compliance officers regarding the transfer mechanism.",
                "Perform a documented Transfer Impact Assessment (TIA) for the destination AWS region.",
                "Verify whether customer consent or contractual safeguards satisfy statutory exceptions."
            ]
        else:
            suggested_next_steps = [
                "Export this assessment record to JSON/CSV for your compliance audit repository.",
                "Deploy CloudFormation / Terraform infrastructure adhering to the evaluated configuration.",
                "Enable continuous compliance monitoring via AWS Config and CloudWatch alarms."
            ]

        # Detailed calculation narrative
        calculation_narrative = (
            f"The final risk score of {final_score}/100 ({risk_category} Risk) was computed deterministically: "
            f"Starting with a baseline sensitivity weight of {base_points} points for {data_cat} data, "
            f"adding policy and deficiency penalties totaling {raw_score - base_points} points, "
            f"and crediting {mitigation_credits} points for active security controls (encryption, access control, audit logging). "
            f"Status '{compliance_status}' was designated based on "
            f"{failed_critical} critical rule violations, {failed_high} high severity violations, and {needs_review_count} pending reviews."
        )

        return {
            "risk_score": final_score,
            "risk_category": risk_category,
            "compliance_status": compliance_status,
            "risk_factors": factors,
            "recommendations": recommendations,
            "suggested_next_steps": suggested_next_steps,
            "calculation_narrative": calculation_narrative
        }
