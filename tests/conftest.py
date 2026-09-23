import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

# Save initial state of activities dictionary for isolation between test runs
_INITIAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities dictionary to its original state after each test."""
    activities.clear()
    activities.update(copy.deepcopy(_INITIAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(copy.deepcopy(_INITIAL_ACTIVITIES))


@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    with TestClient(app) as test_client:
        yield test_client
