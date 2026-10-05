from backend.main import app
from backend.services.agent import classify

def test_unpaid_wages():
    result = classify(
        "My employer has not paid my salary."
    )

    assert result.category == "unpaid_wages"


def test_rent():
    result = classify(
        "My landlord is refusing to return my deposit."
    )

    assert result.category == "rent_or_deposit"


def test_termination():
    result = classify(
        "I was terminated from my job."
    )

    assert result.category == "termination"


def test_harassment():
    result = classify(
        "My manager is harassing me at work."
    )

    assert result.category == "workplace_harassment"