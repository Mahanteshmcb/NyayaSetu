from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze():
    response = client.post(
        "/analyze",
        json={
            "description": "My employer has not paid my salary.",
            "state": "Karnataka"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["category"] == "unpaid_wages"
    assert "confidence" in data