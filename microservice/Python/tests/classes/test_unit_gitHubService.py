import pytest
import json
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone
import jwt
from classes.GitHubService import GitHubService

SECRET_KEY = "123ua8sd9123h1k!@#!K$1j"
TOKEN_FILE_PATH = '/home/token_bearer.json'  # This must match your code

# Function to create a JWT token
def make_token(data, secret=SECRET_KEY, expired=False):
    now = datetime.now(timezone.utc)  # timezone-aware datetime
    payload = data

    if expired:
        payload["exp"] = now - timedelta(minutes=5)  # Expired token
    else:
        payload["exp"] = now + timedelta(minutes=5)  # Valid token

    return jwt.encode(payload, secret, algorithm="HS256")


@pytest.fixture
def client():
    service = GitHubService()
    
    # Use the __call__ method to get the FastAPI app instance
    app = service()
    
    # Return the TestClient instance for FastAPI testing
    client = TestClient(app)
    
    yield client  # Use `yield` to ensure the test client is cleaned up properly after the test
    

@pytest.mark.unit
def test_list_reps_valid_token(client):
    # Generate a valid JWT token for 'klausbegnis'
    token = make_token({"sub":"klausbegnis"}, expired=False)
    
    # Request the /list-reps endpoint with the valid token in the Authorization header
    response = client.get("/list-reps", headers={"Authorization": f"Bearer {token}"})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.unit
def test_list_reps_invalid_token(client):
    # Generate an expired token for 'klausbegnis'
    token = make_token({"sub":"klausbegnis"}, expired=True)
    
    # Request the /list-reps endpoint with the expired token in the Authorization header
    response = client.get("/list-reps", headers={"Authorization": f"Bearer {token}"})
    
    # Assert that the response status code is 403 (Forbidden) since the token is expired
    assert response.status_code == 403


@pytest.mark.unit
def test_list_reps_missing_token(client):
    # Request the /list-reps endpoint without the Authorization header
    response = client.get("/list-reps")
    
    # Assert that the response status code is 401 (Unauthorized) because the token is missing
    assert response.status_code == 401

@pytest.mark.unit
def test_store_token(client):
    test_user = "test"
    test_git_token = "ghp_fakeToken123456"

    payload = {
        "sub" : test_user,
        "git_token" : test_git_token
    }

    token = make_token(payload, SECRET_KEY)

    response = client.post("/save-token", headers={"Authorization": f"Bearer {token}"})

    # Assert the response is 200 OK (or whatever you return, update if needed)
    assert response.status_code == 200 or response.status_code == 204

    # Now verify the file was written correctly
    with open(TOKEN_FILE_PATH, 'r') as f:
        data = json.load(f)
        assert test_user in data
        assert data[test_user]["token"] == test_git_token