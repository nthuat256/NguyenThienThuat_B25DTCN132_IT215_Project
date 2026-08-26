import uuid

from conftest import auth_header, login


def test_get_current_user(client, user_token):
    response = client.get("/users/me", headers=auth_header(user_token))
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "nguyenvana@gmail.com"
    assert "password" not in data
    assert "password_hash" not in data


def test_update_current_user(client, user_token):
    new_name = f"Nguyen Van A Test {uuid.uuid4().hex[:8]}"
    response = client.put(
        "/users/me",
        headers=auth_header(user_token),
        json={"full_name": new_name},
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == new_name

    response = client.put(
        "/users/me",
        headers=auth_header(user_token),
        json={"full_name": "Nguyen Van A"},
    )
    assert response.status_code == 200


def test_get_users_requires_admin(client, user_token):
    response = client.get("/users/", headers=auth_header(user_token))
    assert response.status_code == 403


def test_admin_get_users(client, admin_token):
    response = client.get("/users/", headers=auth_header(admin_token))
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(user["email"] == "admin@gmail.com" for user in data)


def test_admin_search_users(client, admin_token):
    response = client.get(
        "/users/",
        headers=auth_header(admin_token),
        params={"q": "Nguyen Van"},
    )
    assert response.status_code == 200
    assert any("nguyen" in user["full_name"].lower() for user in response.json())


def test_admin_filter_active_users(client, admin_token):
    response = client.get(
        "/users/",
        headers=auth_header(admin_token),
        params={"is_active": False},
    )
    assert response.status_code == 200
    assert response.json()
    assert all(user["is_active"] is False for user in response.json())


def test_admin_get_user(client, admin_token):
    response = client.get("/users/3", headers=auth_header(admin_token))
    assert response.status_code == 200
    assert response.json()["email"] == "nguyenvana@gmail.com"


def test_admin_get_missing_user(client, admin_token):
    response = client.get("/users/999999999", headers=auth_header(admin_token))
    assert response.status_code == 404


def test_register_user(client):
    email = f"test_{uuid.uuid4().hex}@example.com"
    response = client.post(
        "/auth/register",
        json={"email": email, "full_name": "Test User", "password": "demo_password"},
    )
    assert response.status_code == 201
    assert response.json()["email"] == email


def test_register_duplicate_email(client):
    response = client.post(
        "/auth/register",
        json={"email": "admin@gmail.com", "full_name": "Another Admin", "password": "demo_password"},
    )
    assert response.status_code == 409


def test_login_invalid_password(client):
    response = client.post(
        "/auth/login",
        json={"email": "admin@gmail.com", "password": "wrong_password"},
    )
    assert response.status_code == 401


def test_login_inactive_user(client):
    response = client.post(
        "/auth/login",
        json={"email": "inactive.user@gmail.com", "password": "demo_password"},
    )
    assert response.status_code == 403


def test_get_me_without_token(client):
    response = client.get("/users/me")
    assert response.status_code == 403


def test_refresh_token_for_admin(client):
    response = client.post(
        "/auth/login",
        json={"email": "admin@gmail.com", "password": "demo_password"},
    )
    assert response.status_code == 200
    refresh_token = response.json()["refresh_token"]
    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert response.json()["access_token"]


def test_refresh_token_for_normal_user_is_rejected(client):
    token = login(client, "nguyenvana@gmail.com")
    response = client.post("/auth/refresh", json={"refresh_token": token})
    assert response.status_code == 401