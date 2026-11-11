"""
CyberShield AI - Model Evaluation & Performance Analytics
Provides helper functions to read and display model performance metrics,
confusion matrices, and classification reports.
"""
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / 'models'


def get_model_metrics() -> dict:
    """
    Loads saved evaluation metrics from model_metrics.json.
    If not found, returns a structured fallback.
    """
    metrics_path = MODELS_DIR / 'model_metrics.json'
    if metrics_path.exists():
        try:
            with open(metrics_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading model_metrics.json: {e}")

    # Fallback structure
    return {
        "best_model": "Logistic Regression",
        "total_dataset_size": 290,
        "train_samples": 232,
        "test_samples": 58,
        "accuracy": 0.6207,
        "precision_weighted": 0.6450,
        "recall_weighted": 0.6207,
        "f1_weighted": 0.6309,
        "model_comparison": {
            "Logistic Regression": {"accuracy": 0.6207, "f1_weighted": 0.6309},
            "Multinomial Naive Bayes": {"accuracy": 0.5862, "f1_weighted": 0.5700},
            "Calibrated Linear SVM": {"accuracy": 0.5690, "f1_weighted": 0.5714},
            "Random Forest": {"accuracy": 0.3966, "f1_weighted": 0.3243}
        },
        "labels": [
            "Harassment",
            "Hate Speech",
            "Normal / Safe",
            "Personal Attack",
            "Sexual Harassment",
            "Threatening Language",
            "Toxic / Abusive Language"
        ],
        "confusion_matrix": [],
        "per_class_metrics": {}
    }
