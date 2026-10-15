# Machine Learning Model Artifacts (`src/ml_model`)

This directory contains the serialized machine learning model artifacts used by the advisory ML service in SovereigntyAI.

## Artifacts
- **`sovereignty_risk_model.joblib`:** Trained `scikit-learn` pipeline consisting of:
  - `preprocessor`: `ColumnTransformer` with `OneHotEncoder` for categorical inputs (`origin_jurisdiction`, `data_category`, `storage_region`, `backup_region`, `transfer_mechanism`, `framework`) and passthrough for boolean numeric flags.
  - `classifier`: `RandomForestClassifier` (100 estimators, max depth 12).
  - **Test Performance:** 96.25% Accuracy, 0.96 Macro F1.

## Training & Retraining
To retrain the model on the latest synthetic dataset:
```bash
python3 scripts/train_ml_model.py
```
To evaluate the model and print classification reports:
```bash
python3 scripts/evaluate_model.py
```
For complete empirical metrics, see `results/model_metrics.json` and `dataset/Dataset_Details.md`.
