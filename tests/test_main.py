import json
import os
import sys
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to BlackJackCVBot"}

def test_read_users():
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data
    assert all("id" in user and "name" in user for user in data)


def test_reset_count():
    response = client.post("/reset_count")
    assert response.status_code == 200
    assert response.json()["count"] == 0


def test_suggest_action():
    payload = {"player_total": 11, "dealer_card": "6"}
    response = client.post("/suggest", json=payload)
    assert response.status_code == 200
    assert response.json()["action"] in {"hit", "stand", "double"}
