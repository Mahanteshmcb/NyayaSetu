from ml.classifier import predict_category

def test_rent_classification():
    assert predict_category("My landlord refuses to return my deposit.")["category"] == "rent_or_deposit"
def test_wage_classification():
    assert predict_category("My employer has not paid my salary")["category"] == "unpaid_wages"
def test_termination_classification():
    assert predict_category("I was terminated from my job")["category"] == "termination"
def test_unknown_classification():
    assert predict_category("I want to buy a bicycle")["category"] == "unknown"
