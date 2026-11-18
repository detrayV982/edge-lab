"""Builds pre-game features. Every feature for a game uses only games played before it."""
import pandas as pd

from edgelab.elo import elo_history
from edgelab.games import normalize_team_codes
from edgelab.team_stats import add_offense_epa_per_play

FORM_WINDOW = 8  # how many past games count toward a team's recent form
MINIMUM_PAST_GAMES = 3
FEATURE_COLUMNS = ["elo_diff", "offense_diff", "defense_diff", "rest_diff"]


# Pairs each team-game with what the opponent's offense did in the same game (that is our defense).
def add_defense_allowed(stats: pd.DataFrame) -> pd.DataFrame:
    opponent = stats[["game_id", "team", "offense_epa"]].rename(
        columns={"team": "opponent_team", "offense_epa": "defense_epa_allowed"}
    )
    return stats.merge(opponent, on=["game_id", "opponent_team"], how="left")


# Rolling average of the last few games, shifted one game so the current game is never included.
def rolling_before_game(values: pd.Series) -> pd.Series:
    return values.shift(1).rolling(FORM_WINDOW, min_periods=MINIMUM_PAST_GAMES).mean()


# One row per team-game with that team's offense and defense form going into the game.
def team_form(stats: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    table = add_defense_allowed(add_offense_epa_per_play(stats))
    table = table.merge(games[["game_id", "gameday"]], on="game_id", how="inner")
    table = table.sort_values(["team", "gameday", "game_id"])
    by_team = table.groupby("team")
    table["offense_form"] = by_team["offense_epa"].transform(rolling_before_game)
    table["defense_form"] = by_team["defense_epa_allowed"].transform(rolling_before_game)
    return table[["game_id", "team", "offense_form", "defense_form"]]


# Attaches one side's form (home or away) to the game table under prefixed column names.
def attach_form(games: pd.DataFrame, form: pd.DataFrame, side: str) -> pd.DataFrame:
    renamed = form.rename(columns={
        "team": f"{side}_team", "offense_form": f"{side}_offense", "defense_form": f"{side}_defense",
    })
    return games.merge(renamed, on=["game_id", f"{side}_team"], how="left")


# Full feature table for every game in the schedule. Positive numbers favor the home team.
def build_features(games: pd.DataFrame, stats: pd.DataFrame, completed: pd.DataFrame) -> pd.DataFrame:
    games, completed = normalize_team_codes(games), normalize_team_codes(completed)
    form = team_form(stats, games)
    table = attach_form(attach_form(games, form, "home"), form, "away")
    table = table.merge(elo_history(completed), on="game_id", how="left")
    table["elo_diff"] = table["home_elo"] - table["away_elo"]
    table["offense_diff"] = table["home_offense"] - table["away_offense"]
    table["defense_diff"] = table["away_defense"] - table["home_defense"]
    table["rest_diff"] = (table["home_rest"].clip(upper=14) - table["away_rest"].clip(upper=14))
    return table
