from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_bootstrap_assets_exist():
    """Verify that Bootstrap assets are present in the filesystem."""
    assert os.path.exists("frontend/static/vendor/bootstrap/bootstrap.min.css")
    assert os.path.exists("frontend/static/vendor/bootstrap/bootstrap.bundle.min.js")
    assert os.path.exists("frontend/static/vendor/bootstrap/popper.min.js")

def test_bootstrap_assets_served():
    """Verify that Bootstrap assets are correctly served by the FastAPI app."""
    response_css = client.get("/static/vendor/bootstrap/bootstrap.min.css")
    assert response_css.status_code == 200
    assert "text/css" in response_css.headers["content-type"]

    response_js = client.get("/static/vendor/bootstrap/bootstrap.bundle.min.js")
    assert response_js.status_code == 200
    assert "application/javascript" in response_js.headers["content-type"]

    response_popper = client.get("/static/vendor/bootstrap/popper.min.js")
    assert response_popper.status_code == 200
    assert "application/javascript" in response_popper.headers["content-type"]

def test_index_html_bootstrap_links():
    """Verify that index.html contains links to local Bootstrap files."""
    response = client.get("/")
    assert response.status_code == 200
    content = response.text
    assert 'href="static/vendor/bootstrap/bootstrap.min.css"' in content
    assert 'src="static/vendor/bootstrap/bootstrap.bundle.min.js"' in content
    assert "bg-light" in content
    assert "d-flex" in content
