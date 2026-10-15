# Project Abstract

**Project Title:** Autonomous Cloud Data Sovereignty Compliance Framework for Cross-Border Cloud Applications using Policy Intelligence and Explainable AI

**Project Name:** SovereigntyAI

**Academic Cohort:** Cloud Computing & Applied AI Engineering Capstone 2026

---

### Abstract Text

The exponential adoption of hyperscale public cloud architectures (such as Amazon Web Services) has empowered multinational enterprises to deploy globally distributed applications with unprecedented agility. However, this global infrastructure directly collides with an increasingly fragmented and extraterritorial regulatory landscape governing cross-border data flows. Statutes such as the European Union’s General Data Protection Regulation (GDPR), the Indian Digital Personal Data Protection Act, 2023 (DPDP Act), and United States sectoral mandates (HIPAA, PCI-DSS) impose stringent, conflicting conditions on data residency, international transfers, and security safeguards. Violations trigger severe financial penalties, operational injunctions, and reputational damage.

Traditional compliance mechanisms rely heavily on manual periodic legal reviews, spreadsheets, or black-box generative AI models that are prone to hallucinations, non-determinism, and lack of auditable traceability. To solve this dilemma, this project develops and implements **SovereigntyAI**, an autonomous, explainable cloud data sovereignty compliance framework.

SovereigntyAI introduces a hybrid intelligence architecture:
1. **Deterministic Policy Intelligence Engine:** Evaluates proposed cloud storage regions, cross-border transfers, and security configurations against structured, configurable condition trees grounded in verified statutory text (e.g., GDPR Chapter V Articles 44–49, DPDP Act 2023 Section 16).
2. **Explainable AI (XAI) Risk-Scoring Algorithm:** Generates a calibrated 0–100 exposure score accompanied by an itemized mathematical factor waterfall, mitigating operational risk without obfuscating critical legal failures.
3. **Advisory Machine Learning Baseline:** Implements a reproducible `scikit-learn` classifier (`RandomForestClassifier`, 96.25% accuracy, 0.96 Macro F1) trained on 1,200 synthetic deployment scenarios to benchmark statistical heuristics against statutory rules.
4. **Cloud-Native Architecture & Auditability:** Designed with modular abstractions mapping directly to AWS services (S3, RDS, Lambda, API Gateway, SageMaker, SNS, CloudWatch, QuickSight), featuring persistent SQLite audit trails, CSV/JSON export facilities, and pre-configured demonstration scenarios.

Implemented in Python 3 and Flask with a lightweight, responsive vanilla JavaScript and CSS frontend, SovereigntyAI operates entirely offline without external API keys or paid cloud subscriptions. The resulting framework provides academic and enterprise cloud architects with a transparent, verifiable tool to evaluate, explain, and remediate cross-border cloud sovereignty risks before infrastructure deployment.
