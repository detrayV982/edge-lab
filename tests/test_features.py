"""Tests for the stats loader and the pre-game features, with a focus on never leaking the future."""
import pandas as pd

from edgelab import team_stats
from edgelab.elo import elo_history, STARTING_RATING
from edgelab.features import build_features
from edgelab.games import normalize_team_codes


# Makes a tiny schedule: team A hosts B, then B hosts A, then A hosts B, one week apart.
def make_games() -> pd.DataFrame:
    rows = []
    for index in range(4):
        home, away = ("AAA", "BBB") if index % 2 == 0 else ("BBB", "AAA")
        rows.append({
            "game_id": f"2020_{index + 1:02d}_{away}_{home}", "season": 2020, "week": index + 1,
            "gameday": f"2020-09-{10 + index * 7}", "home_team": home, "away_team": away,
            "home_score": 24, "away_score": 17, "home_rest": 7, "away_rest": 7,
        })
    return pd.DataFrame(rows)


# Makes matching weekly stats where every team-game has the given offensive EPA.
def make_stats(games: pd.DataFrame, epa_by_game: dict[str, float]) -> pd.DataFrame:
    rows = []
    for game in games.itertuples():
        for team, opponent in [(game.home_team, game.away_team), (game.away_team, game.home_team)]:
            rows.append({
                "season": game.season, "week": game.week, "team": team, "game_id": game.game_id,
                "season_type": "REG", "opponent_team": opponent, "attempts": 30, "carries": 20,
                "sacks_suffered": 0, "passing_epa": epa_by_game[game.game_id] * 50, "rushing_epa": 0.0,
                "sack_fumbles_lost": 0,
            })
    return pd.DataFrame(rows)


def test_offense_epa_is_divided_by_plays():
    stats = pd.DataFrame([{"attempts": 30, "carries": 20, "sacks_suffered": 0, "passing_epa": 10.0, "rushing_epa": 0.0}])
    assert abs(team_stats.add_offense_epa_per_play(stats)["offense_epa"][0] - 0.2) < 1e-9


def test_cached_season_makes_no_download(tmp_path, monkeypatch):
    cached = team_stats.stats_path(2020, tmp_path)
    cached.write_text("season\n2020\n")
    monkeypatch.setattr(pd, "read_csv", lambda *a, **k: (_ for _ in ()).throw(AssertionError("network used")))
    assert team_stats.download_season(2020, tmp_path) == cached


def test_old_team_codes_are_renamed():
    games = pd.DataFrame({"home_team": ["OAK", "SD"], "away_team": ["STL", "KC"]})
    result = normalize_team_codes(games)
    assert list(result["home_team"]) == ["LV", "LAC"] and list(result["away_team"]) == ["LA", "KC"]


def test_first_game_starts_at_default_rating_and_ignores_its_own_result():
    games = make_games()
    history = elo_history(games)
    assert history.loc[0, "home_elo"] == STARTING_RATING
    assert history.loc[1, "home_elo"] != STARTING_RATING  # the second game sees the first result


def test_features_do_not_change_when_a_later_game_changes():
    games = make_games()
    stats_before = make_stats(games, {game_id: 0.1 for game_id in games["game_id"]})
    later = dict.fromkeys(games["game_id"], 0.1)
    later[games["game_id"].iloc[3]] = 0.9  # change only the last game
    later_games = games.copy()
    later_games.loc[3, ["home_score", "away_score"]] = [0, 50]
    first = build_features(games, stats_before, games)
    second = build_features(later_games, make_stats(later_games, later), later_games)
    columns = ["elo_diff", "offense_diff", "defense_diff"]
    pd.testing.assert_frame_equal(first.loc[:2, columns], second.loc[:2, columns])


def test_a_games_own_stats_never_enter_its_own_features():
    games = make_games()
    steady = make_stats(games, {game_id: 0.1 for game_id in games["game_id"]})
    spiked = steady.copy()
    last = games.iloc[3]
    spiked.loc[(spiked["game_id"] == last["game_id"]) & (spiked["team"] == last["home_team"]), "passing_epa"] = 250.0
    first = build_features(games, steady, games)
    second = build_features(games, spiked, games)
    assert first.loc[3, "offense_diff"] == second.loc[3, "offense_diff"]
    assert first.loc[3, "defense_diff"] == second.loc[3, "defense_diff"]
