"""Predicts upcoming games with the logistic model and lines them up against the live market."""
import pandas as pd

from edgelab.compare import market_home_probability
from edgelab.elo import build_ratings, home_win_probability, STARTING_RATING
from edgelab.features import FEATURE_COLUMNS, FORM_WINDOW, add_defense_allowed
from edgelab.games import completed_games, normalize_team_codes
from edgelab.model import predict_home_probability
from edgelab.team_stats import add_offense_epa_per_play
from edgelab.teams import to_abbreviation


# Each team's average offense and defense over its most recent games (all games played so far).
def latest_form(stats: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    table = add_defense_allowed(add_offense_epa_per_play(stats))
    table = table.merge(games[["game_id", "gameday"]], on="game_id").sort_values(["team", "gameday"])
    recent = table.groupby("team").tail(FORM_WINDOW)
    return recent.groupby("team")[["offense_epa", "defense_epa_allowed"]].mean()


# Feature row for one future game, built only from results that already happened.
def upcoming_features(home: str, away: str, ratings: dict[str, float], form: pd.DataFrame) -> dict | None:
    if home not in form.index or away not in form.index:
        return None
    home_rating, away_rating = ratings.get(home, STARTING_RATING), ratings.get(away, STARTING_RATING)
    return {
        "elo_diff": home_rating - away_rating,
        "offense_diff": form.loc[home, "offense_epa"] - form.loc[away, "offense_epa"],
        "defense_diff": form.loc[away, "defense_epa_allowed"] - form.loc[home, "defense_epa_allowed"],
        "rest_diff": 0.0,  # rest days are not in the odds feed, so assume equal rest
    }


# Builds the Elo vs model vs market table for every event that has a market and enough history.
def compare_upcoming(events: list[dict], games: pd.DataFrame, stats: pd.DataFrame, model) -> pd.DataFrame:
    finished = normalize_team_codes(completed_games(games))
    ratings, form = build_ratings(finished), latest_form(stats, finished)
    rows = []
    for event in events:
        home, away = to_abbreviation(event["home_team"]), to_abbreviation(event["away_team"])
        market, features = market_home_probability(event), upcoming_features(home, away, ratings, form)
        if market is None or features is None:
            continue
        model_probability = float(predict_home_probability(model, pd.DataFrame([features]))[0])
        elo = home_win_probability(ratings.get(home, STARTING_RATING), ratings.get(away, STARTING_RATING))
        rows.append({"kickoff": event["commence_time"], "away": away, "home": home,
                     "market": round(market, 3), "elo": round(elo, 3), "model": round(model_probability, 3),
                     "model_minus_market": round(model_probability - market, 3)})
    return pd.DataFrame(rows)
