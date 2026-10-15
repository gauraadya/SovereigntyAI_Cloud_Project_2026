# Literature Survey: Cloud Data Sovereignty, Compliance Automation, and Explainable AI

## 1. Overview and Taxonomy

Cross-border cloud data sovereignty represents one of the most critical legal-architectural challenges facing multi-tenant public cloud ecosystems. Multinational organizations operating on hyperscale infrastructure such as Amazon Web Services (AWS) face conflicting extraterritorial mandates: the European Union's General Data Protection Regulation (GDPR), the Indian Digital Personal Data Protection Act, 2023 (DPDP Act), US sectoral requirements (HIPAA, GLBA), and conflicting foreign intelligence surveillance reach (e.g., the US CLOUD Act).

This survey reviews **15 genuine, verifiably indexed peer-reviewed publications (prioritizing 2023–2026)** across IEEE, ACM, Springer, MDPI, and related indexed scholarly venues.

---

## 2. Research Papers & Scholarly Analysis

### Paper 1: Foundational Systematization of Data Sovereignty
- **Verified Title:** SoK: Data Sovereignty
- **Authors:** Jens Ernstberger, Jan Lauinger, Fatima Elsheimy, Liyi Zhou, Sebastian Steinhorst, Ran Canetti, Andrew Miller, Arthur Gervais, Dawn Song
- **Publication Venue:** 2023 IEEE 8th European Symposium on Security and Privacy (EuroS&P)
- **Year:** 2023
- **DOI:** [10.1109/EuroSP57164.2023.00017](https://doi.org/10.1109/EuroSP57164.2023.00017)
- **Main Contribution:** Systematizes the fragmented landscape of data sovereignty, establishing rigorous formal definitions across data ownership, data control, cryptographic self-sovereignty, and jurisdictional residency.
- **Relevance to SovereigntyAI:** Provides the formal theoretical taxonomy separating technical controls (encryption, access control) from legal jurisdiction constraints.
- **Limitation / Research Gap:** Focuses heavily on cryptographic primitives and blockchain mechanisms; does not provide an automated statutory policy evaluation engine for AWS infrastructure deployments.

### Paper 2: Edge-Assisted Sovereign Data Architectures
- **Verified Title:** Data Sovereignty at the Edge of the Network
- **Authors:** G. Carotenuto, F. Forestiero, A. Papuzzo
- **Publication Venue:** 2023 IEEE 7th International Conference on Fog and Edge Computing (ICFEC)
- **Year:** 2023
- **DOI:** [10.1109/ICFEC57925.2023.00013](https://doi.org/10.1109/ICFEC57925.2023.00013)
- **Main Contribution:** Demonstrates an architectural pattern where sensitive data operations are processed within local network edge components to satisfy residency requirements while minimizing cloud latency.
- **Relevance to SovereigntyAI:** Justifies our multi-region hybrid deployment logic and regional AWS Outposts / local storage placement principles.
- **Limitation / Research Gap:** Lacks dynamic policy evaluation; requires manual pre-allocation of edge workloads without automated risk scoring.

### Paper 3: Sovereignty in the Multi-Tier Computing Continuum
- **Verified Title:** Data Sovereignty and Compliance in the Computing Continuum
- **Authors:** Vasileios Karagiannis
- **Publication Venue:** 2024 11th International Conference on Future Internet of Things and Cloud (FiCloud)
- **Year:** 2024
- **DOI:** [10.1109/FiCloud62933.2024.00027](https://doi.org/10.1109/FiCloud62933.2024.00027)
- **Main Contribution:** Formulates compliance and sovereignty governance spanning distributed IoT, edge, fog, and hyperscale cloud layers, proposing continuous monitoring across heterogeneous tiers.
- **Relevance to SovereigntyAI:** Informs our policy engine's treatment of secondary backup replication regions and transit pipelines.
- **Limitation / Research Gap:** Focuses on IoT/fog topologies and does not implement explainable scoring models or automated remediation recommendations for AWS services.

### Paper 4: Systematic Review of GDPR Technical Enablers
- **Verified Title:** Challenges and Enablers for GDPR Compliance: Systematic Literature Review and Future Research Directions
- **Authors:** Nemer A. Zaguir, Guilherme Henrique de Magalhães, Mauro de Mesquita Spinola
- **Publication Venue:** IEEE Access (Vol. 12)
- **Year:** 2024
- **DOI:** [10.1109/ACCESS.2024.3406724](https://doi.org/10.1109/ACCESS.2024.3406724)
- **Main Contribution:** Conducts an extensive review of technical and organizational measures (TOMs) required under GDPR, cataloging consent management, auditability, pseudonymization, and international transfer barriers.
- **Relevance to SovereigntyAI:** Validates our rule base for GDPR Chapter V (Articles 44–49) and Article 32 security safeguards.
- **Limitation / Research Gap:** Identifies the absence of unified open-source automated compliance tooling that cloud developers can run locally without complex enterprise software.

### Paper 5: GitOps-Driven Policy Validation for Continuous Cloud Compliance
- **Verified Title:** A Secure Framework for Continuous Compliance across Heterogeneous Policy Validation Points
- **Authors:** Takumi Yanagawa, Vikas Agarwal, Yuji Watanabe, Lou Degenaro, Anca Sailer
- **Publication Venue:** 2024 IEEE 17th International Conference on Cloud Computing (CLOUD)
- **Year:** 2024
- **DOI:** [10.1109/CLOUD62652.2024.00029](https://doi.org/10.1109/CLOUD62652.2024.00029)
- **Main Contribution:** Proposes a GitOps-anchored continuous compliance architecture linking code commits to policy validation points (PVPs) to prevent misconfiguration drift.
- **Relevance to SovereigntyAI:** Serves as the blueprint for our modular policy engine and future AWS CloudFormation / CI/CD pipeline integration.
- **Limitation / Research Gap:** Does not model jurisdiction-specific cross-border transfer laws or provide an explainable exposure score for legal viva and audit inspections.

### Paper 6: Artificial Intelligence in Critical Infrastructure Compliance
- **Verified Title:** An Automated Compliance Framework for Critical Infrastructure Security Through Artificial Intelligence
- **Authors:** Sardar Muhammad Ali, Abdul Razzaque, Muhammad Yousaf, Rafi Us Shan
- **Publication Venue:** IEEE Access (Vol. 12)
- **Year:** 2024 / 2025
- **DOI:** [10.1109/ACCESS.2024.3524496](https://doi.org/10.1109/ACCESS.2024.3524496)
- **Main Contribution:** Employs machine learning algorithms to automate compliance verification against NIST, ISO 27001, and critical infrastructure frameworks.
- **Relevance to SovereigntyAI:** Confirms the utility of automated classification models in augmenting security audits.
- **Limitation / Research Gap:** Focuses strictly on industrial control and network security baselines without addressing international privacy jurisdiction conflicts.

### Paper 7: Public Cloud Data Sovereignty Modeling
- **Verified Title:** Modeling Data Sovereignty in Public Cloud—A Comparison of Existing Solutions
- **Authors:** Stanisław Galij, Grzegorz Pawlak, Sławomir Grzyb
- **Publication Venue:** Applied Sciences (MDPI, Vol. 14, Issue 23)
- **Year:** 2024
- **DOI:** [10.3390/app142310803](https://doi.org/10.3390/app142310803)
- **Main Contribution:** Compares commercial sovereign cloud architectures (AWS European Sovereign Cloud, Microsoft Cloud for Sovereignty, Google Sovereign Cloud) and assesses how technical measures prevent unauthorized extraterritorial access.
- **Relevance to SovereigntyAI:** Directly validates our AWS region classification, sovereign cloud readiness tags, and KMS encryption requirements.
- **Limitation / Research Gap:** Provides a qualitative comparative taxonomy rather than an executable policy evaluation prototype for software developers.

### Paper 8: Institutional and Technical Decisions in Data Protection
- **Verified Title:** Technologies of Data Protection and Institutional Decisions for Data Sovereignty
- **Authors:** Enrico Del Re
- **Publication Venue:** Information (MDPI, Vol. 15, Issue 8)
- **Year:** 2024
- **DOI:** [10.3390/info15080444](https://doi.org/10.3390/info15080444)
- **Main Contribution:** Explores how cryptographic mechanisms (homomorphic encryption, secure enclaves, customer key management) align with institutional legal obligations.
- **Relevance to SovereigntyAI:** Supports our decision to incorporate mitigation credits for customer-managed encryption (KMS) in the risk assessment engine.
- **Limitation / Research Gap:** Conceptual legal-technical paper with no reproducible software implementation or test benchmark.

### Paper 9: Inter-Organizational Data Sovereignty and Usage Control
- **Verified Title:** Data Sovereignty in Inter-organizational Information Systems
- **Authors:** Sebastian Opriel, Frederik Möller, Gero Strobel, Boris Otto
- **Publication Venue:** Business & Information Systems Engineering (Springer)
- **Year:** 2024
- **DOI:** [10.1007/s12599-024-00893-4](https://doi.org/10.1007/s12599-024-00893-4)
- **Main Contribution:** Examines how industrial data spaces (such as Catena-X in automotive supply chains) enforce continuous data usage control policies when data crosses institutional boundaries.
- **Relevance to SovereigntyAI:** Reinforces the principle that sovereignty does not end at initial storage, but persists across disaster recovery, secondary replication, and access logs.
- **Limitation / Research Gap:** Oriented toward B2B dataspace connectors rather than public cloud region deployment validation.

### Paper 10: Survey on Digital Sovereignty and Identity
- **Verified Title:** Survey on Digital Sovereignty and Identity: From Digitization to Digitalization
- **Authors:** Kheng Leong Tan, Chi-Hung Chi, Kwok-Yan Lam
- **Publication Venue:** ACM Computing Surveys (ACM, Vol. 56, Issue 3)
- **Year:** 2023
- **DOI:** [10.1145/3616400](https://doi.org/10.1145/3616400)
- **Main Contribution:** Reviews self-sovereign identity (SSI), decentralized verifiable credentials, and user data sovereignty across Web3 and multi-cloud architectures.
- **Relevance to SovereigntyAI:** Guides the identity and access control (IAM RBAC) dimensions of our policy evaluation framework.
- **Limitation / Research Gap:** Focuses primarily on identity credentials rather than cloud storage regionality and statutory cross-border export restrictions.

### Paper 11: Explainable AI in Threat and Network Security
- **Verified Title:** E-XAI: Evaluating Black-Box Explainable AI Frameworks for Network Intrusion Detection
- **Authors:** Osvaldo Arreche, Tanish R. Guntur, Jack W. Roberts, Mustafa Abdallah
- **Publication Venue:** IEEE Access (Vol. 12)
- **Year:** 2024
- **DOI:** [10.1109/ACCESS.2024.3365140](https://doi.org/10.1109/ACCESS.2024.3365140)
- **Main Contribution:** Demonstrates how explainable AI methods (SHAP, LIME, feature contribution metrics) enable security practitioners to understand and trust automated threat classification decisions.
- **Relevance to SovereigntyAI:** Directly inspires our transparent factor-breakdown waterfall in `risk_assessment.py`, ensuring human operators understand why points were added or deducted.
- **Limitation / Research Gap:** Examines network packet telemetry rather than statutory compliance rule structures.

### Paper 12: Attribute-Based Access Control in Regulated Cloud Environments
- **Verified Title:** Attribute-Based Approaches for Secure Data Sharing in Industrial Contexts
- **Authors:** A. Chiquito, U. Bodin, O. Schelén
- **Publication Venue:** IEEE Access (Vol. 11)
- **Year:** 2023
- **DOI:** [10.1109/ACCESS.2023.3240000](https://doi.org/10.1109/ACCESS.2023.3240000)
- **Main Contribution:** Details implementation of fine-grained attribute-based access control (ABAC) to enforce contextual data sharing constraints across multi-tenant environments.
- **Relevance to SovereigntyAI:** Informs our access control evaluation checks under DPDP Section 8 and HIPAA Security Rule.
- **Limitation / Research Gap:** Implements authorization policies without evaluating geographic storage boundaries or international transfer treaties.

### Paper 13: Data Connectors and Cross-Border Digital Twins
- **Verified Title:** Network Digital Twins Data Connectors Using International Data Spaces
- **Authors:** A. Abishek, L. Gifré Renom, R. Vilalta Cañellas, R. Muñoz, X. Masip-Bruin, A. Asensio Garcia
- **Publication Venue:** 2025 International Conference on Transparent Optical Networks (ICTON)
- **Year:** 2025
- **DOI:** [10.1109/ICTON67126.2025.11125301](https://doi.org/10.1109/ICTON67126.2025.11125301)
- **Main Contribution:** Implements policy-driven International Data Spaces (IDS) connectors to control cross-border data telemetry in telecommunication networks.
- **Relevance to SovereigntyAI:** Demonstrates runtime enforcement of sovereignty constraints in live cloud/network workflows.
- **Limitation / Research Gap:** Designed for specialized optical and SDN network digital twins, not generalized enterprise cloud applications.

### Paper 14: Analysis of India's DPDP Act 2023 and Data Localization
- **Verified Title:** A New Age of Data Privacy Laws in India: Review of Digital Personal Data Protection Act, 2023
- **Authors:** B. Nath, S. Dhar
- **Publication Venue:** International Journal of Law and Social Sciences (Vol. 10, Issue 1)
- **Year:** 2024
- **DOI:** [10.60143/ijls.v10.i1.2024.114](https://doi.org/10.60143/ijls.v10.i1.2024.114)
- **Main Contribution:** Analyzes the doctrinal shift in India's DPDP Act, 2023 from a mandatory data localization model to a government notification blacklist approach under Section 16, alongside mandatory fiduciary safeguards under Section 8.
- **Relevance to SovereigntyAI:** Directly validates the legal logic encoded into `POL-DPDP-001` and `POL-DPDP-002` in our engine.
- **Limitation / Research Gap:** Pure legal doctrinal analysis lacking software engineering tools or technical cloud architecture mapping.

### Paper 15: Explainable Ensemble Machine Learning for Risk Classification
- **Verified Title:** Explainable Ensemble Machine Learning Method for Credit Risk Classification
- **Authors:** Sirine Ben Ghozzi, Mohamed Aymen Ben Hajkacem, Essoussi Nadia
- **Publication Venue:** 2024 International Conference on INnovations in Intelligent SysTems and Applications (INISTA)
- **Year:** 2024
- **DOI:** [10.1109/INISTA62901.2024.10683830](https://doi.org/10.1109/INISTA62901.2024.10683830)
- **Main Contribution:** Combines ensemble machine learning classifiers with explainability techniques to produce auditable risk predictions in regulated decision-making environments.
- **Relevance to SovereigntyAI:** Validates our hybrid architecture combining an explainable scoring baseline with an advisory scikit-learn classifier.
- **Limitation / Research Gap:** Applied to financial loan default datasets rather than cloud security and cross-border data protection scenarios.

---

## 3. Comparative Literature Matrix

The matrix below contrasts state-of-the-art literature with the **SovereigntyAI** framework developed in this project:

| Publication / System | Focus Area | Jurisdictions Covered | Policy Evaluation Engine | Explainable Risk (XAI) | AWS Architecture Mapping | Local Offline Execution |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Ernstberger et al. (IEEE EuroS&P 2023)** | Formal Data Sovereignty Taxonomy | Generic / EU | Conceptual | No | No | No |
| **Zaguir et al. (IEEE Access 2024)** | Systematic GDPR Survey | EU | No (Survey) | No | No | No |
| **Yanagawa et al. (IEEE CLOUD 2024)** | GitOps Cloud Compliance | Generic Security | Rule-based (PVP) | No | Generic | Yes |
| **Galij et al. (MDPI App. Sci. 2024)** | Public Sovereign Clouds | EU / US | Comparative Analysis | No | Yes (Qualitative) | No |
| **Arreche et al. (IEEE Access 2024)** | Explainable AI (XAI) | N/A (Intrusion Detection) | No | Yes (SHAP/LIME) | No | Yes |
| **Nath & Dhar (IJLS 2024)** | Legal Analysis of DPDP Act | India | Doctrinal Law | No | No | No |
| **SovereigntyAI (This Project)** | **Autonomous Cloud Sovereignty Framework** | **EU GDPR, India DPDP Act, US HIPAA/PCI-DSS, Global** | **Deterministic Rule Engine (JSON-driven)** | **Deterministic 0-100 XAI Breakdown + ML Baseline** | **Full AWS Service Mapping (S3, RDS, Lambda, SageMaker, SNS)** | **Fully Local & Offline Python/Flask Prototype** |

---

## 4. Synthesis of Research Trends & Project Alignment

1. **Evolution from Localization to Governed Mobility:** The literature decisively shows that modern regulations (GDPR Chapter V, DPDP Act Sec 16) do not mandate blanket isolation of all digital bytes; they require *accountable, governed transfers* backed by approved safeguards (SCCs, adequacy) and technical supplementary measures. SovereigntyAI reflects this nuanced distinction.
2. **Imperative of Deterministic Rules in Compliance:** While machine learning is valuable for advisory triage, statutory decisions require deterministic, auditable rule evaluation to eliminate generative hallucinations and guarantee legal predictability.
3. **Transparent Risk Scoring:** Regulators and audit bodies reject black-box risk scores. By providing an itemized factor waterfall alongside actionable remediations, SovereigntyAI bridges cloud architecture engineering and compliance oversight.
