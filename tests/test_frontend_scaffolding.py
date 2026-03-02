import os

def test_frontend_files_exist():
    assert os.path.exists("frontend/login.html")
    assert os.path.exists("frontend/static/css/tailwind.css")
    assert os.path.exists("frontend/static/js/login.js")

def test_login_html_content():
    with open("frontend/login.html", "r") as f:
        content = f.read()
        assert '<form id="login-form">' in content
        assert "static/css/tailwind.css" in content
        assert "static/js/login.js" in content

def test_login_js_content():
    with open("frontend/static/js/login.js", "r") as f:
        content = f.read()
        assert "login-form" in content
        assert "fetch('/api/v1/login'" in content
        assert "localStorage.setItem('access_token'" in content
