from backend.data.fixtures import SOURCES


def retrieve_sources(
    category: str,
    state: str,
    top_k: int = 3
):
    results = [
        source
        for source in SOURCES
        if source["category"] == category
        and (
            source["jurisdiction"] == state
            or source["jurisdiction"] == "PENDING_STATE_SELECTION"
        )
    ]

    return results[:top_k]