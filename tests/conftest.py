import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture providing a TestClient with a fresh app instance for each test."""
    return TestClient(app)
