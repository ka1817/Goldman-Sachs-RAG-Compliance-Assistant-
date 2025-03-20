import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

def test_home_endpoint():
    """Test the home ('/') endpoint without starting backend"""
    with patch("main.app.get") as mock_get:
        mock_get.return_value = {"message": "Goldman Sachs Support Bot"}
        response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Goldman Sachs Support Bot"}

if __name__ == "__main__":
    pytest.main()
