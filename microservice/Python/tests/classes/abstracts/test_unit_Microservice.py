import pytest
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from starlette.datastructures import Headers
from starlette.requests import Request as StarletteRequest
from classes.abstracts.Microservice import Microservice
import logging

SECRET_KEY = "super-secret-key"

class DummyService(Microservice):
    def _addRoutes(self):
        self.availableRoutes["/ping"] = {
            "method": "GET",
            "function": self.ping,
            "description": "Health check"
        }

    def ping(self):
        return {"message": "pong"}

def make_request_with_token(token: str):
    headers = Headers({
        "Authorization": f"Bearer {token}"
    })
    scope = {
        "type": "http",
        "headers": headers.raw,
    }
    return StarletteRequest(scope)

def make_token(payload: dict, secret=SECRET_KEY, expired=False):
    now = datetime.now(timezone.utc)  # timezone-aware datetime

    if expired:
        payload["exp"] = now - timedelta(minutes=5)
    else:
        payload["exp"] = now + timedelta(minutes=5)

    return jwt.encode(payload, secret, algorithm="HS256")


@pytest.fixture
def dummy_service():
    return DummyService()


@pytest.mark.unit
def test_microservice_registers_routes(dummy_service):
    routes = [route for route in dummy_service.availableRoutes.keys()]
    assert "/ping" in routes

@pytest.mark.unit
def test_valid_jwt_token(dummy_service):
    token = make_token({"sub": "user123"})
    request = make_request_with_token(token)
    logging.warning(f"request {request}")
    payload = dummy_service._validate_internal_jwt(request, SECRET_KEY)
    assert payload["sub"] == "user123"

@pytest.mark.unit
def test_expired_jwt_token(dummy_service):
    token = make_token({"sub": "user123"}, expired=True)
    request = make_request_with_token(token)
    with pytest.raises(HTTPException) as exc_info:
        dummy_service._validate_internal_jwt(request, SECRET_KEY)
    assert exc_info.value.status_code == 403

@pytest.mark.unit
def test_missing_authorization_header(dummy_service):
    scope = {
        "type": "http",
        "headers": [],  # No headers
    }
    request = StarletteRequest(scope)
    with pytest.raises(HTTPException) as exc_info:
        dummy_service._validate_internal_jwt(request, SECRET_KEY)
    assert exc_info.value.status_code == 401

@pytest.mark.unit
def test_malformed_token(dummy_service):
    # Not a real JWT
    request = make_request_with_token("this.is.not.valid")
    with pytest.raises(HTTPException) as exc_info:
        dummy_service._validate_internal_jwt(request, SECRET_KEY)
    assert exc_info.value.status_code == 403
