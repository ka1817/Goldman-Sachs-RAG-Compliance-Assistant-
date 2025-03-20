import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app  # Import FastAPI app

client = TestClient(app)

# Mock ChatGroq to prevent API calls during tests
@pytest.fixture(autouse=True)
def mock_groq():
    with patch("main.ChatGroq") as mock:
        mock.return_value.predict.return_value = "Mocked response"
        yield mock

def test_health_check():
    """Test that the API health check endpoint is working"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Goldman Sachs Support Bot" in response.text

def test_another_get_endpoint():
    """Test another GET endpoint (replace with actual endpoint)"""
    response = client.get("/some-get-endpoint")  # Replace with an actual GET route
    assert response.status_code == 200
