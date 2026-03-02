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
