import os

def test_stat_cards_exist():
    with open("frontend/dashboard.html", "r") as f:
        content = f.read()
        # Check for 4 stat cards (using a common class or identifier)
        assert 'id="stat-cards-grid"' in content
        assert "Total Builds" in content
        assert "Active Ships" in content
        assert "Successful Uploads" in content
        assert "Pending Defects" in content

def test_activity_table_exists():
    with open("frontend/dashboard.html", "r") as f:
        content = f.read()
        assert 'id="activity-table"' in content
        assert "Recent Activity" in content
        assert "Ship" in content
        assert "Project" in content
        assert "Version" in content
        assert "Date" in content

def test_filters_exist():
    with open("frontend/dashboard.html", "r") as f:
        content = f.read()
        assert 'id="filters-header"' in content
        assert "Ship Name" in content
        assert "Sonar Project" in content
        assert "<select" in content
