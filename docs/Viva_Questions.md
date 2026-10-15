# Viva Voce Examination Preparation Guide

This document contains curated questions and concise, authoritative answers designed to help a college student excel during their final project defense and viva voce examination.

---

## 1. Cloud Computing & Data Sovereignty Fundamentals

### Q1: What is data sovereignty, and how does it differ from data residency and data localization?
- **Data Residency:** Refers to the physical geographic location where an organization specifies its data is stored (e.g., "Our S3 bucket is hosted in Frankfurt, Germany").
- **Data Localization:** A strict legal mandate requiring data created within a jurisdiction to remain physically stored and processed within that jurisdiction's national borders (e.g., RBI payment localization in India).
- **Data Sovereignty:** The legal concept that digital data is subject to the laws and governance structures of the nation-state in which it was collected or where the data subjects reside, regardless of where the servers physically reside.

### Q2: Why is data sovereignty a major challenge for public hyperscale cloud providers like AWS?
AWS operates on a globally distributed multi-tenant model with shared management planes, automated cross-region replication, and centralized control systems. While this maximizes uptime and scalability, extraterritorial laws (such as the US CLOUD Act) allow foreign law enforcement to subpoena data managed by US-headquartered providers, even if stored in European or Asian data centers. Multinational enterprises must therefore implement technical controls (such as customer-managed encryption keys) to ensure true sovereignty.

---

## 2. Regulatory Frameworks: GDPR, India DPDP Act, and US Laws

### Q3: Does GDPR Chapter V prohibit all transfers of European personal data outside the EU/EEA?
**No.** This is a common misconception. GDPR Chapter V allows international transfers under several legal mechanisms:
1. **Article 45 Adequacy Decisions:** The European Commission recognizes a third country as providing an adequate level of data protection (e.g., Japan, UK, South Korea, Canada).
2. **Article 46 Appropriate Safeguards:** Organizations execute Standard Contractual Clauses (SCCs) or Binding Corporate Rules (BCRs) accompanied by supplementary technical measures (EDPB 01/2020).
3. **Article 49 Specific Derogations:** Explicit informed consent or contractual necessity for occasional, non-repetitive transfers.

### Q4: How does India's Digital Personal Data Protection Act, 2023 (DPDP Act) approach cross-border data transfers?
Section 16 of the DPDP Act 2023 adopts a **"blacklist" or "negative-list" model**:
- By default, cross-border transfer of personal data outside India is **permitted**.
- The Central Government retains the power to notify a list of restricted countries to which transfers are prohibited.
- Crucially, Section 8(5) mandates that the Data Fiduciary must implement **reasonable security safeguards** (encryption and access control) to prevent personal data breaches, regardless of storage location.

### Q5: What are the HIPAA technical safeguards for cloud storage?
Under 45 CFR § 164.312, cloud deployments processing Protected Health Information (PHI) must implement:
1. Access control with unique user identification and emergency access procedures.
2. Immutable hardware/software audit controls to record activity.
3. Integrity controls to prevent improper alteration.
4. Transmission and rest encryption.

---

## 3. Policy Engine & Explainable AI (XAI)

### Q6: Why did you implement a deterministic rule engine instead of using a Large Language Model (LLM) for compliance decisions?
1. **Zero Hallucination:** Regulatory compliance requires 100% determinism. LLMs can invent non-existent legal articles or misquote statutes.
2. **Auditability & Non-Repudiation:** A deterministic rule engine guarantees that the same cloud configuration submitted twice will produce the exact same result with identical mathematical justifications.
3. **Speed & Zero Cost:** Evaluates in under 1 millisecond locally without external API latency or token subscription costs.
4. **Data Privacy:** Avoids transmitting architectural configurations to third-party AI APIs.

### Q7: How does your risk-scoring algorithm work? Explain the mathematical formula.
The risk score (0 to 100) is computed additively with mitigation credits:
$$\text{Score} = \text{Base Sensitivity} + \sum \text{Policy Violation Penalties} + \sum \text{Deficiencies} - \sum \text{Mitigation Credits}$$
- **Base Sensitivity:** Non-personal (5), Personal (20), Financial (35), Healthcare (40).
- **Penalties:** Critical failed rule (+30), High failed rule (+20), Unencrypted plaintext (+15), Missing RBAC (+10).
- **Mitigation Credits:** KMS Encryption (-10), Access Controls (-8), CloudTrail Logging (-7).
- **Floor Protection:** If any Critical statutory rule fails, the score is floored at 55 to ensure an illegal transfer can never be deceptively scored as "Low Risk".

### Q8: What role does the machine learning model play if the policy engine is deterministic?
The `scikit-learn` `RandomForestClassifier` acts as an **advisory heuristic**:
- It demonstrates how machine learning models can be trained on past compliance audit batches to predict likelihood of approval during architectural triage.
- In our UI, it is clearly labeled as an advisory baseline that **does not override statutory policy rules**.
- The application includes graceful fallback handling if the model artifact is missing.

---

## 4. Dataset & Empirical Limitations

### Q9: Why did you not use the OPP-115 Privacy Policy dataset for cloud compliance evaluation?
The OPP-115 dataset consists of natural-language text extracted from website consumer privacy notices (e.g., "We use cookies for analytics"). It does **not** contain cloud infrastructure attributes such as AWS storage regions (`eu-central-1`), encryption types (SSE-KMS), access control flags, or disaster recovery backup configurations. Attempting to use website privacy notices to evaluate cloud server compliance would be domain-inappropriate. Therefore, we algorithmically generated a documented 1,200-sample synthetic cloud deployment dataset.

---

## 5. AWS Architecture & Enterprise Integration

### Q10: How does your application integrate with AWS?
The application is architected with modular adapters in `src/aws/`:
- **Amazon S3:** Archives immutable JSON compliance reports (using `boto3` when credentials exist, with a local `data/s3_mock/` fallback).
- **Amazon RDS:** Production relational database replacing local SQLite.
- **AWS Lambda & API Gateway:** Serverless execution of policy evaluation triggered by CI/CD pipelines.
- **Amazon SNS:** Dispatches immediate alert emails when a `NON_COMPLIANT` assessment occurs.
- **Amazon CloudWatch:** Emits operational telemetry and compliance breach metrics.

### Q11: What is the "Secondary Backup Replication" risk, and how does your engine handle it?
Many organizations store data locally in their home region (e.g., Mumbai `ap-south-1`) but configure automated cross-region replication for disaster recovery to a foreign region (e.g., Virginia `us-east-1`). This creates an unintentional cross-border export. Our policy rule `POL-BACKUP-001` explicitly validates secondary backup regions and flags jurisdictional mismatches.

---

## 6. Testing, Limitations, and Future Scope

### Q12: How did you test the system?
We created a 22-test automated test suite using Python's `unittest` framework covering:
1. Correct evaluation of GDPR, DPDP Act, HIPAA, and PCI-DSS rules.
2. Mathematical score clamping and risk band classification.
3. SQLite database persistence, query filtering, and CSV/JSON export integrity.
4. Flask web routes and REST API input validation (HTTP 200, 201, 400).
5. Verification that all 6 pre-configured sample scenarios produce their expected outcomes.

### Q13: What are the current limitations of the prototype?
1. **Scope of Jurisdictions:** Currently models EU/EEA, India, US Federal/Sectoral, California, UK, and Global standards. Additional national laws (e.g., China PIPL, Saudi Arabia PDPL) can be added as JSON rules.
2. **Simplified Cloud Providers:** Focuses on Amazon Web Services (AWS) regions; multi-cloud mapping to Microsoft Azure and Google Cloud Platform is future work.
3. **Educational Prototype:** It is an engineering decision-support tool, not certified legal counsel.

### Q14: What is the future scope of this project?
- **Infrastructure-as-Code (IaC) Pre-Commit Hook:** Integrating `policy_engine.py` directly into Terraform and AWS CloudFormation pipelines to automatically block non-compliant Git commits before deployment.
- **Live AWS CloudTrail Ingestion:** Continuously inspecting live AWS S3 and RDS bucket creation events via EventBridge and Lambda to detect runtime sovereignty drift.
