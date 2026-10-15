# Project Objectives

The primary objective of **SovereigntyAI** is to design, implement, and validate an autonomous prototype that evaluates whether a proposed cloud data storage or transfer scenario satisfies configurable jurisdiction-specific compliance policies, assesses potential compliance risk, explains its findings transparently, and recommends safer cloud deployment configurations.

---

## Specific Functional & Academic Objectives

### 1. Statutory Policy Engine Design & Implementation
- Model international data residency and cross-border transfer laws into structured, machine-evaluable condition trees in `policies/policy_rules.json`.
- Encode explicit rules for:
  - **European Union / EEA (GDPR):** Chapter V international transfer restrictions (Articles 44–49), Article 9 special category requirements, and Article 32 security safeguards.
  - **India (DPDP Act 2023):** Section 16 negative-list cross-border transfer principles and Section 8(5) mandatory reasonable security safeguards.
  - **United States (HIPAA / PCI-DSS):** Technical safeguards for protected health information (45 CFR § 164.312) and cryptographic standards for financial data.
- Distinguish verified legal requirements from configurable demonstration rules and simplifying assumptions.
- Ensure the engine autonomously returns `NEEDS_REVIEW` when regulatory data is ambiguous or unverified, rather than inventing conclusions.

### 2. Explainable AI (XAI) Risk-Scoring Algorithm
- Develop a deterministic risk-scoring algorithm producing a calibrated metric from 0 to 100.
- Ensure the algorithm eliminates double-counting of underlying deficiencies while modeling:
  - Intrinsic data sensitivity weights (non-personal, personal, financial, healthcare/biometric).
  - Cross-border deployment exposure.
  - Penalties for failed statutory checks.
  - Mitigation discounts for defense-in-depth controls (encryption at rest, RBAC, audit logging).
- Produce a natural-language narrative and an itemized mathematical factor waterfall explaining how the score was calculated.

### 3. Machine Learning Baseline & Empirical Evaluation
- Construct a reproducible synthetic dataset of 1,200 cross-border cloud deployment scenarios (`dataset/processed/synthetic_compliance_data.csv`).
- Train a scikit-learn pipeline classifier (`RandomForestClassifier`) to predict compliance outcomes.
- Evaluate the model on a separate 20% holdout test set using precision, recall, accuracy, and F1-score, recording genuine results in `results/model_metrics.json`.
- Provide graceful offline fallback when the model artifact is absent, ensuring the deterministic policy engine operates independently.

### 4. Interactive Full-Stack Web Application
- Build a responsive web application in Python 3 (Flask) with HTML, CSS, and vanilla JavaScript.
- Deliver an executive dashboard with fleet-wide compliance metrics, risk distribution visualizations, and recent evaluation history.
- Implement an interactive assessment form with 12 distinct input parameters, input validation, and dynamic scenario loading.
- Build a Policy Explorer enabling keyword search and filtering by jurisdiction and severity.
- Persist evaluations in SQLite with audit logging, single-assessment audit reports, and CSV/JSON export endpoints.

### 5. Enterprise Cloud Architecture Mapping
- Design a production AWS target architecture mapping application components to Amazon S3, RDS, Lambda, API Gateway, SageMaker, IAM, Cognito, CloudWatch, SNS, and QuickSight.
- Implement modular cloud service adapters in `src/aws/` that run locally without AWS credentials via local filesystem fallbacks.
- Formulate an end-to-end cloud deployment plan, IAM least-privilege security policies, and estimated monthly operational costs.

### 6. Demonstration & Academic Verification
- Provide six reproducible pre-configured demonstration scenarios covering compliant domestic storage, unauthorized sensitive transfers, compliant Indian DPDP architectures, weak security controls, secondary disaster recovery risks, and ambiguous needs-review cases.
- Develop a comprehensive test suite (22+ unit and integration tests) verifying rule logic, scoring, persistence, and APIs.
- Prepare complete viva voce examination documentation, research comparisons, and architectural diagrams.
