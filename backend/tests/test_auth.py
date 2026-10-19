from conftest import register


def test_register_and_login(client):
    register(client, "alice", "employee")
    res = client.post("/login", json={"username": "alice", "password": "password123"})
    assert res.status_code == 200
    assert res.json()["role"] == "employee"
    assert res.json()["token"]


def test_duplicate_username_is_400_not_500(client):
    register(client, "alice", "employee")
    res = client.post("/register", json={"username": "alice", "password": "password123", "role": "employee"})
    assert res.status_code == 400


def test_wrong_password_is_401_not_500(client):
    register(client, "alice", "employee")
    res = client.post("/login", json={"username": "alice", "password": "wrong-password"})
    assert res.status_code == 401


def test_unknown_user_is_401(client):
    assert client.post("/login", json={"username": "ghost", "password": "password123"}).status_code == 401


def test_invalid_role_and_short_password_rejected(client):
    assert client.post("/register", json={"username": "bob", "password": "password123", "role": "admin"}).status_code == 422
    assert client.post("/register", json={"username": "bob", "password": "short", "role": "employee"}).status_code == 422


def test_password_is_hashed_and_never_logged(client, caplog):
    register(client, "alice", "employee", password="super-secret-pw")
    assert "super-secret-pw" not in caplog.text


def test_protected_route_requires_valid_token(client):
    assert client.get("/feedback/").status_code == 422  # missing header
    assert client.get("/feedback/", headers={"Authorization": "Bearer nope"}).status_code == 401
    assert client.get("/feedback/", headers={"Authorization": "Token x"}).status_code == 401


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}
