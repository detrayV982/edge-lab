"""Tests for predicting upcoming games from past results only."""
import pandas as pd
import pytest

from edgelab.upcoming import latest_form, upcoming_features


def test_unknown_team_gives_no_features():
    form = pd.DataFrame({"offense_epa": [0.1], "defense_epa_allowed": [0.0]}, index=["AAA"])
    assert upcoming_features("AAA", "ZZZ", {}, form) is None


def test_features_favor_the_better_home_team():
    form = pd.DataFrame({"offense_epa": [0.2, 0.0], "defense_epa_allowed": [-0.1, 0.1]}, index=["AAA", "BBB"])
    features = upcoming_features("AAA", "BBB", {"AAA": 1600.0, "BBB": 1500.0}, form)
    assert features["elo_diff"] == 100.0
    assert features["offense_diff"] == pytest.approx(0.2)
    assert features["defense_diff"] == pytest.approx(0.2)


def test_latest_form_averages_only_recent_games():
    games = pd.DataFrame({"game_id": ["g1", "g2"], "gameday": ["2020-09-10", "2020-09-17"]})
    rows = []
    for game_id, epa in [("g1", 10.0), ("g2", 0.0)]:
        for team, opponent in [("AAA", "BBB"), ("BBB", "AAA")]:
            rows.append({"game_id": game_id, "team": team, "opponent_team": opponent, "attempts": 25, "carries": 25,
                         "sacks_suffered": 0, "passing_epa": epa if team == "AAA" else 0.0, "rushing_epa": 0.0})
    form = latest_form(pd.DataFrame(rows), games)
    assert form.loc["AAA", "offense_epa"] == pytest.approx(0.1)  # (0.2 + 0.0) / 2
