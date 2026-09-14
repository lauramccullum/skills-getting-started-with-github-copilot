"""
Test module for input validation and error handling.

Tests are organized using the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up invalid inputs or error conditions
- Act: Execute the API call with invalid data
- Assert: Verify appropriate error response codes and messages
"""

import pytest


def test_signup_duplicate_email_returns_400(
    client, sample_activities, test_activity_name, existing_participant
):
    """
    Test that POST /signup returns 400 when attempting to register duplicate email.
    
    AAA Pattern:
    - Arrange: Activity with existing participant
    - Act: POST /signup with same email already registered
    - Assert: Status 400 with error message
    """
    # Arrange
    activity = test_activity_name
    email = existing_participant
    assert email in sample_activities[activity]["participants"]
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already" in data["detail"].lower()


def test_signup_invalid_activity_returns_404(
    client, sample_activities, test_email
):
    """
    Test that POST /signup returns 404 for non-existent activity.
    
    AAA Pattern:
    - Arrange: Invalid activity name
    - Act: POST /signup for non-existent activity
    - Assert: Status 404 with error message
    """
    # Arrange
    activity = "Nonexistent Activity"
    email = test_email
    assert activity not in sample_activities
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_nonexistent_participant_returns_400(
    client, sample_activities, test_activity_name, test_email
):
    """
    Test that DELETE /unregister returns 400 when participant not registered.
    
    AAA Pattern:
    - Arrange: Activity and participant not in it
    - Act: DELETE /unregister for non-existent participant
    - Assert: Status 400 with error message
    """
    # Arrange
    activity = test_activity_name
    email = test_email
    assert email not in sample_activities[activity]["participants"]
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"].lower()


def test_unregister_invalid_activity_returns_404(
    client, sample_activities, existing_participant
):
    """
    Test that DELETE /unregister returns 404 for non-existent activity.
    
    AAA Pattern:
    - Arrange: Invalid activity name
    - Act: DELETE /unregister for non-existent activity
    - Assert: Status 404 with error message
    """
    # Arrange
    activity = "Nonexistent Activity"
    email = existing_participant
    assert activity not in sample_activities
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()
