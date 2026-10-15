# Raw Data Directory

## Acquisition Instructions & Notes

This directory is designated for raw source policy documents and external dataset inputs.

### 1. Investigation of OPP-115 Dataset
- **Resource:** Online Privacy Policies 115 (OPP-115) Dataset
- **Source:** Usable Privacy Policy Project ([usableprivacy.org/data](https://usableprivacy.org/data))
- **Status:** Investigated and analyzed. As documented in `dataset/Dataset_Details.md`, OPP-115 contains natural-language website privacy prose and lacks cloud infrastructure deployment features (AWS regions, KMS encryption, IAM RBAC, disaster recovery replication). It was therefore rejected for direct cloud compliance modeling to preserve scientific integrity.

### 2. Live Cloud Acquisition
To ingest raw cloud configuration snapshots from live AWS environments, use the AWS CLI:
```bash
aws s3api list-buckets --output json > dataset/raw/s3_buckets_raw.json
aws ec2 describe-regions --output json > dataset/raw/aws_regions_raw.json
```
These snapshots can be processed into deployment payloads evaluated by `policy_engine.py`.
