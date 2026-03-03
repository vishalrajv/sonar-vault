from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dashboard_page_bootstrap_links():
    """Verify that dashboard.html contains links to local Bootstrap files."""
    response = client.get("/dashboard")
    assert response.status_code == 200
    content = response.text
    assert 'href="static/vendor/bootstrap/bootstrap.min.css"' in content
    assert 'src="static/vendor/bootstrap/bootstrap.bundle.min.js"' in content
    assert 'static/css/tailwind.css' not in content

def test_dashboard_page_bootstrap_layout():
    """Verify that dashboard.html uses Bootstrap grid and components."""
    response = client.get("/dashboard")
    assert response.status_code == 200
    content = response.text
    assert "d-flex" in content
    assert "vh-100" in content
    assert "navbar" in content
    assert "container-fluid" in content
    assert "row" in content
    assert "col-12" in content
    assert "placeholder-glow" in content
    assert "modal fade" in content

def test_dashboard_js_bootstrap_classes():
    """Verify that dashboard.js uses Bootstrap classes for dynamic elements."""
    response = client.get("/static/js/dashboard.js")
    assert response.status_code == 200
    content = response.text
    assert "d-flex" in content
    assert "d-none" in content
    assert "progress-bar" in content
    assert "hidden" not in content
