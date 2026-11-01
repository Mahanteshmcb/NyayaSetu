<<<<<<< HEAD
from ml.classifier import predict_category

def test_rent_classification():
    assert predict_category("My landlord refuses to return my deposit.")["category"] == "rent_or_deposit"
def test_wage_classification():
    assert predict_category("My employer has not paid my salary")["category"] == "unpaid_wages"
def test_termination_classification():
    assert predict_category("I was terminated from my job")["category"] == "termination"
def test_unknown_classification():
    assert predict_category("I want to buy a bicycle")["category"] == "unknown"
=======
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
>>>>>>> origin/main
