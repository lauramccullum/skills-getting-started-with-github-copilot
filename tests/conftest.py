"""
Pytest configuration and shared fixtures for API tests.
Provides TestClient instance and sample test data.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a FastAPI TestClient instance for making HTTP requests in tests.
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Provide a fresh copy of the activities database for each test.
    This ensures test isolation - modifications in one test don't affect others.
    
    Returns the activities dict and resets it after the test completes.
    """
    # Store original state
    original_activities = {
        name: {
            "description": activity["description"],
            "schedule": activity["schedule"],
            "max_participants": activity["max_participants"],
            "participants": activity["participants"].copy()
        }
        for name, activity in activities.items()
    }
    
    yield activities
    
    # Restore original state after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def test_activity_name():
    """
    Provide a known activity name for use in tests.
    """
    return "Chess Club"


@pytest.fixture
def test_email():
    """
    Provide a test email address for sign-up tests.
    """
    return "test.student@mergington.edu"


@pytest.fixture
def existing_participant():
    """
    Provide an email of a participant already signed up for Chess Club.
    """
    return "michael@mergington.edu"
