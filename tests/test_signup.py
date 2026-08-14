import pytest


class TestSignup:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_valid_signup_adds_participant(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"

        # Verify participant was added
        activities_response = client.get("/activities")
        assert email in activities_response.json()[activity_name]["participants"]

    def test_duplicate_signup_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_for_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_multiple_students_different_activities(self, client):
        # Arrange
        students = [
            ("Programming Class", "student1@mergington.edu"),
            ("Programming Class", "student2@mergington.edu"),
            ("Drama Club", "student3@mergington.edu"),
        ]

        # Act
        for activity, email in students:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Assert
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        assert "student1@mergington.edu" in activities["Programming Class"]["participants"]
        assert "student2@mergington.edu" in activities["Programming Class"]["participants"]
        assert "student3@mergington.edu" in activities["Drama Club"]["participants"]
