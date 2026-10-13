def build_explanation(category: str, results: list[dict]) -> dict:
    if not results:
        return {
            "explanation": "",
            "uncertainty": (
                "No sufficiently relevant source was retrieved."
            ),
        }

    best = results[0]

    # These are development fixtures, not verified legal authorities.
    if best.get("authority") == "Development Fixture":
        explanation = (
            f"Your description appears related to "
            f"{category.replace('_', ' ')}. "
            f"The retrieved development material, "
            f"'{best['title']}', says that the outcome depends "
            f"on the agreement, the facts, and applicable law. "
            f"This material does not establish your legal rights "
            f"or determine the outcome of your dispute."
        )

        uncertainty = (
            "The retrieved material is a development fixture, "
            "not a verified legal authority. Applicable legal "
            "provisions and remedies have not yet been verified."
        )

        return {
            "explanation": explanation,
            "uncertainty": uncertainty,
        }

    return {
        "explanation": (
            f"Your description appears related to "
            f"{category.replace('_', ' ')}. "
            f"Retrieved source: {best['title']}."
        ),
        "uncertainty": (
            "The retrieved source must be checked for applicability "
            "to the facts and jurisdiction before drawing conclusions."
        ),
    }