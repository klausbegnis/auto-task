import pytest
from classes.abstracts.Microservice import Microservice
import requests
import threading
import time

class DummyService(Microservice):
    def _addRoutes(self):
        self.availableRoutes["/ping"] = {
            "method": "GET",
            "function": self.ping,
            "description": "Health check"
        }

    def ping(self):
        return {"message": "pong"}

@pytest.mark.integration
def test_microservice_up_and_running():
    # Instantiate service on a different port to avoid collisions
    service = DummyService(port=8010)

    # Start FastAPI server in a background thread
    def run():
        service.run()  # this internally starts uvicorn

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    # Wait for the server to start
    time.sleep(1.5)

    # Make request to the service
    response = requests.get("http://localhost:8010/ping")

    # Assert response
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}
