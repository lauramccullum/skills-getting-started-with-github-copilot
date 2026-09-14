"""
Test module for business logic and data integrity.

Tests are organized using the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up specific preconditions and scenarios
- Act: Execute API operations
- Assert: Verify data state, calculations, and integrity
"""

import pytest


def test_spots_remaining_calculated_correctly(
    client, sample_activities, test_activity_name
):
    """
    Test that available spots are calculated correctly.
    
    AAA Pattern:
    - Arrange: Get activity details
    - Act: GET /activities to retrieve spot information
    - Assert: Verify spots_remaining = max - actual participants
    """
    # Arrange
    activity = test_activity_name
    max_participants = sample_activities[activity]["max_participants"]
    current_participants = len(sample_activities[activity]["participants"])
    expected_spots = max_participants - current_participants
    
    # Act
    response = client.get("/activities")
    
    # Assert
    data = response.json()
    actual_spots = data[activity]["max_participants"] - len(data[activity]["participants"])
    assert actual_spots == expected_spots
    assert actual_spots > 0


def test_multiple_participants_can_register_for_same_activity(
    client, sample_activities, test_activity_name
):
    """
    Test that multiple different participants can register for the same activity.
    
    AAA Pattern:
    - Arrange: Multiple new email addresses
    - Act: Register each email for activity sequentially
    - Assert: All registrations succeed, all emails in participants list
    """
    # Arrange
    activity = test_activity_name
    new_emails = [
        "alice@mergington.edu",
        "bob@mergington.edu",
        "charlie@mergington.edu"
    ]
    initial_count = len(sample_activities[activity]["participants"])
    
    # Act & Assert for each email
    for email in new_emails:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        assert email in sample_activities[activity]["participants"]
    
    # Final assertion: all emails registered
    final_count = len(sample_activities[activity]["participants"])
    assert final_count == initial_count + len(new_emails)
    for email in new_emails:
        assert email in sample_activities[activity]["participants"]


def test_removal_updates_participant_list(
    client, sample_activities, test_activity_name, test_email
):
    """
    Test that participant removal properly updates the activity's participant list.
    
    AAA Pattern:
    - Arrange: Register a participant, verify they're in the list
    - Act: Register, then unregister the same participant
    - Assert: After unregister, email not in list; list size decreased by 1
    """
    # Arrange
    activity = test_activity_name
    email = test_email
    initial_count = len(sample_activities[activity]["participants"])
    
    # Act: Register participant
    response_signup = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response_signup.status_code == 200
    assert email in sample_activities[activity]["participants"]
    count_after_signup = len(sample_activities[activity]["participants"])
    
    # Act: Unregister participant
    response_unregister = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response_unregister.status_code == 200
    assert email not in sample_activities[activity]["participants"]
    count_after_unregister = len(sample_activities[activity]["participants"])
    assert count_after_signup == count_after_unregister + 1
    assert count_after_unregister == initial_count


def test_activity_data_isolation(
    client, sample_activities, test_email
):
    """
    Test that registering for one activity doesn't affect others.
    
    AAA Pattern:
    - Arrange: Get initial state of two activities
    - Act: Register participant in one activity
    - Assert: Other activity's participant list unchanged
    """
    # Arrange
    activity1 = "Chess Club"
    activity2 = "Programming Class"
    email = test_email
    initial_chess = sample_activities[activity1]["participants"].copy()
    initial_prog = sample_activities[activity2]["participants"].copy()
    
    # Act
    response = client.post(
        f"/activities/{activity1}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    # Activity 1 changed
    assert email in sample_activities[activity1]["participants"]
    # Activity 2 unchanged
    assert sample_activities[activity2]["participants"] == initial_prog
    assert email not in sample_activities[activity2]["participants"]


def test_unregister_doesnt_affect_other_participants(
    client, sample_activities, test_activity_name, existing_participant, test_email
):
    """
    Test that removing one participant doesn't affect others in the same activity.
    
    AAA Pattern:
    - Arrange: Add new participant to activity with existing participants
    - Act: Register new participant, then unregister them
    - Assert: Existing participants still registered in activity
    """
    # Arrange
    activity = test_activity_name
    new_email = test_email
    # Remember existing participants before test
    existing_participants = sample_activities[activity]["participants"].copy()
    
    # Act: Register new participant
    response_signup = client.post(
        f"/activities/{activity}/signup",
        params={"email": new_email}
    )
    assert response_signup.status_code == 200
    
    # Act: Unregister new participant
    response_unregister = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": new_email}
    )
    assert response_unregister.status_code == 200
    
    # Assert
    assert new_email not in sample_activities[activity]["participants"]
    # All original participants still there
    for original_email in existing_participants:
        assert original_email in sample_activities[activity]["participants"]
