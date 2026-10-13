from pathlib import Path

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from ml.preprocessing.text import normalize_text


ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = ROOT / "data" / "samples" / "scenarios.csv"
MODEL_PATH = ROOT / "ml" / "models" / "category_classifier.joblib"


def main():
    df = pd.read_csv(DATA_PATH)

    df["text"] = df["text"].apply(normalize_text)

    model = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    min_df=1
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000
                ),
            ),
        ]
    )

    model.fit(df["text"], df["category"])

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()