import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""

    def test_get_all_activities_returns_correct_count(self, client):
        # Arrange
        expected_activity_count = 9

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert len(response.json()) == expected_activity_count

    def test_get_activities_returns_correct_structure(self, client):
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)

    def test_chess_club_has_initial_participants(self, client):
        # Arrange
        expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

        # Act
        response = client.get("/activities")
        chess_club = response.json()["Chess Club"]

        # Assert
        assert chess_club["participants"] == expected_participants
