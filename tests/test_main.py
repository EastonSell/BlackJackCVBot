import json
import os
import sys
import pytest
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


def test_suggest_action_alias():
    payload = {"player_total": 10, "dealer_card": "Ace of Spades"}
    response = client.post("/suggest", json=payload)
    assert response.status_code == 200
    assert response.json()["action"] == "hit"


def test_layout_roundtrip():
    layout = {
        "dealer": {"x1": 0, "y1": 0, "x2": 10, "y2": 10},
        "players": [{"x1": 1, "y1": 1, "x2": 5, "y2": 5}],
    }
    response = client.post("/layout", json=layout)
    assert response.status_code == 200
    assert response.json() == layout

    response = client.get("/layout")
    assert response.status_code == 200
    assert response.json() == layout


def test_count_endpoints():
    client.post("/reset_count")
    client.post("/count", json={"card": "A"})
    response = client.get("/count")
    assert response.status_code == 200
    assert response.json()["count"] == -1


def test_card_aliases():
    client.post("/reset_count")
    client.post("/count", json={"card": "Ace of Spades"})
    response = client.get("/count")
    assert response.json()["count"] == -1
    client.post("/reset_count")
    client.post("/count", json={"card": "7c"})
    response = client.get("/count")
    assert response.json()["count"] == 0


def test_decks_and_true_count():
    client.post("/decks", json={"decks": 1})
    client.post("/reset_count")
    client.post("/count", json={"card": "5"})
    response = client.get("/true_count")
    assert response.status_code == 200
    true_count = response.json()["true_count"]
    assert isinstance(true_count, float)
    assert true_count > 1


def test_draw_page():
    response = client.get("/draw")
    assert response.status_code == 200
    assert "Table Layout" in response.text


def test_bounding_box_immutable():
    from dataclasses import FrozenInstanceError
    from app.main import BoundingBox

    bbox = BoundingBox(0, 0, 10, 10)
    with pytest.raises(FrozenInstanceError):
        bbox.x1 = 1
