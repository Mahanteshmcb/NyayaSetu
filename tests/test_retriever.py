from rag.retriever import search_documents

def test_local_rent_retrieval_returns_dev_fixture():
    results = search_documents("My landlord refuses to return my deposit", "rent_or_deposit", "Karnataka", 3)
    assert results
    assert results[0]["provenance"] == "synthetic_development_fixture"
