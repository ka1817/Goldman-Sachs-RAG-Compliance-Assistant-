import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure the project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app  # Import FastAPI app

client = TestClient(app)

def test_home():
    """Test the home ('/') endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Goldman Sachs Support Bot"}
