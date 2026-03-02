import os

def test_dashboard_file_exists():
    assert os.path.exists("frontend/dashboard.html")

def test_dashboard_html_structure():
    with open("frontend/dashboard.html", "r") as f:
        content = f.read()
        assert "<!DOCTYPE html>" in content
        assert "static/css/tailwind.css" in content
        assert "Dashboard" in content
