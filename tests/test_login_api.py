from fastapi.testclient import TestClient

def test_login_success(client):
    response = client.post("/api/v1/login", json={"username": "ADMIN000", "password": "adminpass"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client):
    response = client.post("/api/v1/login", json={"username": "ADMIN000", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect staff number or password"

def test_login_user_not_found(client):
    response = client.post("/api/v1/login", json={"username": "nonexistent", "password": "pwd"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect staff number or password"

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
