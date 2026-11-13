"""Loads NFL game results and schedules from the free nflverse games file."""
from pathlib import Path

import pandas as pd

GAMES_URL = "https://raw.githubusercontent.com/nflverse/nfldata/master/data/games.csv"
GAMES_FILE = Path("data/raw/nflverse_games.csv")


# Downloads the nflverse games file once and reuses the saved copy afterward.
def load_games(path: Path = GAMES_FILE, refresh: bool = False) -> pd.DataFrame:
    if refresh or not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        pd.read_csv(GAMES_URL).to_csv(path, index=False)
    return pd.read_csv(path)


# Games that already have a final score; these are the only games the model may learn from.
def completed_games(games: pd.DataFrame) -> pd.DataFrame:
    return games.dropna(subset=["home_score", "away_score"])


# Games with no score yet, which are the ones we want predictions for.
def upcoming_games(games: pd.DataFrame) -> pd.DataFrame:
    return games[games["home_score"].isna()]
