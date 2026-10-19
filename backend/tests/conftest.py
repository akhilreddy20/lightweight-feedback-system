import os
import sys

import pytest
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("JWT_SECRET", "test-secret")

import database  # noqa: E402


@pytest.fixture()
def client(monkeypatch):
    """App wired to an in-memory MongoDB mock, fresh for every test."""
    db = AsyncMongoMockClient().feedback_system_test
    import auth
    import feedback

    for module in (database, auth, feedback):
        if hasattr(module, "users_collection"):
            monkeypatch.setattr(module, "users_collection", db.users)
        if hasattr(module, "feedbacks_collection"):
            monkeypatch.setattr(module, "feedbacks_collection", db.feedbacks)

    from main import app

    with TestClient(app) as c:
        yield c


def register(client, username, role, password="password123"):
    res = client.post("/register", json={"username": username, "password": password, "role": role})
    assert res.status_code == 201, res.text


def token_for(client, username, password="password123"):
    res = client.post("/login", json={"username": username, "password": password})
    assert res.status_code == 200, res.text
    return {"Authorization": f"Bearer {res.json()['token']}"}
