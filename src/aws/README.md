# AWS Cloud Services Module (`src/aws`)

This directory houses the modular cloud service adapters that enable SovereigntyAI to interact with live Amazon Web Services resources when cloud credentials are configured, while maintaining graceful local filesystem fallbacks when operating offline.

## Components
- **`aws_services.py`:** Contains:
  - `S3ReportStorage`: Archives assessment reports to an Amazon S3 bucket (`s3://...`) or local fallback directory (`data/s3_mock/`).
  - `SNSComplianceNotifier`: Broadcasts high-severity compliance alerts to an Amazon SNS topic or simulated local log.
  - `CloudWatchMetricsLogger`: Emits custom compliance metrics (`AssessmentEvaluated`, `RiskScore`) to Amazon CloudWatch.
- **`__init__.py`:** Exports the adapter classes.

For complete cloud service mapping and architecture diagrams, see `architecture/AWS_Architecture.md` and `docs/AWS_Services.md`.
