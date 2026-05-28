import html
import re
from pathlib import Path

import joblib

from .suspicious_terms import SUSPICIOUS_TERMS


MODEL_PATH = Path("models/phishing_detector.joblib")


def load_model(model_path: Path = MODEL_PATH):
    if not model_path.exists():
        raise FileNotFoundError(
            "Trained model not found. Run `python train_model.py` before starting the app."
        )
    return joblib.load(model_path)


def predict_message(model, message: str) -> dict:
    clean_message = message.strip()
    if not clean_message:
        return {
            "label": "safe",
            "phishing_probability": 0.0,
            "safe_probability": 1.0,
        }

    probabilities = model.predict_proba([clean_message])[0]
    classes = list(model.classes_)

    phishing_index = classes.index(1)
    safe_index = classes.index(0)
    phishing_probability = float(probabilities[phishing_index])
    safe_probability = float(probabilities[safe_index])

    return {
        "label": "phishing" if phishing_probability >= 0.5 else "safe",
        "phishing_probability": phishing_probability,
        "safe_probability": safe_probability,
    }


def find_suspicious_terms(message: str) -> list[str]:
    lowered = message.lower()
    found = []
    for term in SUSPICIOUS_TERMS:
        if term in lowered:
            found.append(term)
    return found


def highlight_suspicious_terms(message: str) -> str:
    escaped = html.escape(message)
    terms = sorted(SUSPICIOUS_TERMS, key=len, reverse=True)

    for term in terms:
        pattern = re.compile(re.escape(html.escape(term)), re.IGNORECASE)
        escaped = pattern.sub(
            lambda match: f"<mark>{match.group(0)}</mark>",
            escaped,
        )

    return escaped.replace("\n", "<br>")


def risk_level(probability: float) -> tuple[str, str]:
    if probability >= 0.75:
        return "High Risk", "danger"
    if probability >= 0.45:
        return "Medium Risk", "warning"
    return "Low Risk", "safe"

