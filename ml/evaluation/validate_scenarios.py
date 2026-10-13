
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = ROOT / "data" / "evaluation" / "scenarios.csv"

VALID_CATEGORIES = {
    "rent_or_deposit",
    "unpaid_wages",
    "termination",
    "workplace_harassment",
}

REQUIRED_COLUMNS = {
    "scenario_id",
    "description",
    "state",
    "expected_category",
    "expected_action",
    "required_facts",
    "review_status",
}


def main():
    with DATASET_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("The CSV file has no header.")

        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing_columns:
            raise ValueError(
                f"Missing columns: {sorted(missing_columns)}"
            )

        rows = list(reader)

    errors = []
    seen_ids = set()

    for line, row in enumerate(rows, start=2):
        scenario_id = row["scenario_id"].strip()
        category = row["expected_category"].strip()
        status = row["review_status"].strip().lower()

        if not scenario_id:
            errors.append(f"Line {line}: missing scenario_id")
        elif scenario_id in seen_ids:
            errors.append(f"Line {line}: duplicate ID {scenario_id}")
        seen_ids.add(scenario_id)

        if not row["description"].strip():
            errors.append(f"Line {line}: missing description")

        if category and category not in VALID_CATEGORIES:
            errors.append(
                f"Line {line}: invalid category {category}"
            )

        if status not in {"reviewed", "unreviewed"}:
            errors.append(
                f"Line {line}: invalid review_status {status}"
            )

    reviewed = sum(
        row["review_status"].strip().lower() == "reviewed"
        for row in rows
    )

    print(f"Total scenarios: {len(rows)}")
    print(f"Reviewed scenarios: {reviewed}")
    print(f"Unreviewed scenarios: {len(rows) - reviewed}")

    if errors:
        print("\nValidation errors:")
        for error in errors:
            print("-", error)
        raise SystemExit(1)

    print("\nDataset structure is valid.")
    print("Remember: structural validity does not verify labels.")


if __name__ == "__main__":
    main()
