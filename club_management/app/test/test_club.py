import uuid

from conftest import auth_header


def create_club(client, token, name=None):
    name = name or f"Test Club {uuid.uuid4().hex}"
    response = client.post(
        "/clubs/",
        headers=auth_header(token),
        json={"name": name, "description": "Club for automated tests"},
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_create_club(client, admin_token):
    club = create_club(client, admin_token)
    assert club["name"].startswith("Test Club")
    assert club["owner_id"]


def test_get_clubs(client, user_token):
    response = client.get("/clubs/", headers=auth_header(user_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_club_by_id(client, user_token):
    response = client.get("/clubs/1", headers=auth_header(user_token))
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_missing_club(client, user_token):
    response = client.get("/clubs/999999999", headers=auth_header(user_token))
    assert response.status_code == 404


def test_update_club_by_owner(client, admin_token):
    club = create_club(client, admin_token)
    new_name = f"Updated Club {uuid.uuid4().hex}"
    response = client.put(
        f"/clubs/{club['id']}",
        headers=auth_header(admin_token),
        json={"name": new_name, "description": "Updated"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == new_name
    assert response.json()["description"] == "Updated"


def test_update_club_by_non_owner(client, admin_token):
    response = client.put(
        "/clubs/2",
        headers=auth_header(admin_token),
        json={"name": "Should Not Update"},
    )
    assert response.status_code == 403


def test_delete_club_by_non_owner(client, user_token):
    response = client.delete("/clubs/1", headers=auth_header(user_token))
    assert response.status_code == 403


def test_add_member_by_owner(client, admin_token):
    club = create_club(client, admin_token)
    response = client.post(
        f"/clubs/{club['id']}/members",
        headers=auth_header(admin_token),
        json={"user_id": 11, "role": "MEMBER"},
    )
    assert response.status_code == 201
    assert response.json()["user_id"] == 11
    assert response.json()["club_id"] == club["id"]


def test_add_duplicate_member(client, admin_token):
    club = create_club(client, admin_token)
    first = client.post(
        f"/clubs/{club['id']}/members",
        headers=auth_header(admin_token),
        json={"user_id": 11, "role": "MEMBER"},
    )
    assert first.status_code == 201

    second = client.post(
        f"/clubs/{club['id']}/members",
        headers=auth_header(admin_token),
        json={"user_id": 11, "role": "MEMBER"},
    )
    assert second.status_code == 400


def test_add_missing_user(client, admin_token):
    club = create_club(client, admin_token)
    response = client.post(
        f"/clubs/{club['id']}/members",
        headers=auth_header(admin_token),
        json={"user_id": 999999999, "role": "MEMBER"},
    )
    assert response.status_code == 404


def test_add_member_by_non_owner(client, user_token):
    response = client.post(
        "/clubs/1/members",
        headers=auth_header(user_token),
        json={"user_id": 11, "role": "MEMBER"},
    )
    assert response.status_code == 403


def test_get_members(client, user_token):
    response = client.get("/clubs/1/members", headers=auth_header(user_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_members_missing_club(client, user_token):
    response = client.get("/clubs/999999999/members", headers=auth_header(user_token))
    assert response.status_code == 404


def test_delete_club_by_owner(client, admin_token):
    club = create_club(client, admin_token)
    response = client.delete(
        f"/clubs/{club['id']}",
        headers=auth_header(admin_token),
    )
    assert response.status_code == 204

    response = client.get(
        f"/clubs/{club['id']}",
        headers=auth_header(admin_token),
    )
    assert response.status_code == 200