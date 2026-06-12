def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    # Check if registration number is present
    assert "student" in data
    assert data["student"] != ""  # Should not be empty"# Health check tests" 
