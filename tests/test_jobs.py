from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def get_auth_token(role="hiring_manager"):
    client.post(
        "/auth/register",
        json={
            "email": f"test_{role}@example.com",
            "full_name": f"Test {role.replace('_', ' ').title()}",
            "password": "testpass123",
            "role": role,
        },
    )
    response = client.post(
        "/auth/login",
        json={
            "email": f"test_{role}@example.com",
            "password": "testpass123",
        },
    )
    return response.json()["access_token"]


def test_create_job():
    token = get_auth_token("hiring_manager")
    response = client.post(
        "/jobs",
        json={
            "title": "Senior Backend Engineer",
            "description": "Looking for an experienced engineer",
            "department": "Engineering",
            "location": "Remote",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Senior Backend Engineer"


def test_get_jobs():
    token = get_auth_token("hiring_manager")
    client.post(
        "/jobs",
        json={
            "title": "Product Manager",
            "description": "Lead our product strategy",
            "department": "Product",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.get(
        "/jobs",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1
