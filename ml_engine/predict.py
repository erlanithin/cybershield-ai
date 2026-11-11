"""
CyberShield AI - Inference & Prediction Service
Handles text classification, confidence scoring, risk determination,
explainability highlights, and actionable guidance.
"""
from pathlib import Path
import joblib
import numpy as np

from ml_engine.preprocessing import clean_text, extract_trigger_words

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / 'models'

# Global cached model and vectorizer
_MODEL = None
_VECTORIZER = None


def load_artifacts():
    """Loads and caches the model and vectorizer."""
    global _MODEL, _VECTORIZER
    if _MODEL is None or _VECTORIZER is None:
        model_path = MODELS_DIR / 'cyberbullying_model.pkl'
        vec_path = MODELS_DIR / 'tfidf_vectorizer.pkl'

        if not model_path.exists() or not vec_path.exists():
            # Trigger training if artifacts don't exist yet
            from ml_engine.train_model import train_and_evaluate_models
            train_and_evaluate_models()

        _MODEL = joblib.load(model_path)
        _VECTORIZER = joblib.load(vec_path)
    return _MODEL, _VECTORIZER


def get_risk_profile(category: str, confidence: float) -> tuple:
    """
    Returns (risk_level, badge_css_class, color_hex, severity_rank)
    Risk levels:
    - Safe: Green (#20A67A)
    - Potentially Harmful: Orange (#F39C12)
    - High-Risk Content: Red (#E74C3C)
    """
    if category == "Normal / Safe":
        return "Safe", "badge-safe", "#20A67A", 1

    # Immediate high-risk categories
    if category in ["Threatening Language", "Sexual Harassment"]:
        return "High-Risk Content", "badge-high-risk", "#E74C3C", 3

    if category == "Hate Speech":
        if confidence >= 0.65:
            return "High-Risk Content", "badge-high-risk", "#E74C3C", 3
        return "Potentially Harmful", "badge-warning", "#F39C12", 2

    # Toxic, Harassment, Personal Attack
    if confidence >= 0.85:
        return "High-Risk Content", "badge-high-risk", "#E74C3C", 3

    return "Potentially Harmful", "badge-warning", "#F39C12", 2


def generate_explanation(category: str, confidence: float, triggers: list, text: str) -> str:
    """
    Generates a clear, transparent, explainable AI explanation for the user and moderator.
    """
    if category == "Normal / Safe":
        return (
            "The linguistic analysis did not detect patterns of hostility, harassment, "
            "slurs, or threatening terminology. The sentiment and phrasing align with standard, "
            "non-harmful communication."
        )

    trigger_phrase = ""
    if triggers:
        trigger_phrase = f" Significant trigger signals detected include: '{', '.join(triggers)}'."

    if category == "Threatening Language":
        return (
            f"The AI model identified direct or implied physical harm, violence, or intimidation.{trigger_phrase} "
            f"This content poses potential real-world safety hazards and requires urgent human review."
        )
    elif category == "Hate Speech":
        return (
            f"The message contains discriminatory, dehumanizing, or abusive language targeting identity, "
            f"ethnicity, religion, or protected attributes.{trigger_phrase}"
        )
    elif category == "Sexual Harassment":
        return (
            f"The message was flagged for non-consensual sexual advances, explicit coercion, or objectification.{trigger_phrase} "
            f"Such behavior violates digital safety norms."
        )
    elif category == "Harassment":
        return (
            f"The text exhibits persistent targeting, exclusion, or digital bullying aimed at distressing the recipient.{trigger_phrase}"
        )
    elif category == "Personal Attack":
        return (
            f"The message directly insults, demeans, or shames the recipient's appearance, intelligence, or dignity.{trigger_phrase}"
        )
    elif category == "Toxic / Abusive Language":
        return (
            f"The text contains aggressive profanity, hostility, or vulgar language intended to provoke or demean.{trigger_phrase}"
        )
    return f"The model detected abusive patterns characteristic of {category.lower()}.{trigger_phrase}"


def generate_recommendations(category: str, risk_level: str) -> list:
    """
    Provides practical, safety-first next steps for recipients or moderators.
    """
    if risk_level == "Safe":
        return [
            "Content meets platform safety guidelines.",
            "No moderation action required.",
            "Safe for standard interaction."
        ]

    if risk_level == "High-Risk Content":
        return [
            "Do not engage or respond to the aggressor directly.",
            "Take immediate screenshots with visible timestamps and username handles.",
            "File an urgent report with the platform safety team and consider law enforcement if physical danger is imminent.",
            "Block the sender across all communication channels.",
            "Reach out to trusted support, counselor, or digital safety helplines."
        ]

    # Potentially Harmful
    return [
        "Mute or block the offending account to stop incoming hostility.",
        "Submit a moderation report via CyberShield AI reporting tool.",
        "Set your social media account privacy to restricted or friends-only.",
        "Take a break from the conversation and avoid retaliating."
    ]


def predict_message(raw_text: str) -> dict:
    """
    End-to-end prediction pipeline for a single message.
    Returns structured results suitable for UI rendering and REST APIs.
    """
    if not raw_text or not raw_text.strip():
        return {
            "success": False,
            "error": "Message text cannot be empty."
        }

    model, vectorizer = load_artifacts()
    cleaned = clean_text(raw_text)

    # If completely stripped of words (e.g. only symbols)
    if not cleaned:
        cleaned = raw_text.lower().strip()

    X_vec = vectorizer.transform([cleaned])

    # Predict category
    predicted_category = model.predict(X_vec)[0]

    # Get class probabilities
    probabilities = {}
    confidence = 0.0

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X_vec)[0]
        classes = model.classes_
        for cls_name, prob in zip(classes, probs):
            probabilities[cls_name] = round(float(prob) * 100, 2)
        confidence = float(np.max(probs))
    else:
        # Fallback if probability not supported
        confidence = 0.85
        probabilities = {predicted_category: 85.0}

    # Format confidence percentage
    confidence_pct = round(confidence * 100, 1)

    # Risk level determination
    risk_level, badge_class, color_hex, severity_rank = get_risk_profile(
        predicted_category, confidence
    )

    # Explainability triggers
    triggers = extract_trigger_words(raw_text, predicted_category)

    # Human-readable explanation and recommendations
    explanation = generate_explanation(predicted_category, confidence, triggers, raw_text)
    recommendations = generate_recommendations(predicted_category, risk_level)

    return {
        "success": True,
        "original_text": raw_text,
        "cleaned_text": cleaned,
        "predicted_category": predicted_category,
        "confidence_score": confidence_pct,
        "risk_level": risk_level,
        "badge_class": badge_class,
        "color_hex": color_hex,
        "severity_rank": severity_rank,
        "explanation": explanation,
        "trigger_words": triggers,
        "probabilities": probabilities,
        "recommendations": recommendations,
        "disclaimer": "Predictions are AI-generated indicators to assist human review, not definitive legal judgments."
    }


def predict_batch(texts: list) -> list:
    """
    Batch prediction for lists of texts (e.g. CSV upload or bulk comments).
    """
    results = []
    for text in texts:
        if text and str(text).strip():
            res = predict_message(str(text))
            results.append(res)
    return results
