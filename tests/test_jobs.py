import pytest
from fastapi import status


@pytest.fixture
def auth_token(client):
    """Register and get auth token."""
    response = client.post(
        "/auth/register",
        json={
            "email": "recruiter@example.com",
            "password": "password123",
            "full_name": "Recruiter User",
            "role": "recruiter",
        },
    )
    return response.json()["access_token"]


def test_create_job(client, auth_token):
    """Test creating a job opening."""
    response = client.post(
        "/jobs",
        json={
            "title": "Senior Python Engineer",
            "description": "We are looking for a senior Python engineer with FastAPI experience",
            "department": "Engineering",
            "location": "San Francisco",
            "salary_min": 150000,
            "salary_max": 200000,
            "required_skills": "Python, FastAPI, PostgreSQL",
            "experience_level": "senior",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Senior Python Engineer"
    assert data["status"] == "open"
    assert data["is_active"] is True


def test_list_jobs(client, auth_token):
    """Test listing jobs."""
    # Create jobs
    for i in range(3):
        client.post(
            "/jobs",
            json={
                "title": f"Job {i}",
                "description": f"Description {i}",
                "department": "Engineering",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )

    # List jobs
    response = client.get(
        "/jobs",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3


def test_get_job(client, auth_token):
    """Test getting a specific job."""
    # Create job
    create_response = client.post(
        "/jobs",
        json={
            "title": "Senior Python Engineer",
            "description": "Job description",
            "department": "Engineering",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    job_id = create_response.json()["id"]

    # Get job
    response = client.get(
        f"/jobs/{job_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == job_id
    assert data["title"] == "Senior Python Engineer"


def test_update_job(client, auth_token):
    """Test updating a job."""
    # Create job
    create_response = client.post(
        "/jobs",
        json={
            "title": "Senior Python Engineer",
            "description": "Job description",
            "department": "Engineering",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    job_id = create_response.json()["id"]

    # Update job
    response = client.put(
        f"/jobs/{job_id}",
        json={
            "title": "Lead Python Engineer",
            "status": "closed",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Lead Python Engineer"
    assert data["status"] == "closed"


def test_delete_job(client, auth_token):
    """Test deleting a job."""
    # Create job
    create_response = client.post(
        "/jobs",
        json={
            "title": "Senior Python Engineer",
            "description": "Job description",
            "department": "Engineering",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    job_id = create_response.json()["id"]

    # Delete job
    response = client.delete(
        f"/jobs/{job_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK

    # Verify deletion
    get_response = client.get(
        f"/jobs/{job_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_create_application(client, auth_token):
    """Test creating an application."""
    # Create job
    job_response = client.post(
        "/jobs",
        json={
            "title": "Senior Python Engineer",
            "description": "Job description",
            "department": "Engineering",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    job_id = job_response.json()["id"]

    # Create candidate
    candidate_response = client.post(
        "/candidates",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    candidate_id = candidate_response.json()["id"]

    # Create application
    response = client.post(
        f"/jobs/{job_id}/applications",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["candidate_id"] == candidate_id
    assert data["job_id"] == job_id
    assert data["status"] == "applied"


def test_update_application_stage(client, auth_token):
    """Test updating application stage."""
    # Create job and candidate
    job_response = client.post(
        "/jobs",
        json={
            "title": "Senior Python Engineer",
            "description": "Job description",
            "department": "Engineering",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    job_id = job_response.json()["id"]

    candidate_response = client.post(
        "/candidates",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    candidate_id = candidate_response.json()["id"]

    # Create application
    app_response = client.post(
        f"/jobs/{job_id}/applications",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    application_id = app_response.json()["id"]

    # Update status
    response = client.patch(
        f"/jobs/applications/{application_id}/stage",
        json={"status": "shortlisted"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "shortlisted"
