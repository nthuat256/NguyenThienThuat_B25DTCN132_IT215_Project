import uuid

from conftest import auth_header


def create_club(client, token):
    response = client.post(
        "/clubs/",
        headers=auth_header(token),
        json={"name": f"Activity Test {uuid.uuid4().hex}", "description": "Test"},
    )
    assert response.status_code == 201, response.text
    return response.json()["id"]


def create_activity(client, token, club_id):
    response = client.post(
        f"/clubs/{club_id}/activities/",
        headers=auth_header(token),
        json={
            "title": f"Activity {uuid.uuid4().hex}",
            "description": "Automated test",
            "assignee_id": 3,
            "status": "TODO",
            "priority": "HIGH",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_create_activity(client, admin_token):
    club_id = create_club(client, admin_token)
    activity = create_activity(client, admin_token, club_id)
    assert activity["club_id"] == club_id
    assert activity["status"] == "TODO"


def test_get_activities(client, admin_token):
    club_id = create_club(client, admin_token)
    create_activity(client, admin_token, club_id)
    response = client.get(f"/clubs/{club_id}/activities/", headers=auth_header(admin_token))
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_activity_by_id(client, admin_token):
    club_id = create_club(client, admin_token)
    activity = create_activity(client, admin_token, club_id)
    response = client.get(
        f"/clubs/{club_id}/activities/{activity['id']}",
        headers=auth_header(admin_token),
    )
    assert response.status_code == 200
    assert response.json()["id"] == activity["id"]


def test_update_activity(client, admin_token):
    club_id = create_club(client, admin_token)
    activity = create_activity(client, admin_token, club_id)
    response = client.put(
        f"/clubs/{club_id}/activities/{activity['id']}",
        headers=auth_header(admin_token),
        json={"title": "Updated Activity", "status": "DONE", "priority": "LOW"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Activity"
    assert response.json()["status"] == "DONE"


def test_delete_activity(client, admin_token):
    club_id = create_club(client, admin_token)
    activity = create_activity(client, admin_token, club_id)
    response = client.delete(
        f"/clubs/{club_id}/activities/{activity['id']}",
        headers=auth_header(admin_token),
    )
    assert response.status_code == 204
    response = client.get(
        f"/clubs/{club_id}/activities/{activity['id']}",
        headers=auth_header(admin_token),
    )
    assert response.status_code == 404


def test_activity_requires_club_owner(client, user_token):
    response = client.get("/clubs/1/activities/", headers=auth_header(user_token))
    assert response.status_code == 403


def test_create_activity_requires_club_owner(client, user_token):
    response = client.post(
        "/clubs/1/activities/",
        headers=auth_header(user_token),
        json={"title": "Test"},
    )
    assert response.status_code == 403


def test_update_activity_requires_club_owner(client, user_token):
    response = client.put(
        "/clubs/1/activities/1",
        headers=auth_header(user_token),
        json={"title": "Test"},
    )
    assert response.status_code == 403


def test_delete_activity_requires_club_owner(client, user_token):
    response = client.delete("/clubs/1/activities/1", headers=auth_header(user_token))
    assert response.status_code == 403


def test_get_missing_activity(client, admin_token):
    club_id = create_club(client, admin_token)
    response = client.get(
        f"/clubs/{club_id}/activities/999999999",
        headers=auth_header(admin_token),
    )
    assert response.status_code == 404


def test_get_activity_from_wrong_club(client, admin_token):
    club_id = create_club(client, admin_token)
    activity = create_activity(client, admin_token, club_id)
    other_club_id = create_club(client, admin_token)
    response = client.get(
        f"/clubs/{other_club_id}/activities/{activity['id']}",
        headers=auth_header(admin_token),
    )
    assert response.status_code == 404


def test_missing_club_activity_endpoint(client, admin_token):
    response = client.get(
        "/clubs/999999999/activities/",
        headers=auth_header(admin_token),
    )
    assert response.status_code == 404