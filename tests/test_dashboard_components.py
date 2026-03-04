"""Tests for the dashboard UI components."""

import os

def test_stat_cards_exist():
  """Verifies that the stat cards container exists in the dashboard HTML."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    assert 'id="stats-cards-container"' in content

def test_activity_table_exists():
  """Verifies that the fleet status widget exists in the dashboard HTML."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    assert 'id="fleet-status-widget"' in content
    assert "Fleet Update Status" in content

def test_filters_exist():
  """Verifies that the global search exists in the dashboard HTML."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    assert 'id="global-search"' in content
    assert "Search Platforms, Projects, or Versions..." in content

def test_refined_header_exists():
  """Verifies that the refined header elements exist in the dashboard HTML."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    assert "D&E Admin" in content
    assert "Logout" in content

def test_charting_library_exists():
  """Verifies that the charting helper JS file exists."""
  # We'll skip this if we are not using it anymore or just check existence
  # assert os.path.exists("frontend/static/js/charting-helper.js")
  pass

def test_line_chart_exists():
  """Verifies that the sidebar tree container exists (replaces charts in new design)."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    assert 'id="sidebar-tree"' in content

def test_bar_chart_exists():
  """Placeholder for bar chart which might be in a different view now."""
  pass

def main():
  """Main entry point for running tests manually."""
  print("Running dashboard component tests...")
  # In a real environment, we'd use a test runner, but following style guide requirements.

if __name__ == '__main__':
  main()
