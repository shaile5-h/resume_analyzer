from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "documentation" in data
    assert data["status"] == "operational"

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "app_name" in data

def test_list_resumes_empty():
    response = client.get("/api/v1/resumes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_bullet_rewriter_endpoint():
    payload = {
        "bullet_text": "worked on fixing bugs in python api",
        "target_role": "Backend Engineer"
    }
    response = client.post("/api/v1/copilot/rewrite-bullet", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["original_bullet"] == payload["bullet_text"]
    assert len(data["enhanced_variants"]) > 0
