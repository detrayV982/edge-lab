"""Baseline win-probability model: Elo ratings plus a home-field bonus."""
import pandas as pd

STARTING_RATING = 1500.0
HOME_FIELD_POINTS = 48.0  # Elo points of home advantage, roughly 2 to 3 points of spread
K_FACTOR = 20.0
SEASON_CARRYOVER = 0.75  # share of last season's rating kept after the offseason


# Probability the home team wins given both ratings and the home-field bonus.
def home_win_probability(home_rating: float, away_rating: float) -> float:
    difference = home_rating + HOME_FIELD_POINTS - away_rating
    return 1.0 / (1.0 + 10 ** (-difference / 400.0))


# Moves both ratings toward the actual result; bigger surprises move them more.
def update_ratings(home_rating: float, away_rating: float, home_won: float) -> tuple[float, float]:
    expected = home_win_probability(home_rating, away_rating)
    change = K_FACTOR * (home_won - expected)
    return home_rating + change, away_rating - change


# Pulls every rating part-way back to the mean at the start of a new season.
def regress_to_mean(ratings: dict[str, float]) -> dict[str, float]:
    return {
        team: STARTING_RATING + SEASON_CARRYOVER * (rating - STARTING_RATING)
        for team, rating in ratings.items()
    }


# Walks completed games in date order and returns the latest rating for every team.
def build_ratings(completed_games: pd.DataFrame) -> dict[str, float]:
    ratings: dict[str, float] = {}
    current_season = None
    for game in completed_games.sort_values("gameday").itertuples():
        if current_season is not None and game.season != current_season:
            ratings = regress_to_mean(ratings)
        current_season = game.season
        home = ratings.get(game.home_team, STARTING_RATING)
        away = ratings.get(game.away_team, STARTING_RATING)
        home_won = 0.5 if game.home_score == game.away_score else float(game.home_score > game.away_score)
        ratings[game.home_team], ratings[game.away_team] = update_ratings(home, away, home_won)
    return ratings


# Replays completed games in date order and records each game's ratings from BEFORE kickoff.
def elo_history(completed_games: pd.DataFrame) -> pd.DataFrame:
    ratings: dict[str, float] = {}
    current_season = None
    rows = []
    for game in completed_games.sort_values(["gameday", "game_id"]).itertuples():
        if current_season is not None and game.season != current_season:
            ratings = regress_to_mean(ratings)
        current_season = game.season
        home = ratings.get(game.home_team, STARTING_RATING)
        away = ratings.get(game.away_team, STARTING_RATING)
        rows.append({"game_id": game.game_id, "home_elo": home, "away_elo": away})
        home_won = 0.5 if game.home_score == game.away_score else float(game.home_score > game.away_score)
        ratings[game.home_team], ratings[game.away_team] = update_ratings(home, away, home_won)
    return pd.DataFrame(rows)
