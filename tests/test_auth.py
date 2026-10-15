def test_register_and_login(client):
    r = client.post(
        "/api/v1/auth/register",
        json={
            "email": "a@b.com",
            "username": "abc",
            "password": "password123",
        },
    )
    assert r.status_code == 201
    assert r.json()["email"] == "a@b.com"

    r = client.post(
        "/api/v1/auth/login",
        data={
            "username": "a@b.com",
            "password": "password123",
        },
    )
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "x@y.com",
            "username": "xyz",
            "password": "password123",
        },
    )
    r = client.post(
        "/api/v1/auth/login",
        data={
            "username": "x@y.com",
            "password": "wrong",
        },
    )
    assert r.status_code == 401
