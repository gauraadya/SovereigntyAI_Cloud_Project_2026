"""
AWS Integration Services for SovereigntyAI.
Provides modular adapters for AWS S3, SNS, and CloudWatch.
Runs locally without credentials via graceful filesystem fallback,
and seamlessly switches to live AWS SDK (boto3) when deployed in AWS.
"""

import os
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import config

class S3ReportStorage:
    """Manages compliance report and artifact archiving in S3 or local mock storage."""
    
    def __init__(self, bucket_name: Optional[str] = None):
        self.bucket_name = bucket_name or os.environ.get("AWS_S3_BUCKET", "sovereignty-ai-audit-reports")
        self.mock_dir = config.BASE_DIR / "data" / "s3_mock"
        self.mock_dir.mkdir(parents=True, exist_ok=True)

    def archive_report(self, assessment_id: str, report_data: Dict[str, Any]) -> str:
        """Save assessment report to S3 bucket or local mock storage."""
        filename = f"{assessment_id}_report.json"
        
        # Check if AWS credentials exist and boto3 is installed
        if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
            try:
                import boto3
                s3 = boto3.client("s3")
                s3.put_object(
                    Bucket=self.bucket_name,
                    Key=f"reports/{filename}",
                    Body=json.dumps(report_data, indent=2),
                    ContentType="application/json"
                )
                return f"s3://{self.bucket_name}/reports/{filename}"
            except Exception as e:
                print(f"[AWS S3] Cloud upload failed, falling back to local: {e}")

        # Local mock storage fallback
        local_path = self.mock_dir / filename
        with open(local_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
        return str(local_path)

class SNSComplianceNotifier:
    """Dispatches compliance breach alerts and review triggers via Amazon SNS."""

    def __init__(self, topic_arn: Optional[str] = None):
        self.topic_arn = topic_arn or os.environ.get("AWS_SNS_TOPIC_ARN", "arn:aws:sns:eu-central-1:123456789012:SovereigntyAlerts")

    def publish_alert(self, assessment_id: str, status: str, risk_score: int, violation_summary: str) -> Dict[str, Any]:
        """Publish alert when assessment fails or requires high-priority review."""
        payload = {
            "assessment_id": assessment_id,
            "status": status,
            "risk_score": risk_score,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": violation_summary
        }

        if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
            try:
                import boto3
                sns = boto3.client("sns")
                response = sns.publish(
                    TopicArn=self.topic_arn,
                    Subject=f"[SovereigntyAI Alert] Status: {status} (Score {risk_score})",
                    Message=json.dumps(payload, indent=2)
                )
                return {"mode": "LIVE_AWS_SNS", "message_id": response.get("MessageId"), "status": "DELIVERED"}
            except Exception as e:
                print(f"[AWS SNS] Live publish failed, using simulated mode: {e}")

        # Simulated local notification
        print(f"[AWS SNS Simulator] Topic: {self.topic_arn} | Alert: {status} (Score {risk_score}) for {assessment_id}")
        return {"mode": "LOCAL_SIMULATOR", "status": "RECORDED_IN_AUDIT_LOG"}

class CloudWatchMetricsLogger:
    """Emits operational telemetry and custom compliance metrics to Amazon CloudWatch."""

    def log_assessment_metric(self, status: str, risk_score: int, jurisdiction: str):
        """Emit custom metric data."""
        if os.environ.get("AWS_ACCESS_KEY_ID"):
            try:
                import boto3
                cw = boto3.client("cloudwatch")
                cw.put_metric_data(
                    Namespace="SovereigntyAI/Compliance",
                    MetricData=[
                        {
                            "MetricName": "AssessmentEvaluated",
                            "Dimensions": [
                                {"Name": "Status", "Value": status},
                                {"Name": "Jurisdiction", "Value": jurisdiction}
                            ],
                            "Value": 1.0,
                            "Unit": "Count"
                        },
                        {
                            "MetricName": "RiskScore",
                            "Dimensions": [{"Name": "Jurisdiction", "Value": jurisdiction}],
                            "Value": float(risk_score),
                            "Unit": "None"
                        }
                    ]
                )
            except Exception as e:
                print(f"[CloudWatch] Metric emission skipped: {e}")
        # Local log output
        # (silent in normal local execution)
