from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpass123",
        },
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_register_duplicate_email():
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpass123",
        },
    )
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User 2",
            "password": "testpass456",
        },
    )
    assert response.status_code == 400


def test_login():
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpass123",
        },
    )
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpass123",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_password():
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpass123",
        },
    )
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401
