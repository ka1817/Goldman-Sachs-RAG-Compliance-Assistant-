import pytest
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

# Create a test client
client = TestClient(app)

def test_home_endpoint():
    """Test the home ('/') endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Goldman Sachs Support Bot"}

def test_predict_valid_question():
    """Test the /predict endpoint with a valid question"""
    test_data = {"question": "How does Goldman Sachs ensure compliance in trading?"}
    response = client.post("/predict", json=test_data)
    
    assert response.status_code == 200
    assert "answer" in response.json()
    assert response.json()["answer"] != "I'm sorry, but I couldn't find relevant information in the retrieved documents."

def test_predict_invalid_input():
    """Test the /predict endpoint with an invalid input (empty question)"""
    test_data = {"question": ""}
    response = client.post("/predict", json=test_data)
    
    assert response.status_code == 200
    assert response.json()["answer"] == "I'm sorry, but I couldn't find relevant information in the retrieved documents."

def test_predict_no_context():
    """Test the /predict endpoint when no relevant documents are found"""
    test_data = {"question": "Tell me a joke about compliance."}
    response = client.post("/predict", json=test_data)
    
    assert response.status_code == 200
    assert response.json()["answer"] == "I'm sorry, but I couldn't find relevant information in the retrieved documents."

if __name__ == "__main__":
    pytest.main()
