import os

def test_dashboard_file_exists():
    assert os.path.exists("frontend/dashboard.html")

def test_dashboard_html_structure():
    with open("frontend/dashboard.html", "r") as f:
        content = f.read()
        assert "<!DOCTYPE html>" in content
        assert "static/css/tailwind.css" in content
        assert "Dashboard" in content
        assert "static/js/dashboard.js" in content
        assert 'id="sidebar"' in content
        assert 'id="sidebar-toggle"' in content

def test_dashboard_js_exists():
    assert os.path.exists("frontend/static/js/dashboard.js")

def test_static_asset_directories_exist():
    assert os.path.exists("frontend/static/fonts")
    assert os.path.exists("frontend/static/images")
