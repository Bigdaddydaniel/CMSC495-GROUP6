from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_grounded_answer():
    response = client.post("/chat", json={"customer_id": "demo-1", "message": "How do I reset my password?"})
    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "answered"
    assert body["source"] == "Account Support Policy"
    assert body["confidence"] > 0


def test_human_handoff_for_refund():
    response = client.post("/chat", json={"customer_id": "demo-2", "message": "I need a refund for my order"})
    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "escalated"
    assert body["ticket_id"].startswith("TKT-")


def test_unknown_question_escalates():
    response = client.post("/chat", json={"customer_id": "demo-3", "message": "Can you diagnose why my laptop fan rattles?"})
    assert response.status_code == 200
    assert response.json()["status"] == "escalated"
