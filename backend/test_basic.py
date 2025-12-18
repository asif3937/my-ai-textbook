import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns a welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "RAG Chatbot" in response.json()["message"]

def test_health_endpoint():
    """Test the health endpoint returns correct status"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_liveness_endpoint():
    """Test the liveness endpoint returns correct status"""
    response = client.get("/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}

def test_readiness_endpoint():
    """Test the readiness endpoint returns correct status"""
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

if __name__ == "__main__":
    pytest.main()