from fastapi.testclient import TestClient
<<<<<<< HEAD
from backend.main import app
client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"
def test_root():
    assert client.get("/").status_code == 200
def test_analyze_validation():
    r = client.post("/analyze", json={"description":"hi", "state":"Karnataka"})
    assert r.status_code == 422

def test_templates_catalog():
    r = client.get('/api/templates')
    assert r.status_code == 200
    assert {x['id'] for x in r.json()['templates']} == {'representation', 'notice_reply', 'evidence_checklist'}

def test_knowledge_sources_endpoint():
    r = client.get('/api/knowledge/sources')
    assert r.status_code == 200
    assert 'sources' in r.json()
=======

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
>>>>>>> origin/main
