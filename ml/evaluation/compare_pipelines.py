
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from backend.services.agent import classify, analyze_case


ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = ROOT / "data" / "evaluation" / "scenarios.csv"
OUTPUT_DIR = ROOT / "artifacts" / "evaluation"


def main():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

    with DATASET_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        scenarios = list(csv.DictReader(file))

    if not scenarios:
        raise ValueError("The evaluation dataset contains no scenarios.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    comparison_rows = []

    for scenario in scenarios:
        scenario_id = scenario.get("scenario_id", "").strip()
        description = scenario.get("description", "").strip()
        state = scenario.get("state", "").strip()

        if not description or not state:
            comparison_rows.append({
                "scenario_id": scenario_id,
                "description": description,
                "state": state,
                "review_status": scenario.get("review_status", ""),
                "baseline_category": "",
                "baseline_confidence": "",
                "grounded_category": "",
                "grounded_confidence": "",
                "grounded_needs_clarification": "",
                "grounded_source_count": 0,
                "grounded_source_ids": "",
                "grounded_explanation": "",
                "grounded_uncertainty": "",
                "baseline_error": "Missing description or state",
                "grounded_error": "Missing description or state",
            })
            continue

        # Path A: classifier-only baseline.
        baseline_category = ""
        baseline_confidence = ""
        baseline_error = ""

        try:
            baseline_result = classify(description)
            baseline_category = baseline_result.category
            baseline_confidence = float(baseline_result.confidence)
        except Exception as exc:
            baseline_error = f"{type(exc).__name__}: {exc}"

        # Path B: existing classifier + HANA retrieval + explanation.
        grounded = {}
        grounded_error = ""

        try:
            grounded = analyze_case(description, state)
        except Exception as exc:
            grounded_error = f"{type(exc).__name__}: {exc}"

        sources = grounded.get("sources", [])

        comparison_rows.append({
            "scenario_id": scenario_id,
            "description": description,
            "state": state,
            "expected_category": scenario.get("expected_category", ""),
            "expected_action": scenario.get("expected_action", ""),
            "review_status": scenario.get("review_status", ""),
            "baseline_category": baseline_category,
            "baseline_confidence": baseline_confidence,
            "grounded_category": grounded.get("category", ""),
            "grounded_confidence": grounded.get("confidence", ""),
            "grounded_needs_clarification": grounded.get(
                "needs_clarification", ""
            ),
            "grounded_source_count": len(sources),
            "grounded_source_ids": ";".join(
                str(source.get("source_id", ""))
                for source in sources
            ),
            "grounded_explanation": grounded.get("explanation", ""),
            "grounded_uncertainty": grounded.get("uncertainty", ""),
            "baseline_error": baseline_error,
            "grounded_error": grounded_error,
        })

    output_csv = OUTPUT_DIR / "pipeline_comparison.csv"
    output_json = OUTPUT_DIR / "pipeline_comparison_summary.json"

    columns = list(comparison_rows[0].keys())

    with output_csv.open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(comparison_rows)

    total = len(comparison_rows)
    baseline_errors = sum(
        bool(row["baseline_error"]) for row in comparison_rows
    )
    grounded_errors = sum(
        bool(row["grounded_error"]) for row in comparison_rows
    )
    source_found = sum(
        int(row["grounded_source_count"]) > 0
        for row in comparison_rows
    )
    clarification_count = sum(
        row["grounded_needs_clarification"] is True
        for row in comparison_rows
    )
    category_agreements = sum(
        bool(row["baseline_category"])
        and row["baseline_category"] == row["grounded_category"]
        for row in comparison_rows
    )

    summary = {
        "evaluated_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": str(DATASET_PATH.relative_to(ROOT)),
        "total_scenarios": total,
        "reviewed_scenarios": sum(
            row.get("review_status", "").strip().lower() == "reviewed"
            for row in scenarios
        ),
        "comparison_type": (
            "classifier-only baseline versus current HANA-grounded "
            "pipeline; not an LLM-versus-RAG comparison"
        ),
        "baseline_errors": baseline_errors,
        "grounded_pipeline_errors": grounded_errors,
        "scenarios_with_grounded_sources": source_found,
        "scenarios_requesting_clarification": clarification_count,
        "baseline_grounded_category_agreements": category_agreements,
        "limitations": [
            "The scenarios are draft data and remain unreviewed.",
            "These outputs are exploratory, not validated performance metrics.",
            "Category agreement does not establish category correctness.",
            "A retrieved source does not establish legal correctness.",
            "Unsupported-claim rate requires human review of individual claims.",
            "The baseline is classifier-only, not an ungrounded LLM.",
        ],
    }

    with output_json.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, ensure_ascii=False)

    print("\n=== NyayaSetu Pipeline Comparison ===")
    print(f"Scenarios: {total}")
    print(f"Reviewed scenarios: {summary['reviewed_scenarios']}")
    print(f"Baseline errors: {baseline_errors}")
    print(f"Grounded pipeline errors: {grounded_errors}")
    print(f"Scenarios with sources: {source_found}/{total}")
    print(f"Clarification requests: {clarification_count}/{total}")
    print(f"Category agreements: {category_agreements}/{total}")
    print("\nSaved files:")
    print(output_csv)
    print(output_json)
    print("\nThese are exploratory results, not validated performance metrics.")


if __name__ == "__main__":
    main()
