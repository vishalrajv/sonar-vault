from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_page_bootstrap_links():
    """Verify that login.html contains links to local Bootstrap files."""
    response = client.get("/login")
    assert response.status_code == 200
    content = response.text
    assert 'href="static/vendor/bootstrap/bootstrap.min.css"' in content
    assert 'src="static/vendor/bootstrap/bootstrap.bundle.min.js"' in content
    assert 'static/css/tailwind.css' not in content

def test_login_page_bootstrap_classes():
    """Verify that login.html uses Bootstrap classes."""
    response = client.get("/login")
    assert response.status_code == 200
    content = response.text
    assert "card shadow-sm" in content
    assert "form-control" in content
    assert "form-check-input" in content
    assert "btn btn-primary" in content
    assert "alert alert-danger" in content
    assert "d-none" in content

def test_login_js_bootstrap_classes():
    """Verify that login.js uses Bootstrap classes for error handling."""
    # Since login.js is served as a static file
    response = client.get("/static/js/login.js")
    assert response.status_code == 200
    content = response.text
    assert "d-none" in content
    assert "hidden" not in content
