from fastapi.testclient import TestClient
from app.main import app
import pytest
from models.user import User
from app.auth_utils import hash_password

def test_dashboard_page_bootstrap_links(client, test_db):
    """Verify that dashboard.html contains links to local Bootstrap files."""
    # Seed user
    user = User(username="test_db_link", staff_number="T_LINK", hashed_password=hash_password("p"), role="user", is_approved=True, is_active=True)
    test_db.add(user)
    test_db.commit()
    
    # Login
    login_resp = client.post("/api/v1/login", json={"username": "T_LINK", "password": "p"})
    token = login_resp.json()["access_token"]
    
    response = client.get(f"/dashboard?token={token}")
    assert response.status_code == 200
    content = response.text
    assert 'href="static/vendor/bootstrap/bootstrap.min.css"' in content
    assert 'src="static/vendor/bootstrap/bootstrap.bundle.min.js"' in content

def test_dashboard_page_bootstrap_layout(client, test_db):
    """Verify that dashboard.html uses Bootstrap grid and components."""
    # Seed and login
    user = User(username="test_db_layout", staff_number="T_LAYOUT", hashed_password=hash_password("p"), role="user", is_approved=True, is_active=True)
    test_db.add(user)
    test_db.commit()
    login_resp = client.post("/api/v1/login", json={"username": "T_LAYOUT", "password": "p"})
    token = login_resp.json()["access_token"]

    response = client.get(f"/dashboard?token={token}")
    assert response.status_code == 200
    content = response.text
    assert "d-flex" in content
    assert "navbar" in content
    assert "row" in content

def test_dashboard_js_bootstrap_classes(client):
    """Verify that dashboard.js uses Bootstrap classes for dynamic elements."""
    response = client.get("/static/js/dashboard.js")
    assert response.status_code == 200
    content = response.text
    assert "d-flex" in content
    assert "d-none" in content
    assert "progress-bar" in content
