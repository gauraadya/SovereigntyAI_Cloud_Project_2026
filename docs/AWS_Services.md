# AWS Services Integration & Cloud Architecture Blueprint

## 1. Overview

SovereigntyAI is designed with a modular architecture that separates business logic from cloud infrastructure providers. While the current prototype runs locally using Python 3 and SQLite for offline college course evaluation, it provides drop-in modular adapters for **ten key Amazon Web Services (AWS)** products.

---

## 2. Detailed Service Mappings & Implementations

### 1. Amazon S3 (Simple Storage Service)
- **Production Role:** Secure object storage repository for evaluated audit reports, exported compliance datasets, and version-controlled policy rule files.
- **Security & Sovereignty Controls:** S3 buckets must be configured with:
  - SSE-KMS (Server-Side Encryption with Customer-Managed Keys).
  - S3 Block Public Access enabled at the account and bucket levels.
  - S3 Object Lock (WORM compliance) to prevent tampering with historical audit trails.
- **Local Implementation:** Abstracted in `src/aws/aws_services.py` (`S3ReportStorage`). When AWS credentials are not configured, reports are archived as structured JSON files in `data/s3_mock/`. When deployed on AWS with `boto3`, it automatically executes `s3.put_object()`.

### 2. Amazon RDS (Relational Database Service - PostgreSQL)
- **Production Role:** Managed multi-AZ relational database storing assessments, organizational profiles, and historical audit trails.
- **Security Controls:** Encrypted with KMS, deployed across private subnets, with automated backups retained within the sovereign region.
- **Local Implementation:** Implemented with Python's built-in `sqlite3` in `database.py`. The table schema matches production PostgreSQL types directly (`TEXT`, `INTEGER`, `JSON`).

### 3. AWS Lambda
- **Production Role:** Serverless compute layer executing event-driven policy checks. When a Terraform or CloudFormation template is pushed, a Lambda function triggers `policy_engine.py` to validate regional compliance before resources are provisioned.
- **Execution Pattern:** Python 3.11/3.12 runtime with container image or Lambda layer containing `scikit-learn` and `joblib`.
- **Local Implementation:** Direct in-process execution via Flask routes (`/assessment` and `/api/assessments`).

### 4. Amazon API Gateway
- **Production Role:** Managed HTTP/REST API gateway providing SSL/TLS 1.3 termination, request validation, API throttling (e.g. 100 requests/sec per tenant), and routing to Lambda microservices.
- **Local Implementation:** Handled natively by Flask URL routing and error handlers in `app.py`.

### 5. Amazon SageMaker
- **Production Role:** Managed ML platform used for training, evaluating, and hosting the advisory compliance baseline model.
  - **SageMaker Training Jobs:** Replaces `scripts/train_ml_model.py` with scheduled retraining on newly recorded compliance audit logs.
  - **SageMaker Serverless Inference:** Hosts the `RandomForestClassifier` pipeline endpoint, scaling to zero when idle to minimize costs.
- **Local Implementation:** Local execution using `joblib` and `scikit-learn` via `ai_services.py` with zero cloud billing.

### 6. AWS IAM (Identity and Access Management)
- **Production Role:** Enforces least-privilege service roles. Grants Lambda execution roles permission only to write to designated S3 audit prefixes and publish to the specific SNS compliance topic.
- **Local Implementation:** Verified via software configuration flags (`access_control: true/false`) and documented least-privilege JSON policies in `architecture/AWS_Architecture.md`.

### 7. Amazon Cognito
- **Production Role:** Managed user pool providing authentication and role-based access control (RBAC) for compliance officers, enterprise auditors, and DevOps engineers, supporting multi-factor authentication (MFA) and SAML/OIDC enterprise federation.
- **Local Implementation:** Open academic session layer designed for single-user offline evaluation and demonstration.

### 8. Amazon CloudWatch
- **Production Role:** Centralized operational monitoring and alarm system:
  - **CloudWatch Logs:** Ingests application and access logs with retention policies.
  - **CloudWatch Custom Metrics:** Tracks `AssessmentEvaluated`, `NonCompliantViolations`, and `AverageRiskScore` under the `SovereigntyAI/Compliance` namespace.
  - **CloudWatch Alarms:** Automatically notifies engineers if non-compliant deployments spike.
- **Local Implementation:** Formatted log outputs and telemetry stubs in `src/aws/aws_services.py` (`CloudWatchMetricsLogger`).

### 9. Amazon SNS (Simple Notification Service)
- **Production Role:** Push-based messaging service broadcasting high-priority security notifications when a critical policy breach (`STATUS_NON_COMPLIANT`) is detected. Sends alerts via SMS, email, or Slack/PagerDuty webhooks.
- **Local Implementation:** Simulated notification dispatcher in `src/aws/aws_services.py` (`SNSComplianceNotifier`) that outputs alert events to the terminal console and SQLite audit log.

### 10. Amazon QuickSight
- **Production Role:** Serverless Business Intelligence (BI) service connecting directly to Amazon RDS to build interactive executive dashboards, visualizing geographical compliance heatmaps, risk score trends, and framework distributions.
- **Local Implementation:** Handled in the local application by the HTML5/CSS3 Dashboard with live SVG dials and CSS risk distribution bars in `templates/index.html`.

---

## 3. Cloud Migration Roadmap

```text
Local Prototype (Phase 1)
  ↓
Docker Containerization (Phase 2: Dockerfile created)
  ↓
AWS ECS Fargate / Lambda Deployment (Phase 3: AWS CDK / Terraform)
  ↓
Amazon RDS PostgreSQL Migration (Phase 4: SQLite data export)
  ↓
Continuous CI/CD Compliance Gate (Phase 5: GitHub Actions + AWS CodePipeline)
```
