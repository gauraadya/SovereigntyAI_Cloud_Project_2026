# Research Gap Analysis

## 1. Context & Motivation

As public cloud infrastructure expands globally, the legal frameworks governing data residency, localization, and cross-border data transfers are diverging sharply across jurisdictions. Despite extensive research in cloud security, automated compliance, and explainable artificial intelligence, a critical gap exists between technical cloud infrastructure provisioning and statutory data sovereignty verification.

---

## 2. Identified Deficiencies in Existing Systems

### Gap 1: Disconnect Between CSPM Tools and Statutory Transfer Treaties
Commercial Cloud Security Posture Management (CSPM) tools—such as AWS Security Hub, Palo Alto Prisma Cloud, and Wiz—excel at detecting technical infrastructure misconfigurations (e.g., unencrypted S3 buckets, permissive security groups, disabled MFA). However:
- **Missing Jurisdictional Logic:** Existing CSPMs do not evaluate whether storing data in `us-east-1` when the data subjects originate in Frankfurt constitutes an unauthorized international transfer under GDPR Chapter V.
- **Absence of Legal Transfer Instruments:** CSPMs do not assess whether Standard Contractual Clauses (SCCs), Adequacy Decisions, or Binding Corporate Rules (BCRs) are documented.
- **Secondary Backup Blindness:** They fail to detect secondary disaster recovery replication scenarios that cross sovereignty boundaries.

### Gap 2: Inadequacy of Generative AI (LLMs) for Regulatory Compliance
Recent attempts to apply Large Language Models (LLMs) to legal compliance introduce severe operational risks:
- **Hallucinations & Legal Inaccuracy:** LLMs frequently invent non-existent regulatory clauses, misquote statutory numbers, and generate conflicting legal conclusions.
- **Non-Determinism:** The same cloud deployment submitted twice can yield different outputs, violating regulatory auditability and non-repudiation mandates.
- **Black-Box Opacity:** Neural language models cannot provide an auditable, mathematical point-by-point breakdown of how a compliance risk score was derived.
- **Data Privacy & Leakage Concerns:** Transmitting proprietary enterprise architecture configurations to third-party commercial LLM APIs often violates the very data sovereignty policies being assessed.

### Gap 3: Theoretical Focus of Academic Sovereign Cloud Frameworks
Academic initiatives such as the European Gaia-X project, the International Data Spaces Association (IDSA), and Self-Sovereign Identity (SSI) frameworks have proposed federated data spaces. However:
- **Lack of Practical Tooling for Standard Hyperscalers:** These frameworks assume specialized decentralized dataspace connectors (DSCs) and federated sovereign hardware rather than standard commercial AWS regions where 90%+ of enterprises actually operate.
- **Excessive Complexity:** Existing prototypes require intricate distributed ledger or multi-container orchestrations that are impossible for solo students or small engineering teams to run or demonstrate locally.

### Gap 4: Absence of Explainable Risk Scoring (XAI) in Cloud Governance
Current governance tools offer binary (Pass/Fail) flags or opaque proprietary risk numbers. They lack:
- An itemized factor waterfall demonstrating exactly which variables (data category weight, cross-border transfer, missing encryption, active audit logging) contributed to the final exposure score.
- Defense-in-depth mitigation recognition (rewarding customer-managed KMS encryption and RBAC without disguising critical statutory violations).

---

## 3. How SovereigntyAI Bridges These Research Gaps

| Dimension | Existing Practice / Academic Literature | SovereigntyAI Solution |
| :--- | :--- | :--- |
| **Decision Mechanism** | Manual lawyer review OR black-box LLM generation | **Deterministic, auditable condition trees grounded in statute** |
| **Jurisdictional Scope** | Single framework focus (GDPR only) | **Multi-jurisdictional: EU GDPR, India DPDP Act 2023, US HIPAA/PCI-DSS** |
| **Cross-Border Intelligence**| Ignored by CSPM tools | **Automatic cross-border inference and transfer mechanism validation** |
| **Risk Explainability** | Opaque percentage or binary Pass/Fail | **Itemized factor breakdown, calculation narrative, and score bands** |
| **Machine Learning Role** | Unchecked generative generation | **Strictly advisory scikit-learn baseline benchmarked against rules** |
| **Deployment Footprint** | Expensive enterprise SaaS or complex federation | **Lightweight, runnable locally offline without API keys or paid cloud** |
