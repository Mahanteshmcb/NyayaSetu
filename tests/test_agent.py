from backend.services.agent import analyze_case

def test_analysis_discloses_fixture_provenance():
    result = analyze_case("My landlord refuses to return my security deposit", "Karnataka")
    assert result["category"] == "rent_or_deposit"
    if not result["needs_clarification"]:
        assert result["sources"]
        assert "synthetic" in result["explanation"].lower()
