# Project Report: Autonomous Cloud Data Sovereignty Compliance Framework

**Project Title:** Autonomous Cloud Data Sovereignty Compliance Framework for Cross-Border Cloud Applications using Policy Intelligence and Explainable AI
**Acronym:** SovereigntyAI
**Academic Year:** 2026
**Repository:** `SovereigntyAI_Cloud_Project_2026` (Branch: `feature/aadya`)

---

## Table of Contents
1. Abstract
2. Introduction & Background
3. Problem Statement
4. Project Objectives
5. Existing System vs. Proposed System
6. Literature Survey Summary
7. Research Gap
8. Novelty & Technical Contributions
9. Methodology
10. System & AWS Architecture
11. Dataset Engineering & Evaluation
12. Implementation Details
13. Empirical Results & Verification
14. Limitations
15. Conclusion & Future Scope
16. References

---

## 1. Abstract
As enterprises increasingly adopt hyperscale cloud infrastructure (such as Amazon Web Services), navigating cross-border data sovereignty has become a paramount legal and architectural challenge. Conflicting statutory requirements—notably the European Union GDPR, India's DPDP Act 2023, and US sectoral mandates (HIPAA, PCI-DSS)—impose strict conditions on data residency, international transfers, and security controls. Traditional manual compliance audits are unscalable, and black-box generative AI models suffer from hallucinations and legal non-determinism.

This project implements **SovereigntyAI**, a full-stack, autonomous framework that couples a deterministic policy intelligence engine with an explainable AI (XAI) risk-scoring algorithm and an advisory scikit-learn machine learning baseline. Implemented in Python 3, Flask, and SQLite with a vanilla JS/CSS web dashboard, the system evaluates cloud storage and replication configurations, computes calibrated risk scores (0–100), provides itemized mathematical factor waterfalls, and generates actionable AWS remediation recommendations. The application runs entirely locally without paid cloud subscriptions or external API keys, while providing drop-in modular adapters for Amazon S3, RDS, Lambda, SageMaker, SNS, and CloudWatch.

---

## 2. Introduction & Background
Public cloud computing has transformed enterprise IT by decoupling computational workloads from physical on-premise hardware. Hyperscalers operate multi-tenant data centers globally, offering automated cross-region replication and load balancing. However, the legal reality of digital data has moved in the opposite direction: nation-states increasingly assert extraterritorial legal sovereignty over citizen data.

Under modern data protection regimes:
- Data collected from European residents is governed by **GDPR Chapter V (Articles 44–49)**.
- Personal data of Indian residents is governed by **Digital Personal Data Protection Act, 2023 (Sections 8 & 16)**.
- Health records in the United States must satisfy **HIPAA Security Rule Technical Safeguards (45 CFR § 164.312)**.

Cloud solutions architects face significant difficulty in verifying whether a given Amazon S3 bucket, RDS database, or disaster recovery replication strategy violates one or more of these complex statutory frameworks.

---

## 3. Problem Statement
Multinational cloud applications lack automated, transparent, and auditable tooling to evaluate whether a proposed cloud data storage or cross-border transfer configuration satisfies jurisdiction-specific compliance laws. Existing Cloud Security Posture Management (CSPM) tools inspect technical vulnerabilities (e.g., open ports, unencrypted buckets) but completely overlook international transfer treaties, adequacy decisions, and cross-border statutory restrictions. Conversely, generative AI models introduce non-deterministic hallucinations, data leakage risks, and unverified legal advice. There is an urgent need for an open, explainable, and deterministic compliance verification framework tailored for cloud architectures.

---

## 4. Project Objectives
1. **Develop a Deterministic Policy Engine:** Model GDPR, DPDP Act 2023, HIPAA, and secondary backup sovereignty rules into structured JSON condition trees.
2. **Implement an Explainable AI (XAI) Risk Algorithm:** Create an auditable mathematical scoring algorithm (0 to 100) with itemized factor attribution and defense-in-depth mitigation recognition.
3. **Train an Advisory ML Baseline:** Train a reproducible scikit-learn classifier on a documented 1,200-sample synthetic dataset, reporting genuine metrics and providing graceful offline fallbacks.
4. **Deliver a Full-Stack Web Application:** Implement a modern Flask dashboard, interactive assessment form with 12 parameters, policy explorer, audit history, and CSV/JSON export capabilities.
5. **Design an Enterprise AWS Blueprint:** Detail cloud service mappings (S3, RDS, Lambda, API Gateway, SageMaker, IAM, Cognito, CloudWatch, SNS, QuickSight) with architecture diagrams and cost analyses.
6. **Validate with Automated Testing:** Build and execute a 22-test automated suite ensuring 100% pass rates across all functional components and sample scenarios.

---

## 5. Existing System vs. Proposed System

| Dimension | Existing Industry Practice | SovereigntyAI Proposed Framework |
| :--- | :--- | :--- |
| **Review Cadence** | Manual, annual or quarterly legal audit | Continuous, automated, pre-deployment verification |
| **Decision Engine** | Human lawyer review or black-box LLM prompt | Deterministic statutory condition trees (zero hallucination) |
| **CSPM Scope** | Technical misconfigurations only | Technical controls + international transfer legality |
| **Scoring Model** | Opaque high/med/low qualitative rating | Mathematical 0–100 score with itemized factor waterfall |
| **Multi-Region DR** | Blind to cross-border backup leakage | Explicit evaluation of secondary DR backup sovereignty |
| **Cost & Dependencies** | Expensive enterprise SaaS or paid API tokens | 100% free, local, open-source execution |

---

## 6. Literature Survey Summary
A systematic review of 15 peer-reviewed publications (2023–2026) across IEEE, ACM, Springer, and MDPI was conducted (documented in `docs/Literature_Survey.md`). Notable findings include:
- Ernstberger et al. (*IEEE EuroS&P 2023*) formalized data sovereignty taxonomies, highlighting the divergence between technical and legal control.
- Zaguir et al. (*IEEE Access 2024*) identified that GDPR compliance tooling lacks unified, developer-accessible open-source automation.
- Yanagawa et al. (*IEEE CLOUD 2024*) demonstrated GitOps continuous compliance for security policies, but lacked cross-border transfer modeling.
- Arreche et al. (*IEEE Access 2024*) and Ben Ghozzi et al. (*IEEE INISTA 2024*) confirmed that explainable AI (XAI) is critical for auditable decision-making in high-stakes environments.

---

## 7. Research Gap & Novelty
- **Gap:** Existing CSPMs do not check cross-border legal instruments; generative LLMs hallucinate; academic federated models (Gaia-X) are overly complex for standard cloud deployments.
- **Novelty:**
  1. Hybrid architecture pairing deterministic statutory rules with an advisory ML baseline.
  2. Nuanced legal modeling recognizing that GDPR and India's DPDP Act do not mandate blanket localization, but rather governed transfers.
  3. Native evaluation of secondary disaster recovery backup regions.
  4. Explainable point-by-point factor waterfall with statutory floor protections ($\ge 55$).
  5. Principled autonomous fallback to `NEEDS_REVIEW` under uncertainty.

---

## 8. Methodology

### Policy Representation & Ingestion
Rules are declared in `policies/policy_rules.json` with fields: `rule_id`, `jurisdiction`, `framework`, `rule_type`, `severity`, `applicable_categories`, `conditions`, `explanation_pass/fail`, `remediation`, and `legal_reference`.

### Mathematical Risk Formulation
The overall risk score $R \in [0, 100]$ is computed as:
$$R = \min\left(100, \max\left(0, S_{\text{base}} + \sum P_i + \sum D_j - \sum M_k\right)\right)$$
Where:
- $S_{\text{base}}$: Base data category sensitivity ($5$ to $40$).
- $P_i$: Penalties for failed statutory policy rules ($+5$ to $+30$).
- $D_j$: Penalties for security deficiencies (plaintext storage $= +15$, missing RBAC $= +10$).
- $M_k$: Mitigation credits (KMS encryption $= -10$, IAM RBAC $= -8$, CloudTrail $= -7$).
- If any Critical statutory violation occurs: $R = \max(55, R)$ and Status = `NON_COMPLIANT`.

---

## 9. System & AWS Architecture
Detailed in `architecture/System_Architecture.md` and `architecture/AWS_Architecture.md`:
- **Presentation Layer:** HTML5, CSS3, Vanilla JavaScript, dynamic scenario loader.
- **Application Controller:** Flask WSGI, request sanitization, security headers.
- **Engine Tier:** `policy_engine.py`, `risk_assessment.py`.
- **Machine Learning:** `ai_services.py` loading `sovereignty_risk_model.joblib`.
- **Datastore Tier:** SQLite (`database.py`) with audit trails and CSV/JSON exporters.
- **Cloud Extension:** Modular adapters for AWS S3, RDS, Lambda, SageMaker, SNS, and CloudWatch.

---

## 10. Dataset Engineering & Evaluation
Detailed in `dataset/Dataset_Details.md`:
- Explains why the OPP-115 Privacy Policy dataset (unstructured website privacy prose) cannot be used for cloud infrastructure evaluation.
- Synthesizes a balanced, reproducible 1,200-sample dataset (`dataset/processed/synthetic_compliance_data.csv`).
- Trains a `RandomForestClassifier` (100 estimators, max depth 12) on an 80/20 train/test split.
- **Test Metrics:** Accuracy: **96.25%**, Macro F1: **0.9602**, Weighted F1: **0.9623**.

---

## 11. Implementation & Verification
- Full implementation in Python 3.14 / Flask 3.1.
- Complete automated test suite (`tests/`) containing 22 tests covering policy evaluation, risk score bounds, SQLite transactions, REST APIs, and sample scenarios.
- All 22 tests pass in 0.69 seconds.

---

## 12. Limitations & Future Scope
- **Current Limitations:** Focuses on AWS regions (multi-cloud GCP/Azure mapping in progress); models primary jurisdictions (EU, India, US); educational advisory tool rather than certified legal counsel.
- **Future Scope:** CI/CD pre-commit hooks for Terraform / CloudFormation; live AWS CloudTrail event stream ingestion via AWS EventBridge and Lambda.

---

## 13. Conclusion
SovereigntyAI demonstrates that complex extraterritorial data sovereignty laws can be modeled systematically, evaluated deterministically, and explained transparently within public cloud architectures. By pairing rigorous statutory condition trees with an explainable risk scoring model, the framework provides an accessible, reproducible blueprint for compliant cloud engineering.
