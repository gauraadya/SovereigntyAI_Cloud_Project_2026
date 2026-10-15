"""
AI Services Module for SovereigntyAI.
Wraps the scikit-learn model artifact to provide advisory ML inference alongside
the deterministic policy engine. Handles model loading, inference caching,
and graceful fallback when the model artifact is absent.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import config

# Try importing ML dependencies safely
_MODEL = None
_MODEL_LOAD_ATTEMPTED = False

def _get_ml_pipeline():
    """Lazy-load the trained scikit-learn pipeline."""
    global _MODEL, _MODEL_LOAD_ATTEMPTED
    if _MODEL_LOAD_ATTEMPTED:
        return _MODEL

    _MODEL_LOAD_ATTEMPTED = True
    if not config.ML_MODEL_PATH.exists():
        return None

    try:
        import joblib
        _MODEL = joblib.load(config.ML_MODEL_PATH)
        return _MODEL
    except Exception as e:
        print(f"[AIServices] Could not load ML model: {e}")
        return None

def predict_compliance_ml(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run advisory inference on the submitted deployment payload using the trained ML model.
    Returns:
        - model_available: bool
        - predicted_status: str or None
        - confidence: float (0.0 to 1.0)
        - class_probabilities: Dict[str, float]
        - advisory_note: str
    """
    pipeline = _get_ml_pipeline()
    if pipeline is None:
        return {
            "model_available": False,
            "predicted_status": None,
            "confidence": 0.0,
            "class_probabilities": {},
            "advisory_note": "ML model artifact is not available. Assessment relies solely on deterministic policy rules."
        }

    try:
        import pandas as pd
        
        # Prepare single row DataFrame matching pipeline feature columns
        df = pd.DataFrame([{
            "origin_jurisdiction": payload.get("origin_jurisdiction", "GLOBAL_OTHER"),
            "data_category": payload.get("data_category", "personal"),
            "storage_region": payload.get("storage_region", "us-east-1"),
            "backup_region": payload.get("backup_region", "none") or "none",
            "cross_border": 1 if payload.get("cross_border") else 0,
            "transfer_mechanism": payload.get("transfer_mechanism", "none_unverified"),
            "encryption_at_rest": 1 if payload.get("encryption_at_rest") else 0,
            "access_control": 1 if payload.get("access_control") else 0,
            "audit_logging": 1 if payload.get("audit_logging") else 0,
            "framework": payload.get("framework", "General Data Sovereignty")
        }])

        pred_class = pipeline.predict(df)[0]
        classes = pipeline.classes_
        proba = pipeline.predict_proba(df)[0]
        
        class_probs = {cls_name: round(float(prob), 4) for cls_name, prob in zip(classes, proba)}
        confidence = round(float(max(proba)), 4)

        return {
            "model_available": True,
            "predicted_status": str(pred_class),
            "confidence": confidence,
            "class_probabilities": class_probs,
            "advisory_note": (
                "Advisory Machine Learning baseline prediction trained on synthetic compliance data. "
                "Serves as an exploratory benchmark and does not override statutory policy rule decisions."
            )
        }
    except Exception as e:
        return {
            "model_available": False,
            "predicted_status": None,
            "confidence": 0.0,
            "class_probabilities": {},
            "advisory_note": f"ML inference failed with error: {str(e)}"
        }

def compare_engine_and_ml(deterministic_status: str, ml_status: Optional[str]) -> Dict[str, Any]:
    """Compare deterministic policy decision with ML advisory prediction for XAI explanation."""
    if not ml_status:
        return {
            "consensus": True,
            "explanation": "Assessment relies solely on deterministic statutory logic."
        }
        
    match = (deterministic_status == ml_status)
    if match:
        explanation = (
            f"Consensus reached: Both the deterministic policy engine and the scikit-learn model "
            f"concur on '{deterministic_status}'."
        )
    else:
        explanation = (
            f"Divergence detected: Policy engine determined '{deterministic_status}' based on specific "
            f"statutory clauses, whereas ML heuristic predicted '{ml_status}'. In all compliance contexts, "
            f"the deterministic statutory check takes legal precedence."
        )
        
    return {
        "consensus": match,
        "explanation": explanation
    }
