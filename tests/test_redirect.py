import pytest


class TestRedirect:
    """Test suite for GET / endpoint"""

    def test_root_redirects_to_static_index(self, client):
        # Arrange
        expected_redirect_url = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == expected_redirect_url

    def test_root_redirect_follows_to_static_page(self, client):
        # Arrange
        # Act
        response = client.get("/", follow_redirects=True)

        # Assert
        assert response.status_code == 200
