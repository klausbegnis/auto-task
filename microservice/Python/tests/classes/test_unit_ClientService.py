import pytest
from fastapi.testclient import TestClient
from classes.ClientService import ClientService

@pytest.fixture
def client():
    service = ClientService()
    
    # Use the __call__ method to get the FastAPI app instance
    app = service()
    
    # Return the TestClient instance for FastAPI testing
    client = TestClient(app)
    yield client  # Use `yield` to ensure the test client is cleaned up properly after the test
    

@pytest.mark.unit
def test_register(client):
    # Sucessfully create an account
    data = {"user":"klausbegnis",
            "email":"klaus@begnis.com",
            "password" : "!nj1247681"}
    # Request the /register endpoint without token in the header
    response = client.post("/register", json=data)
    print("resopsta:",response)
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert response_data.get("user") == data.get("user")

    