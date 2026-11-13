"""Pulls NFL moneyline odds from The Odds API and caches every response to disk."""
import json
import os
from datetime import date
from pathlib import Path

import requests

ODDS_URL = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds"
RAW_DIRECTORY = Path("data/raw")


# Reads the API key from the environment or a local .env file; never prints it.
def load_api_key(env_path: Path = Path(".env")) -> str | None:
    if os.environ.get("ODDS_API_KEY"):
        return os.environ["ODDS_API_KEY"]
    if not env_path.exists():
        return None
    for line in env_path.read_text().splitlines():
        if line.startswith("ODDS_API_KEY="):
            return line.split("=", 1)[1].strip() or None
    return None


# Path of today's cache file, so a second run on the same day never spends another API call.
def cache_path_for(day: date, directory: Path = RAW_DIRECTORY) -> Path:
    return directory / f"odds_{day.isoformat()}.json"


# Calls the API once and returns the parsed JSON; only called when no cache exists.
def request_odds(api_key: str) -> list[dict]:
    parameters = {"apiKey": api_key, "regions": "us", "markets": "h2h", "oddsFormat": "american"}
    response = requests.get(ODDS_URL, params=parameters, timeout=30)
    response.raise_for_status()
    print("Odds API requests remaining:", response.headers.get("x-requests-remaining", "unknown"))
    return response.json()


# Returns today's odds from cache if present, otherwise makes one live call and caches it.
def get_odds(day: date | None = None, directory: Path = RAW_DIRECTORY) -> list[dict]:
    day = day or date.today()
    cache_file = cache_path_for(day, directory)
    if cache_file.exists():
        return json.loads(cache_file.read_text())
    api_key = load_api_key()
    if api_key is None:
        raise RuntimeError("No ODDS_API_KEY found. Put it in .env (see .env.example).")
    odds = request_odds(api_key)
    directory.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(odds))
    return odds
