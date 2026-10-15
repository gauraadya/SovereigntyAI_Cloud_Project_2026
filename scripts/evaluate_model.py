"""
Evaluation script for SovereigntyAI baseline model.
Reads results/model_metrics.json and prints detailed performance metrics.
"""

import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

def display_evaluation_results():
    if not config.ML_METRICS_PATH.exists():
        print("[Error] No evaluation metrics found. Please run scripts/train_ml_model.py first.")
        return

    with open(config.ML_METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    print("=" * 60)
    print(" SovereigntyAI ML Baseline Model Evaluation Summary")
    print("=" * 60)
    print(f"Model Type:      {metrics.get('model_type')}")
    print(f"Dataset:         {metrics.get('dataset')}")
    print(f"Train Samples:   {metrics.get('train_samples')}")
    print(f"Test Samples:    {metrics.get('test_samples')}")
    print(f"Overall Accuracy:{metrics.get('accuracy') * 100:.2f}%")
    print(f"Macro Avg F1:    {metrics.get('macro_avg_f1'):.4f}")
    print(f"Weighted Avg F1: {metrics.get('weighted_avg_f1'):.4f}")
    print("-" * 60)
    print("Per-Class Breakdown:")
    for cls_name, vals in metrics.get("per_class_metrics", {}).items():
        print(f"  [{cls_name}]")
        print(f"    Precision: {vals['precision'] * 100:.2f}%")
        print(f"    Recall:    {vals['recall'] * 100:.2f}%")
        print(f"    F1-Score:  {vals['f1_score']:.4f}")
        print(f"    Support:   {vals['support']}")
    print("-" * 60)
    print(f"Disclaimer: {metrics.get('disclaimer')}")
    print("=" * 60)

if __name__ == "__main__":
    display_evaluation_results()
