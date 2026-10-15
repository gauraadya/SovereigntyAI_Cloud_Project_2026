# Final Project Presentation & Viva Voce Guide

This presentation guide provides a structured 12-slide presentation outline, speaking notes, and a live demonstration script for defending **SovereigntyAI** before examiners.

---

## 1. Slide Deck Structure (12 Slides)

### Slide 1: Title & Introduction
- **Title:** SovereigntyAI: Autonomous Cloud Data Sovereignty Compliance Framework
- **Subtitle:** Cross-Border Cloud Policy Intelligence & Explainable AI
- **Presenter:** Candidate / Student Name
- **Course:** Cloud Computing & Applied AI Engineering (2026)
- **Talking Points:** Introduce the core challenge: public clouds are borderless, but data privacy laws are fiercely bordered.

### Slide 2: The Core Problem: Cross-Border Cloud Sovereignty Collisions
- **Points:**
  - Multi-region hyperscale clouds (AWS) replicate data across globe.
  - EU GDPR Chapter V (Art 44–49) restricts transfers outside the EEA.
  - India DPDP Act 2023 Sec 16 introduces negative-list transfers & Sec 8 mandatory safeguards.
  - US HIPAA requires strict technical safeguards for healthcare data.
  - CSPM tools inspect open ports, not international transfer legality.

### Slide 3: Research Gap & Industry Dilemma
- **Points:**
  - Manual legal spreadsheet audits are slow and out of sync with DevOps pipelines.
  - Generative AI / LLMs suffer from legal hallucinations, non-determinism, and data privacy leakage.
  - Academic sovereign cloud projects (Gaia-X) are overly complex and not built for standard AWS regions.

### Slide 4: Proposed Solution & Core Innovation
- **Points:**
  - **SovereigntyAI:** A hybrid compliance framework combining:
    1. Deterministic statutory policy engine (formal JSON condition trees).
    2. Explainable AI (XAI) risk scoring algorithm (0–100 calibrated metric).
    3. Advisory scikit-learn machine learning baseline (Random Forest).
    4. Production-ready AWS architecture mappings.

### Slide 5: System Architecture & Data Flow
- **Points:** Present the Layered Architecture diagram from `architecture/System_Architecture.md`:
  - Presentation Layer &rarr; Flask WSGI &rarr; Policy Engine &rarr; Risk Engine &rarr; Advisory ML &rarr; SQLite / AWS S3 & SNS.

### Slide 6: The Policy Intelligence Engine
- **Points:**
  - Structure of `policies/policy_rules.json`.
  - Distinguishes *Verified Legal Requirements*, *Demonstration Rules*, and *Simplifying Assumptions*.
  - Nuanced handling: Does not falsely claim all data must be localized; validates SCCs, Adequacy Decisions, and BCRs.
  - Evaluates dual-region disaster recovery backup sovereignty.

### Slide 7: Explainable Risk Scoring Algorithm (XAI)
- **Points:**
  - Transparent formula: $\text{Base Sensitivity} + \sum \text{Penalties} - \sum \text{Mitigation Credits}$.
  - Defense-in-depth credits for AWS KMS encryption, IAM RBAC, and CloudTrail logging.
  - Statutory floor protection ($\ge 55$) prevents technical controls from masking an illegal transfer.

### Slide 8: Machine Learning Advisory Baseline
- **Points:**
  - Trained on 1,200 synthetic scenarios with stratified 80/20 train/test split.
  - Genuine test metrics: 96.25% Accuracy, 0.96 Macro F1.
  - Clearly positioned as an advisory heuristic that does not override statutory rule logic.
  - Graceful fallback if model artifact is absent.

### Slide 9: AWS Enterprise Blueprint
- **Points:** Present mapping to 10 AWS services: S3, RDS, Lambda, API Gateway, SageMaker, IAM, Cognito, CloudWatch, SNS, QuickSight.
  - Estimated pilot cost: ~$18.09/month (virtually free on AWS Free Tier).

### Slide 10: Live Demonstration Scenarios
- **Points:** Showcase the 6 pre-configured demonstration scenarios:
  1. Safe EU Local Storage (Compliant).
  2. Cross-Border Sensitive Health Transfer (Critical Non-Compliant).
  3. India DPDP Compliant Transfer with Contracts (Compliant).
  4. Weak Security Controls on US Financial Data (Non-Compliant).
  5. Risky Secondary Disaster Recovery Backup (Needs Review).
  6. Ambiguous / Underspecified Transfer (Needs Review).

### Slide 11: Automated Testing & Verification
- **Points:**
  - 22 automated tests executed via `unittest` / `run_tests.py` in 0.69s.
  - 100% pass rate across policy engine, risk calculation, database, web UI, REST API, and sample scenarios.

### Slide 12: Conclusion & Future Scope
- **Points:**
  - Successfully proved that cross-border cloud sovereignty can be automated deterministically and explained transparently.
  - Future Work: Terraform CI/CD pre-commit hooks and live AWS CloudTrail EventBridge streaming.

---

## 2. 5-Minute Live Demonstration Script for Examiners

1. **Step 1: Dashboard Overview (`http://127.0.0.1:5001/`)**
   - *"Here is the SovereigntyAI dashboard. We see real-time compliance metrics: total evaluations, compliant deployments, non-compliant breaches, and needs-review flags, alongside a fleet-wide risk distribution bar."*
2. **Step 2: Testing Scenario 1 (Compliant Baseline)**
   - Click **"Scenarios"** &rarr; Select **Scenario 1** (EuroHealth Logistics).
   - Show how the form inputs auto-populate.
   - Click **"⚡ Evaluate Sovereignty & Risk"**.
   - Show result: **Status COMPLIANT**, **Risk Score 0/100 (Low Risk)**.
   - Highlight: *"Because storage remains within the EEA (Frankfurt) and utilizes KMS encryption, all statutory checks pass."*
3. **Step 3: Testing Scenario 2 (Critical Violation)**
   - Click **Scenario 2** (Global MedTech Diagnostics: EU health records exported to US East without SCCs and unencrypted).
   - Click **"⚡ Evaluate"**.
   - Show result: **Status NON-COMPLIANT**, **Risk Score 100/100 (Critical Risk)**.
   - Highlight the **Contributing Factors Waterfall** and the failed checks under GDPR Chapter V and HIPAA.
4. **Step 4: Testing Scenario 5 (Secondary Backup Leakage)**
   - Click **Scenario 5** (Indic Retail: primary storage in Mumbai, but backup replicated to Virginia without transfer terms).
   - Show result: **Status NEEDS_REVIEW**, **Risk Score 50/100**.
   - Highlight: *"Our engine catches secondary backup leakage that conventional CSPM tools miss."*
5. **Step 5: Policy Explorer & Audit Export**
   - Navigate to **"Policy Explorer"**: Demonstrate live search by typing "GDPR" or "HIPAA".
   - Navigate to **"Audit History"**: Click **"Export CSV"** and **"Export JSON"** to demonstrate complete audit data portability.
