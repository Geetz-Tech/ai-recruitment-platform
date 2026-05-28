from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def get_auth_token():
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpass123",
            "role": "recruiter",
        },
    )
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpass123",
        },
    )
    return response.json()["access_token"]


def test_create_candidate():
    token = get_auth_token()
    response = client.post(
        "/candidates",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "555-1234",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"


def test_get_candidates():
    token = get_auth_token()
    client.post(
        "/candidates",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.get(
        "/candidates",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1
