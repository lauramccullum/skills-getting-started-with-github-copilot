"""
Test module for successful API endpoint operations (happy path).

Tests are organized using the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and preconditions
- Act: Execute the API call
- Assert: Verify response status, content, and state changes
"""

import pytest


def test_get_activities_returns_all_activities(client, sample_activities):
    """
    Test that GET /activities returns all available activities with correct structure.
    
    AAA Pattern:
    - Arrange: sample_activities fixture provides the test data
    - Act: GET /activities
    - Assert: Response contains all activities with required fields
    """
    # Arrange (via fixtures)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "schedule" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_get_activities_has_correct_participant_count(client, sample_activities):
    """
    Test that GET /activities returns correct participant counts.
    
    AAA Pattern:
    - Arrange: sample_activities fixture with known participants
    - Act: GET /activities
    - Assert: Participant list matches fixture data
    """
    # Arrange (via fixtures)
    expected_chess_participants = sample_activities["Chess Club"]["participants"]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    data = response.json()
    actual_participants = data["Chess Club"]["participants"]
    assert actual_participants == expected_chess_participants
    assert len(actual_participants) == 2


def test_signup_successfully_registers_new_participant(
    client, sample_activities, test_activity_name, test_email
):
    """
    Test that POST /signup successfully registers a new participant.
    
    AAA Pattern:
    - Arrange: Fresh activities data and new email
    - Act: POST /signup for test activity
    - Assert: Status 200, success message, participant added to activity
    """
    # Arrange
    activity = test_activity_name
    email = test_email
    initial_count = len(sample_activities[activity]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]
    # Verify state change: participant added to activity
    assert email in sample_activities[activity]["participants"]
    assert len(sample_activities[activity]["participants"]) == initial_count + 1


def test_unregister_successfully_removes_participant(
    client, sample_activities, test_activity_name, existing_participant
):
    """
    Test that DELETE /unregister successfully removes a participant.
    
    AAA Pattern:
    - Arrange: Activity with known participant
    - Act: DELETE /unregister for existing participant
    - Assert: Status 200, success message, participant removed from activity
    """
    # Arrange
    activity = test_activity_name
    email = existing_participant
    initial_count = len(sample_activities[activity]["participants"])
    assert email in sample_activities[activity]["participants"]
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]
    # Verify state change: participant removed from activity
    assert email not in sample_activities[activity]["participants"]
    assert len(sample_activities[activity]["participants"]) == initial_count - 1
