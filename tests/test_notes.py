def test_create_and_list_notes(auth_client):
    r = auth_client.post(
        "/api/v1/notes",
        json={
            "title": "Hello",
            "content": "World",
            "is_public": True,
        },
    )
    assert r.status_code == 201

    r = auth_client.get("/api/v1/notes")
    assert r.status_code == 200
    assert r.json()["total"] == 1


def test_unauthorized_create(client):
    r = client.post(
        "/api/v1/notes",
        json={
            "title": "x",
            "content": "y",
        },
    )
    assert r.status_code == 401
