import pandas as pd
import pytest

from edgelab.elo import (HOME_FIELD_POINTS, STARTING_RATING, build_ratings,
                         home_win_probability, regress_to_mean, update_ratings)


def test_equal_teams_favor_home():
    assert home_win_probability(1500, 1500) > 0.5


def test_home_field_bonus_is_applied():
    assert home_win_probability(1500 - HOME_FIELD_POINTS, 1500) == pytest.approx(0.5)


def test_update_is_zero_sum():
    new_home, new_away = update_ratings(1500, 1500, 1.0)
    assert new_home + new_away == pytest.approx(3000)


def test_winner_gains_rating():
    new_home, new_away = update_ratings(1500, 1500, 1.0)
    assert new_home > 1500 > new_away


def test_regress_moves_toward_mean():
    result = regress_to_mean({"A": 1600.0, "B": 1400.0})
    assert 1500 < result["A"] < 1600
    assert 1400 < result["B"] < 1500


def test_build_ratings_rewards_winner():
    games = pd.DataFrame({
        "season": [2025, 2025], "gameday": ["2025-09-07", "2025-09-14"],
        "home_team": ["A", "A"], "away_team": ["B", "B"],
        "home_score": [24, 20], "away_score": [10, 17],
    })
    ratings = build_ratings(games)
    assert ratings["A"] > STARTING_RATING > ratings["B"]
