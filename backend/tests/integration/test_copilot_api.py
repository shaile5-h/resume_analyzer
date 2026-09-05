def test_rewrite_bullet_endpoint(client):
    payload = {
        "bullet_text": "built apis in python and fixed memory leaks",
        "target_role": "Senior Backend Engineer"
    }
    response = client.post("/api/v1/copilot/rewrite-bullet", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["original_bullet"] == payload["bullet_text"]
    assert len(data["enhanced_variants"]) >= 2
    assert any("XYZ" in v["formula"] or "Google" in v["formula"] for v in data["enhanced_variants"])

def test_interview_prep_endpoint(client):
    payload = {
        "role_title": "Full Stack Developer",
        "skills": ["Python", "FastAPI", "React"],
        "missing_skills": ["Kubernetes", "GraphQL"]
    }
    response = client.post("/api/v1/copilot/interview-prep", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["role_title"] == payload["role_title"]
    assert len(data["questions"]) >= 2
    categories = [q["category"] for q in data["questions"]]
    assert "Technical" in categories
