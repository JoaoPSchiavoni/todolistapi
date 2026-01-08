import pytest
from fastapi.testclient import TestClient

from todolist_api.app import app


@pytest.fixture
def client():
    return TestClient(app)
