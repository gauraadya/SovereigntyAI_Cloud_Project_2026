# SovereigntyAI

**Autonomous Cloud Data Sovereignty Compliance Framework for Cross-Border Cloud Applications using Policy Intelligence and Explainable AI**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask 3.0+](https://img.shields.io/badge/framework-Flask_3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests: 22 Passed](https://img.shields.io/badge/tests-22%20passed-brightgreen.svg)](docs/Testing_Report.md)
[![Academic Project](https://img.shields.io/badge/course-Cloud_Computing_Capstone_2026-orange.svg)](docs/Project_Report.md)

---

## 1. Project Overview

**SovereigntyAI** is an autonomous, explainable cloud data sovereignty compliance framework designed for multi-region and cross-border enterprise cloud applications. Operating primarily on Amazon Web Services (AWS) architectural paradigms, the system evaluates whether a proposed cloud data storage, processing, or replication scenario satisfies complex, jurisdiction-specific regulatory policies (including **EU GDPR**, **India DPDP Act 2023**, and **US HIPAA / PCI-DSS**).

The framework pairs a **deterministic statutory policy engine** with an **explainable AI (XAI) risk-scoring algorithm** and an **advisory machine learning baseline** (`RandomForestClassifier`, 96.25% test accuracy). It eliminates the risks of generative AI hallucinations while delivering a transparent, mathematical factor breakdown and actionable AWS remediation recommendations.

SovereigntyAI runs **100% locally and offline** without requiring paid cloud resources, external API keys, or active AWS credentials, while providing modular adapters ready for production cloud deployment.

---

## 2. Problem Statement

Public hyperscale cloud providers (AWS, Azure, GCP) operate globally distributed infrastructures with shared control planes and automated cross-region replication. Conversely, modern legal frameworks enforce territorial digital sovereignty:
- **EU GDPR Chapter V (Articles 44–49):** Strictly conditions data transfers outside the European Economic Area on adequacy decisions, Standard Contractual Clauses (SCCs), or Binding Corporate Rules (BCRs).
- **India DPDP Act 2023 (Sections 8 & 16):** Regulates cross-border data flows via a negative-list approach and mandates reasonable security safeguards.
- **US Healthcare & Finance (HIPAA / PCI-DSS):** Enforces mandatory technical safeguards including encryption at rest and audit logging.

Existing Cloud Security Posture Management (CSPM) tools detect technical flaws (e.g., unencrypted buckets) but fail to evaluate international transfer legality or secondary disaster recovery backup risks. Meanwhile, generative LLMs suffer from legal hallucinations, non-determinism, and data leakage risks.

---

## 3. Proposed Solution

SovereigntyAI resolves this dilemma through a hybrid architecture:
1. **Deterministic Statutory Rules:** Condition trees grounded directly in verified statutory text and EDPB guidelines.
2. **Explainable AI (XAI) Risk Algorithm:** Transparent additive scoring ($0$ to $100$) with defense-in-depth mitigation credits and statutory floor protections ($\ge 55$) on critical violations.
3. **Advisory Machine Learning:** Scikit-learn pipeline predicting compliance likelihood based on a synthetic benchmark of 1,200 scenarios.
4. **Autonomous Uncertainty Handling:** Flags underspecified transfers as `NEEDS_REVIEW` instead of inventing conclusions.
5. **Interactive Full-Stack Web Application:** Modern, responsive Flask/Vanilla JS dashboard with one-click demo scenarios, policy explorer, and audit exports.

---

## 4. Key Features

- **Executive Compliance Dashboard:** Real-time metrics for total assessments, compliant counts, breach alerts, fleet-wide average risk scores, and visual risk distribution bars.
- **Interactive Assessment Form:** 12-parameter evaluation form capturing origin jurisdiction, data category, primary storage region, backup region, transfer mechanisms, and security controls.
- **One-Click Demonstration Scenarios:** Instant preloading of 6 benchmark scenarios covering compliant domestic hosting, critical cross-border violations, and disaster recovery backup leakage.
- **Explainable Factor Waterfall:** Itemized point-by-point breakdown showing exactly how the 0–100 risk score was computed.
- **Actionable AWS Remediations:** Specific guidance on AWS KMS encryption, IAM RBAC, and regional placement tailored to identified gaps.
- **Comprehensive Policy Explorer:** Searchable, filterable catalog of all policy rules with legal citations, severity badges, and source links.
- **Immutable SQLite Audit Trail:** Complete persistence across application restarts with search, filtering, and single-click **CSV and JSON export**.
- **REST API Suite:** Programmatic endpoints for automated CI/CD pipeline integration.

---

## 5. Technology Stack

- **Backend:** Python 3.10+ / Python 3.14, Flask 3.1
- **Frontend:** Semantic HTML5, CSS3 (Modern custom variables, responsive grid), Vanilla JavaScript (No heavyweight frameworks or CDN dependencies)
- **Database:** SQLite 3 (Persistent local relational datastore with JSON support)
- **Machine Learning:** scikit-learn 1.3+, pandas, joblib
- **Testing:** Python standard library `unittest` (22 automated test cases)
- **Cloud Architecture Parity:** Amazon Web Services (S3, RDS, Lambda, API Gateway, SageMaker, IAM, Cognito, CloudWatch, SNS, QuickSight)

---

## 6. Repository Structure

```text
SovereigntyAI_Cloud_Project_2026/
├── README.md                   # Comprehensive project documentation
├── LICENSE                     # MIT Open Source License
├── requirements.txt            # Python dependencies (Flask, scikit-learn, pandas, joblib)
├── .env.example                # Environment variable configuration template
├── .gitignore                  # Git ignore rules for caches, secrets, and SQLite DBs
├── app.py                      # Flask WSGI application entry point & REST APIs
├── config.py                   # Central settings, AWS regions, and jurisdiction metadata
├── policy_engine.py            # Deterministic statutory rule evaluation engine
├── risk_assessment.py          # Explainable risk scoring algorithm & recommendations
├── ai_services.py              # Advisory scikit-learn ML inference wrapper
├── database.py                 # SQLite datastore, audit logging, and CSV/JSON exporters
├── utils.py                    # Input validation, sanitization, and ID generator
├── run_tests.py                # Standalone test runner script
├── policies/
│   └── policy_rules.json       # Configurable statutory compliance rules (GDPR, DPDP, HIPAA)
├── dataset/
│   ├── raw/                    # Raw data acquisition notes (OPP-115 analysis)
│   ├── processed/              # Synthetic compliance dataset (1,200 records)
│   ├── sample_scenarios.json   # 6 pre-configured demonstration test cases
│   └── Dataset_Details.md      # Comprehensive dataset documentation and schema
├── architecture/
│   ├── AWS_Architecture.md     # AWS service mappings, Mermaid diagrams, deployment plan
│   ├── System_Architecture.md  # Layered system architecture and sequence diagrams
│   └── Workflow.md             # End-to-end evaluation lifecycle & state transition diagram
├── docs/
│   ├── Abstract.md             # Academic capstone abstract
│   ├── Objectives.md           # Functional and academic project objectives
│   ├── Literature_Survey.md    # 15 verified peer-reviewed publications (2023-2026) & matrix
│   ├── Research_Gap.md         # Detailed research gap analysis
│   ├── Novelty.md              # Architectural novelty & technical contributions
│   ├── AWS_Services.md         # Detailed breakdown of all 10 AWS service integrations
│   ├── Testing_Report.md       # Full test execution report (22 tests, 100% pass)
│   ├── Viva_Questions.md       # Comprehensive viva voce preparation guide (Q&A)
│   └── Project_Report.md       # Complete academic capstone project report
├── presentation/
│   └── README.md               # 12-slide presentation outline and 5-min viva demo script
├── results/
│   ├── README.md               # Overview of empirical results
│   └── model_metrics.json      # Verified ML evaluation metrics (Accuracy, F1, Confusion Matrix)
├── scripts/
│   ├── generate_dataset.py     # Generates reproducible synthetic compliance dataset
│   ├── train_ml_model.py       # Trains scikit-learn RandomForestClassifier baseline
│   ├── evaluate_model.py       # Standalone terminal evaluation script
│   └── seed_demo_data.py       # Seeds SQLite database with demonstration records
├── src/
│   ├── aws/                    # Modular cloud adapters (S3, SNS, CloudWatch)
│   ├── backend/                # Backend component documentation
│   ├── frontend/               # Frontend component documentation
│   └── ml_model/               # Serialized model artifact (sovereignty_risk_model.joblib)
├── static/
│   ├── css/style.css           # Clean, accessible styling (cards, dials, badges)
│   └── js/app.js               # Client controller for scenario preloading & policy filters
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Common layout with navigation bar & footer
│   ├── index.html              # Main dashboard view
│   ├── assessment.html         # Assessment form & XAI results display
│   ├── policies.html           # Policy Explorer
│   ├── history.html            # Searchable audit history
│   ├── detail.html             # Single assessment detailed audit view
│   ├── scenarios.html          # Demonstration scenario showcase
│   └── about.html              # About page & viva cheat-sheet
└── tests/                      # Automated test suite
    ├── test_policy_engine.py   # Unit tests for policy evaluation rules
    ├── test_risk_assessment.py # Unit tests for risk score calculation & bounds
    ├── test_database.py        # Unit tests for SQLite CRUD & exports
    ├── test_scenarios.py       # Integration tests for all 6 sample scenarios
    └── test_app.py             # Integration tests for web routes & REST APIs
```

---

## 7. Installation & Setup (macOS / Linux)

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14.
- `pip` package manager.
- Git.

### Step 1: Clone or Navigate to the Repository
```bash
cd SovereigntyAI_Cloud_Project_2026
git checkout feature/aadya
```

### Step 2: Install Dependencies
```bash
pip3 install -r requirements.txt
```

### Step 3: Seed Demonstration Data (Optional but Recommended)
Populate initial sample assessments so the dashboard displays live metrics upon startup:
```bash
python3 scripts/seed_demo_data.py
```

---

## 8. Running the Application

Start the SovereigntyAI web server:
```bash
python3 app.py
```
*Expected terminal output:*
```text
[*] Starting SovereigntyAI Server on http://127.0.0.1:5001
```
Open your web browser and navigate to:
**[http://127.0.0.1:5001](http://127.0.0.1:5001)**

---

## 9. Running the Automated Test Suite

Execute the complete 22-test automated suite:
```bash
python3 run_tests.py
```
Or via standard unittest discovery:
```bash
python3 -m unittest discover -s tests -v
```
*Result:* All 22 tests pass in **~0.69 seconds** with zero failures.

---

## 10. Sample Demonstration Scenarios

SovereigntyAI includes six pre-configured scenarios accessible from the **"Scenarios"** menu:

1. **SCENARIO-01 (Safe EU Local):** Enterprise personal data stored in `eu-central-1` (Frankfurt) with KMS encryption and CloudTrail. &rarr; **Result: COMPLIANT (Score: 0, Low Risk)**.
2. **SCENARIO-02 (GDPR Cross-Border Breach):** EU patient health records transferred to `us-east-1` without SCCs and unencrypted. &rarr; **Result: NON_COMPLIANT (Score: 100, Critical Risk)**.
3. **SCENARIO-03 (India DPDP Act Compliant):** Indian financial records stored in Mumbai (`ap-south-1`) with DR in Hyderabad (`ap-south-2`) adhering to Sec 8(5). &rarr; **Result: COMPLIANT (Score: 10, Low Risk)**.
4. **SCENARIO-04 (Weak Security Controls):** US financial data stored in `us-east-1` with disabled encryption and logging. &rarr; **Result: NON_COMPLIANT (Score: 98, Critical Risk)**.
5. **SCENARIO-05 (Secondary DR Backup Risk):** Indian personal data stored locally in Mumbai, but backup replicated to Virginia (`us-east-1`) without transfer terms. &rarr; **Result: NEEDS_REVIEW (Score: 50, Moderate Risk)**.
6. **SCENARIO-06 (Ambiguous Transfer):** International transfer with unverified mechanisms triggering mandatory governance review. &rarr; **Result: NEEDS_REVIEW (Score: 73, High Risk)**.

---

## 11. REST API Usage Examples

### Evaluate Compliance Programmatically
```bash
curl -X POST http://127.0.0.1:5001/api/assessments \
  -H "Content-Type: application/json" \
  -d '{
    "origin_jurisdiction": "EU_EEA",
    "source_org": "FinTech Europe AG",
    "data_category": "personal",
    "storage_region": "eu-central-1",
    "backup_region": "eu-west-1",
    "cross_border": false,
    "transfer_mechanism": "adequate_country",
    "encryption_at_rest": true,
    "access_control": true,
    "audit_logging": true,
    "framework": "GDPR"
  }'
```

### List Configured Policy Rules
```bash
curl http://127.0.0.1:5001/api/policies
```

---

## 12. AWS Production Service Mapping

| AWS Service | Architecture Role | Production Implementation |
| :--- | :--- | :--- |
| **Amazon S3** | Audit Archive | Immutable WORM object storage for JSON reports (`data/s3_mock/` locally). |
| **Amazon RDS** | Relational Datastore | Multi-AZ PostgreSQL for assessments (SQLite locally). |
| **AWS Lambda** | Serverless Compute | Event-driven policy evaluation triggered on CI/CD code push. |
| **Amazon API Gateway**| Ingestion & Throttling | Edge REST API with rate limiting and TLS 1.3 termination. |
| **Amazon SageMaker** | ML Pipeline | Model endpoint hosting and periodic retraining. |
| **AWS IAM** | Least-Privilege RBAC | Fine-grained service execution roles and KMS key policies. |
| **Amazon Cognito** | Authentication | Multi-user federated identity for auditors and engineers. |
| **Amazon CloudWatch** | Telemetry & Alarms | Custom metrics (`AssessmentEvaluated`, `RiskScore`) and breach alarms. |
| **Amazon SNS** | Incident Alerts | Immediate push notifications for `NON_COMPLIANT` breaches. |
| **Amazon QuickSight** | Business Intelligence | Fleet-wide compliance posture and risk heatmaps. |

*Estimated monthly pilot operational cost on AWS:* **~$18.09 / month** (details in `architecture/AWS_Architecture.md`).

---

## 13. Limitations & Disclosures

1. **Educational & Decision-Support Prototype:** SovereigntyAI provides technical risk assessment for cloud architectures. It does not constitute certified legal counsel or formal statutory immunity under EU, Indian, or US law.
2. **Advisory ML Baseline:** The scikit-learn model is trained exclusively on synthetic benchmark scenarios to explore ML heuristics; the deterministic policy engine remains the authoritative compliance mechanism.
3. **Regional Scope:** Focuses on AWS infrastructure; multi-cloud expansion to Azure and GCP is planned for future work.

---

## 14. Academic References & Literature Survey

This project is grounded in 15 peer-reviewed publications (2023–2026) across IEEE, ACM, Springer, and MDPI, including:
1. J. Ernstberger et al., *"SoK: Data Sovereignty"*, 2023 IEEE EuroS&P, DOI: [10.1109/EuroSP57164.2023.00017](https://doi.org/10.1109/EuroSP57164.2023.00017).
2. N. A. Zaguir et al., *"Challenges and Enablers for GDPR Compliance"*, IEEE Access, 2024, DOI: [10.1109/ACCESS.2024.3406724](https://doi.org/10.1109/ACCESS.2024.3406724).
3. T. Yanagawa et al., *"A Secure Framework for Continuous Compliance across Heterogeneous Policy Validation Points"*, 2024 IEEE CLOUD, DOI: [10.1109/CLOUD62652.2024.00029](https://doi.org/10.1109/CLOUD62652.2024.00029).
4. V. Karagiannis, *"Data Sovereignty and Compliance in the Computing Continuum"*, 2024 IEEE FiCloud, DOI: [10.1109/FiCloud62933.2024.00027](https://doi.org/10.1109/FiCloud62933.2024.00027).
5. S. Galij et al., *"Modeling Data Sovereignty in Public Cloud"*, Applied Sciences (MDPI), 2024, DOI: [10.3390/app142310803](https://doi.org/10.3390/app142310803).

*Complete bibliography, DOIs, and comparative matrix are in `docs/Literature_Survey.md`.*

---

## 15. License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
