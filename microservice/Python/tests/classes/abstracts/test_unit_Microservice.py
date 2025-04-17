import pytest
#from unittest.mock import MagicMock, patch
from classes.abstracts.Microservice import Microservice

class DummyService(Microservice):
    def _addRoutes(self):
        self.availableRoutes["/ping"] = {
            "method": "GET",
            "function": self.ping,
            "description": "Health check"
        }

    def ping(self):
        return {"message": "pong"}

def test_microservice_registers_routes():
    service = DummyService()

    routes = [route.path for route in service().routes]
    assert "/ping" in routes
