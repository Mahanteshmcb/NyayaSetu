
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from backend.services.agent import classify


ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = ROOT / "data" / "evaluation" / "scenarios.csv"
OUTPUT_DIR = ROOT / "artifacts" / "evaluation"

CATEGORIES = [
    "rent_or_deposit",
    "unpaid_wages",
    "termination",
    "workplace_harassment",
]


def main():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Evaluation dataset not found: {DATASET_PATH}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Only reviewed, labeled scenarios can be used for metrics.
    with DATASET_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        rows = list(csv.DictReader(file))

    reviewed_rows = [
        row
        for row in rows
        if row.get("review_status", "").strip().lower() == "reviewed"
        and row.get("expected_category", "").strip() in CATEGORIES
        and row.get("description", "").strip()
    ]

    if not reviewed_rows:
        raise ValueError(
            "No reviewed, labeled scenarios found. Add scenarios to "
            "data/evaluation/scenarios.csv and set review_status to "
            "'reviewed' only after their labels have been checked."
        )

    y_true = []
    y_pred = []
    prediction_rows = []

    for row in reviewed_rows:
        expected = row["expected_category"].strip()

        # The current classifier returns an object with attributes.
        result = classify(row["description"].strip())
        predicted = result.category
        confidence = float(result.confidence)

        y_true.append(expected)
        y_pred.append(predicted)

        prediction_rows.append(
            {
                "scenario_id": row.get("scenario_id", ""),
                "description": row["description"],
                "state": row.get("state", ""),
                "expected_category": expected,
                "predicted_category": predicted,
                "confidence": confidence,
                "correct": expected == predicted,
                "expected_action": row.get("expected_action", ""),
                "required_facts": row.get("required_facts", ""),
                "review_status": row.get("review_status", ""),
            }
        )

    labels = CATEGORIES + [
        label
        for label in sorted(set(y_true + y_pred))
        if label not in CATEGORIES
    ]

    accuracy = accuracy_score(y_true, y_pred)

    report = classification_report(
        y_true,
        y_pred,
        labels=labels,
        output_dict=True,
        zero_division=0,
    )

    matrix = confusion_matrix(
        y_true,
        y_pred,
        labels=labels,
    )

    predictions_path = OUTPUT_DIR / "classifier_predictions.csv"
    report_path = OUTPUT_DIR / "classifier_metrics.json"
    matrix_path = OUTPUT_DIR / "confusion_matrix.csv"

    pd.DataFrame(prediction_rows).to_csv(
        predictions_path,
        index=False,
        encoding="utf-8-sig",
    )

    matrix_df = pd.DataFrame(
        matrix,
        index=labels,
        columns=labels,
    )
    matrix_df.index.name = "actual_category"
    matrix_df.to_csv(matrix_path, encoding="utf-8-sig")

    metrics = {
        "evaluated_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": str(DATASET_PATH.relative_to(ROOT)),
        "evaluated_scenarios": len(reviewed_rows),
        "labels": labels,
        "accuracy": float(accuracy),
        "classification_report": report,
        "limitations": [
            "Metrics apply only to the reviewed scenarios in this run.",
            "A small or unrepresentative dataset cannot establish "
            "general model performance.",
            "Classification metrics do not measure retrieval relevance "
            "or legal correctness.",
        ],
    }

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2, ensure_ascii=False)

    print("\n=== NyayaSetu Classifier Evaluation ===")
    print(f"Reviewed scenarios: {len(reviewed_rows)}")
    print(f"Accuracy: {accuracy:.4f}")
    print("\nPer-category metrics:")
    print(
        classification_report(
            y_true,
            y_pred,
            labels=labels,
            zero_division=0,
        )
    )
    print("Confusion matrix (rows = actual, columns = predicted):")
    print(matrix_df.to_string())

    print("\nSaved evaluation artifacts:")
    print(predictions_path)
    print(report_path)
    print(matrix_path)


if __name__ == "__main__":
    main()
