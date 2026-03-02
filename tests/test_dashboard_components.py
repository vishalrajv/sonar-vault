"""Tests for the dashboard UI components."""

import os

def test_stat_cards_exist():
  """Verifies that the 4 stat cards exist in the dashboard HTML."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    # Check for 4 stat cards (using a common class or identifier)
    assert 'id="stat-cards-grid"' in content
    assert "Total Builds" in content
    assert "Active Ships" in content
    assert "Successful Uploads" in content
    assert "Pending Defects" in content

def test_activity_table_exists():
  """Verifies that the recent activity table exists in the dashboard HTML."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    assert 'id="activity-table"' in content
    assert "Recent Activity" in content
    assert "Ship" in content
    assert "Project" in content
    assert "Version" in content
    assert "Date" in content

def test_filters_exist():
  """Verifies that the filter header and dropdowns exist in the dashboard HTML."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    assert 'id="filters-header"' in content
    assert "Ship Name" in content
    assert "Sonar Project" in content
    assert "<select" in content

def test_refined_header_exists():
  """Verifies that the refined header elements exist in the dashboard HTML."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    assert "BSTC Admin" in content
    assert "Logout" in content
    assert "sticky top-0" in content

def test_charting_library_exists():
  """Verifies that the charting helper JS file exists."""
  assert os.path.exists("frontend/static/js/charting-helper.js")

def test_line_chart_exists():
  """Verifies that the line chart container exists in the dashboard HTML."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    assert 'id="line-chart"' in content
    assert "Software Uploads Over Time" in content

def test_bar_chart_exists():
  """Verifies that the bar chart container exists in the dashboard HTML."""
  with open("frontend/dashboard.html", "r") as f:
    content = f.read()
    assert 'id="bar-chart"' in content
    assert "Project Distribution" in content

def main():
  """Main entry point for running tests manually."""
  print("Running dashboard component tests...")
  # In a real environment, we'd use a test runner, but following style guide requirements.

if __name__ == '__main__':
  main()
