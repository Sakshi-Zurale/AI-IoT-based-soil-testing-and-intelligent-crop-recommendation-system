import os
os.environ["DATABASE_URL"] = "sqlite:///./test_krushiai.db"
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_status():
    r = client.get("/api/system/status")
    assert r.status_code == 200
    assert "gateway" in r.json()
