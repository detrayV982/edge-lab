"""Downloads and loads nflverse weekly team stats, one cached file per season."""
from pathlib import Path

import pandas as pd

STATS_URL = "https://github.com/nflverse/nflverse-data/releases/download/stats_team/stats_team_week_{season}.csv"
STATS_FOLDER = Path("data/raw")
FIRST_SEASON = 2006
KEPT_COLUMNS = [
    "season", "week", "team", "game_id", "season_type", "opponent_team", "attempts", "carries",
    "sacks_suffered", "passing_epa", "rushing_epa", "sack_fumbles_lost",
]


# Where the cached stats file for one season lives on disk.
def stats_path(season: int, folder: Path = STATS_FOLDER) -> Path:
    return folder / f"nflverse_team_stats_{season}.csv"


# Downloads one season of weekly team stats unless the file is already saved.
def download_season(season: int, folder: Path = STATS_FOLDER) -> Path:
    path = stats_path(season, folder)
    if path.exists():
        return path
    folder.mkdir(parents=True, exist_ok=True)
    pd.read_csv(STATS_URL.format(season=season)).to_csv(path, index=False)
    return path


# Loads every season from first to last into one table, keeping only the columns the model uses.
def load_team_stats(first: int, last: int, folder: Path = STATS_FOLDER) -> pd.DataFrame:
    frames = [pd.read_csv(download_season(season, folder), usecols=KEPT_COLUMNS) for season in range(first, last + 1)]
    return pd.concat(frames, ignore_index=True)


# Offensive expected points added per play for each team-game (pass, run and sack plays together).
def add_offense_epa_per_play(stats: pd.DataFrame) -> pd.DataFrame:
    plays = stats["attempts"] + stats["carries"] + stats["sacks_suffered"]
    result = stats.copy()
    result["offense_epa"] = (result["passing_epa"].fillna(0) + result["rushing_epa"].fillna(0)) / plays.where(plays > 0)
    return result
