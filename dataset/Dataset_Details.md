# Dataset Details & Empirical Evaluation Methodology

## 1. Investigation of OPP-115 Privacy Policy Dataset

As part of the initial data engineering phase for this project, the proposed **OPP-115 (Online Privacy Policies) Dataset** was investigated to determine its suitability for autonomous cloud data sovereignty evaluation.

### OPP-115 Dataset Profile & Facts
- **Dataset Name:** Online Privacy Policies 115 (OPP-115) Dataset
- **Authors / Research Group:** Usable Privacy Policy Project (Carnegie Mellon University, Fordham University, Stanford University)
- **Verified URL:** [https://usableprivacy.org/data](https://usableprivacy.org/data)
- **Nature of Data:** 115 natural-language website privacy policies annotated by law students with 3,792 fine-grained privacy practice segments across 10 categories (e.g., *First Party Collection/Use*, *Third Party Sharing/Collection*, *User Choice/Control*, *Data Retention*).
- **License:** Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).

### Technical Assessment & Incompatibility for Cloud Architecture Evaluation
1. **Domain Mismatch:** The OPP-115 corpus consists of unstructured English prose found on website privacy notices (e.g., terms of service and consumer disclosures). It contains text segments such as *"We may share your email with marketing partners."*
2. **Absence of Cloud Infrastructure Attributes:** OPP-115 **does not** contain technical cloud deployment tuples:
   - It contains no AWS region identifiers (`eu-central-1`, `ap-south-1`, `us-east-1`).
   - It contains no disaster recovery backup replication specifications.
   - It does not annotate whether server-side encryption with customer-managed keys (SSE-KMS) or AWS IAM role boundaries are enforced.
   - It lacks legal transfer mechanism indicators (such as European Commission Standard Contractual Clauses, Binding Corporate Rules, or DPDP Act Section 16 bilateral treaties).
3. **Conclusion:** Natural-language privacy policy text does **not** provide labels or features for determining whether an AWS S3 bucket or RDS instance complies with extraterritorial data localization laws. Attempting to force-fit OPP-115 text into cloud architecture validation would be scientifically dishonest and misleading.

Therefore, following academic standards, this limitation is clearly documented, and a transparent, reproducible **Synthetic Cloud Compliance Dataset** was constructed specifically for infrastructure evaluation.

---

## 2. SovereigntyAI Synthetic Cloud Compliance Dataset

### Overview
- **File Location:** `dataset/processed/synthetic_compliance_data.csv`
- **Dataset Purpose:** Benchmarking, policy engine validation, and training an exploratory scikit-learn machine learning baseline (`RandomForestClassifier`).
- **Generation Method:** Algorithmic generation via `scripts/generate_dataset.py`, evaluated through formal policy condition trees in `policy_engine.py` and calibrated by `risk_assessment.py`.
- **Sample Count:** 1,200 labeled cloud deployment scenarios.
- **Random Seed:** Reproducible (Seed 42).
- **Split Ratio:** Stratified 80% Training (960 records), 20% Holdout Testing (240 records).
- **License:** Open Academic Demonstration License (MIT equivalent).

### Schema & Feature Dictionary

| Feature Name | Data Type | Permissible Values / Domain | Description |
| :--- | :--- | :--- | :--- |
| `scenario_id` | String | `SYN-00001` to `SYN-01200` | Unique scenario identifier. |
| `origin_jurisdiction` | Categorical | `EU_EEA`, `IN`, `US_FED`, `US_CA`, `UK`, `GLOBAL_OTHER` | The primary legal jurisdiction where data subjects reside. |
| `data_category` | Categorical | `non_personal`, `personal`, `financial`, `healthcare`, `sensitive_personal` | Regulatory sensitivity classification of stored data assets. |
| `storage_region` | Categorical | Valid AWS Regions (e.g. `eu-central-1`, `ap-south-1`, `us-east-1`) | Primary AWS hosting region for S3, EBS, or RDS. |
| `backup_region` | Categorical | Valid AWS Region or `none` | Disaster recovery secondary replication target. |
| `cross_border` | Integer (0/1) | `0` (False), `1` (True) | Whether data leaves the domestic borders of the origin jurisdiction. |
| `transfer_mechanism`| Categorical | `adequate_country`, `scc`, `bcr`, `explicit_consent`, `statutory_exemption`, `none_unverified` | Legal instrument justifying cross-border transfer. |
| `encryption_at_rest` | Integer (0/1) | `0` (Disabled), `1` (Enabled) | Whether AWS KMS encryption at rest is enforced. |
| `access_control` | Integer (0/1) | `0` (Disabled), `1` (Enabled) | Whether least-privilege IAM RBAC / MFA is enforced. |
| `audit_logging` | Integer (0/1) | `0` (Disabled), `1` (Enabled) | Whether multi-region CloudTrail auditing is active. |
| `framework` | Categorical | `GDPR`, `DPDP Act 2023`, `HIPAA`, `PCI-DSS / ISO 27001`, `Cross-Border Standard` | Primary regulatory benchmark evaluated. |
| `risk_score` | Integer | `0` to `100` | Deterministic exposure score computed by explainable engine. |
| `risk_category` | Categorical | `Low`, `Moderate`, `High`, `Critical` | Calibrated risk exposure band. |
| `compliance_status` | Categorical | `COMPLIANT`, `NON_COMPLIANT`, `NEEDS_REVIEW` | **Target Label**: Statutory compliance determination. |

---

## 3. Class Balance and Distribution

| Compliance Status (Class) | Count in Dataset | Proportion (%) |
| :--- | :--- | :--- |
| **COMPLIANT** | 614 | 51.17% |
| **NEEDS_REVIEW** | 315 | 26.25% |
| **NON_COMPLIANT** | 271 | 22.58% |
| **Total** | **1,200** | **100.0%** |

---

## 4. Empirical ML Baseline Evaluation Results

The machine learning baseline was trained using `scripts/train_ml_model.py` and evaluated on the 20% holdout test set (240 samples):

```text
Model: scikit-learn Pipeline (ColumnTransformer + RandomForestClassifier)
Hyperparameters: n_estimators=100, max_depth=12, random_state=42

Evaluation Metrics on Unseen Test Split (N = 240):
- Overall Accuracy:        96.25%
- Macro Average F1-Score:  0.9602
- Weighted Avg F1-Score:   0.9623

Per-Class Detailed Performance:
┌───────────────┬───────────┬────────┬──────────┬─────────┐
│ Class         │ Precision │ Recall │ F1-Score │ Support │
├───────────────┼───────────┼────────┼──────────┼─────────┤
│ COMPLIANT     │   0.97    │  0.98  │   0.97   │   123   │
│ NEEDS_REVIEW  │   0.94    │  0.94  │   0.94   │    63   │
│ NON_COMPLIANT │   0.98    │  0.96  │   0.97   │    54   │
└───────────────┴───────────┴────────┴──────────┴─────────┘
```

### Critical Academic Disclaimer
The scikit-learn model achieves high accuracy because it models the underlying statistical correlations of our deterministic policy engine. However, in enterprise deployment, **this model is strictly advisory and exploratory**. It does **not** replace statutory policy checks, nor does it guarantee compliance in real-world legal proceedings. The deterministic rule engine (`policy_engine.py`) remains the authoritative decision mechanism.
