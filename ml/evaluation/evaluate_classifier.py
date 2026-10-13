from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split

from ml.preprocessing.text import normalize_text


ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = ROOT / "data" / "samples" / "scenarios.csv"


def main():
    df = pd.read_csv(DATA_PATH)

    df["text"] = df["text"].apply(normalize_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"],
        df["category"],
        test_size=0.25,
        random_state=42,
        stratify=df["category"],
    )

    model = joblib.load(
        ROOT / "ml" / "models" / "category_classifier.joblib"
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\nAccuracy:")
    print(accuracy_score(y_test, predictions))

    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    print("\nConfusion matrix:")
    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )


if __name__ == "__main__":
    main()