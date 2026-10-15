"""
Train scikit-learn ML Baseline for SovereigntyAI.
Trains a RandomForestClassifier on the synthetic compliance dataset to predict
compliance_status (COMPLIANT, NON_COMPLIANT, NEEDS_REVIEW).

Outputs:
- Saved pipeline model: src/ml_model/sovereignty_risk_model.joblib
- Evaluation metrics: results/model_metrics.json
"""

import json
from pathlib import Path
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

def train_baseline_model():
    dataset_path = config.BASE_DIR / "dataset" / "processed" / "synthetic_compliance_data.csv"
    if not dataset_path.exists():
        raise FileNotFoundError(f"Synthetic dataset not found at {dataset_path}. Run generate_dataset.py first.")

    df = pd.read_csv(dataset_path)
    print(f"[Training] Loaded dataset with {len(df)} samples.")
    print(f"[Training] Class distribution:\n{df['compliance_status'].value_counts()}\n")

    feature_cols = [
        "origin_jurisdiction",
        "data_category",
        "storage_region",
        "backup_region",
        "cross_border",
        "transfer_mechanism",
        "encryption_at_rest",
        "access_control",
        "audit_logging",
        "framework"
    ]
    
    target_col = "compliance_status"

    X = df[feature_cols]
    y = df[target_col]

    # Categorical and numerical columns
    categorical_cols = [
        "origin_jurisdiction",
        "data_category",
        "storage_region",
        "backup_region",
        "transfer_mechanism",
        "framework"
    ]
    numeric_cols = ["cross_border", "encryption_at_rest", "access_control", "audit_logging"]

    # Split dataset into train and test sets (80% train, 20% test, stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Preprocessing with ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ("num", "passthrough", numeric_cols)
        ]
    )

    # Model pipeline
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42))
        ]
    )

    # Train model
    print("[Training] Fitting RandomForestClassifier pipeline...")
    pipeline.fit(X_train, y_train)

    # Evaluate model
    y_pred = pipeline.predict(X_test)
    accuracy = float(accuracy_score(y_test, y_pred))
    report = classification_report(y_test, y_pred, output_dict=True)
    labels = sorted(list(y.unique()))
    cm = confusion_matrix(y_test, y_pred, labels=labels).tolist()

    print(f"[Evaluation] Accuracy: {accuracy * 100:.2f}%")
    print(f"[Evaluation] Classification Report:\n{classification_report(y_test, y_pred)}")

    # Genuine metrics dictionary
    metrics = {
        "model_type": "RandomForestClassifier (scikit-learn)",
        "dataset": "Synthetic Cloud Compliance Dataset (1200 samples)",
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": round(accuracy, 4),
        "macro_avg_f1": round(report["macro avg"]["f1-score"], 4),
        "weighted_avg_f1": round(report["weighted avg"]["f1-score"], 4),
        "labels": labels,
        "confusion_matrix": cm,
        "per_class_metrics": {
            lbl: {
                "precision": round(report[lbl]["precision"], 4),
                "recall": round(report[lbl]["recall"], 4),
                "f1_score": round(report[lbl]["f1-score"], 4),
                "support": int(report[lbl]["support"])
            }
            for lbl in labels if lbl in report
        },
        "disclaimer": "This baseline model is trained exclusively on synthetic rule-engine outputs for academic experimentation and comparison. It does not replace deterministic statutory rule evaluation."
    }

    # Save model artifact
    config.ML_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, config.ML_MODEL_PATH)
    print(f"[Artifact] Saved model pipeline to {config.ML_MODEL_PATH}")

    # Save metrics JSON
    config.ML_METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(config.ML_METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(f"[Artifact] Saved evaluation metrics to {config.ML_METRICS_PATH}")

    return metrics

if __name__ == "__main__":
    train_baseline_model()
