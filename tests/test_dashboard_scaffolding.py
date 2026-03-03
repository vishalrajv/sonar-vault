"""Tests for the dashboard scaffolding and offline integrity."""

import os

def test_dashboard_file_exists():
  """Verifies that the dashboard HTML file exists."""
  assert os.path.exists("frontend/dashboard.html")

def test_dashboard_html_structure():
  """Verifies the basic HTML structure and links in dashboard.html."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    assert "<!DOCTYPE html>" in content
    assert "static/css/tailwind.css" in content
    assert "Dashboard" in content
    assert "static/js/dashboard.js" in content
    assert 'id="sidebar"' in content
    # New design requirements
    assert 'id="sidebar-tree"' in content
    assert 'id="global-search"' in content
    assert 'id="user-profile-menu"' in content
    assert 'id="stats-cards-container"' in content
    assert 'id="fleet-status-widget"' in content

def test_dashboard_theme_colors():
  """Verifies the dashboard theme colors from the design doc."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    # Design doc specifies Emerald-900 (#064E3B) for sidebar and Emerald-600 for active stats
    # We'll check for the tailwind class equivalents if they are used directly in HTML
    # or just check if the Emerald palette is present.
    assert "emerald-900" in content.lower() or "emerald-600" in content.lower()

def test_dashboard_js_exists():
  """Verifies that the dashboard JS file exists."""
  assert os.path.exists("frontend/static/js/dashboard.js")

def test_static_asset_directories_exist():
  """Verifies that the static asset directories for fonts and images exist."""
  assert os.path.exists("frontend/static/fonts")
  assert os.path.exists("frontend/static/images")

def test_offline_integrity():
  """Verifies that no external asset links (http/https) are used."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    # Check for asset links starting with http or https
    assert 'src="http' not in content
    assert 'href="http' not in content

def test_basic_accessibility():
  """Performs a basic check for accessibility (e.g., alt tags)."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    # Basic check for image alt tags (if any img tags are used)
    if "<img" in content:
      assert 'alt="' in content

def test_js_initialization():
  """Verifies that key JS elements are initialized in dashboard.js."""
  with open("frontend/static/js/dashboard.js", "r") as f:
    content = f.read()
    assert "globalSearch" in content
    assert "fleetData" in content
    assert "renderTree" in content
    assert "statsData" in content
    assert "fleetStatusData" in content

def main():
  """Main entry point for running tests manually."""
  print("Running dashboard scaffolding tests...")

if __name__ == '__main__':
  main()
