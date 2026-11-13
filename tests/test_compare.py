import pandas as pd
import pytest

from edgelab.compare import compare_to_market, market_home_probability
from edgelab.games import completed_games, upcoming_games
from edgelab.odds_fetch import cache_path_for, get_odds

# Made-up sample in The Odds API response shape. Not real market data.
SAMPLE_EVENT = {
    "commence_time": "2026-11-15T18:00:00Z",
    "home_team": "Kansas City Chiefs", "away_team": "Buffalo Bills",
    "bookmakers": [{"key": "book", "markets": [{"key": "h2h", "outcomes": [
        {"name": "Kansas City Chiefs", "price": -110},
        {"name": "Buffalo Bills", "price": -110}]}]}],
}


def test_market_probability_even_market():
    assert market_home_probability(SAMPLE_EVENT) == pytest.approx(0.5)


def test_market_probability_none_without_bookmakers():
    assert market_home_probability({**SAMPLE_EVENT, "bookmakers": []}) is None


def test_compare_table_columns_and_gap():
    games = pd.DataFrame({
        "season": [2025], "gameday": ["2025-09-07"], "home_team": ["KC"], "away_team": ["BUF"],
        "home_score": [27], "away_score": [20],
    })
    table = compare_to_market([SAMPLE_EVENT], games)
    row = table.iloc[0]
    assert row["home"] == "KC" and row["away"] == "BUF"
    assert row["model_minus_market"] == pytest.approx(row["model_home_prob"] - row["market_home_prob"], abs=1e-3)


def test_completed_and_upcoming_split():
    games = pd.DataFrame({"home_score": [10.0, None], "away_score": [3.0, None]})
    assert len(completed_games(games)) == 1
    assert len(upcoming_games(games)) == 1


def test_cache_hit_makes_no_network_call(tmp_path, monkeypatch):
    from datetime import date
    import json
    day = date(2026, 11, 13)
    cache_path_for(day, tmp_path).write_text(json.dumps([SAMPLE_EVENT]))
    monkeypatch.setattr("edgelab.odds_fetch.request_odds", lambda key: pytest.fail("network called"))
    assert get_odds(day, tmp_path) == [SAMPLE_EVENT]
