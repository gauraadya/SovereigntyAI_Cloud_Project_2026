# Processed Datasets Directory

This directory contains processed and benchmarked datasets used for training and evaluating machine learning baseline models in SovereigntyAI.

## Primary Dataset
- **File:** `synthetic_compliance_data.csv`
- **Samples:** 1,200 evaluated cloud deployment scenarios.
- **Generator Script:** `scripts/generate_dataset.py`
- **Target Label:** `compliance_status` (`COMPLIANT`, `NON_COMPLIANT`, `NEEDS_REVIEW`)
- **Features:** 10 deployment attributes including origin jurisdiction, data category, primary storage region, backup region, cross-border status, transfer mechanism, KMS encryption, IAM RBAC, and CloudTrail audit logging.

To regenerate the dataset:
```bash
python3 scripts/generate_dataset.py
```
For detailed schema and distribution analysis, see `dataset/Dataset_Details.md`.
