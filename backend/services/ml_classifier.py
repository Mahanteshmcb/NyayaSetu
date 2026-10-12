from pathlib import Path

import joblib


ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    ROOT
    / "ml"
    / "models"
    / "category_classifier.joblib"
)

_model = None


def get_model():
    global _model

    if _model is None:
        _model = joblib.load(MODEL_PATH)

    return _model


def predict_category(text: str):
    model = get_model()

    probabilities = model.predict_proba([text])[0]
    classes = model.classes_

    best_index = probabilities.argmax()

    return {
        "category": classes[best_index],
        "confidence": float(probabilities[best_index]),
    }