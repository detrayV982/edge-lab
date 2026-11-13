"""Builds the model-vs-market table for upcoming games."""
from statistics import mean

import pandas as pd

from edgelab.elo import build_ratings, home_win_probability, STARTING_RATING
from edgelab.odds_math import fair_probabilities
from edgelab.teams import to_abbreviation


# Finds the moneyline price one bookmaker offers for one team, or None if missing.
def find_price(bookmaker: dict, team_name: str) -> float | None:
    for market in bookmaker["markets"]:
        if market["key"] != "h2h":
            continue
        for outcome in market["outcomes"]:
            if outcome["name"] == team_name:
                return outcome["price"]
    return None


# Averages each bookmaker's margin-free home probability into one market consensus.
def market_home_probability(event: dict) -> float | None:
    probabilities = []
    for bookmaker in event["bookmakers"]:
        home_price = find_price(bookmaker, event["home_team"])
        away_price = find_price(bookmaker, event["away_team"])
        if home_price is None or away_price is None:
            continue
        probabilities.append(fair_probabilities(home_price, away_price)[0])
    return mean(probabilities) if probabilities else None


# Makes one table row: market probability, model probability, and the gap between them.
def build_row(event: dict, ratings: dict[str, float]) -> dict | None:
    market = market_home_probability(event)
    if market is None:
        return None
    home, away = to_abbreviation(event["home_team"]), to_abbreviation(event["away_team"])
    model = home_win_probability(
        ratings.get(home, STARTING_RATING), ratings.get(away, STARTING_RATING)
    )
    return {
        "kickoff": event["commence_time"], "away": away, "home": home,
        "market_home_prob": round(market, 3), "model_home_prob": round(model, 3),
        "model_minus_market": round(model - market, 3),
    }


# Compares the Elo model to the market for every event in the odds response.
def compare_to_market(events: list[dict], games: pd.DataFrame) -> pd.DataFrame:
    from edgelab.games import completed_games

    ratings = build_ratings(completed_games(games))
    rows = [build_row(event, ratings) for event in events]
    return pd.DataFrame([row for row in rows if row is not None])
