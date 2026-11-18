"""Compares Elo, the logistic model and the market for upcoming games. Uses cached odds (max 1 live call per day)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evaluate_week7 import load_labeled
from edgelab.games import load_games
from edgelab.model import fit_model, time_split
from edgelab.odds_fetch import get_odds
from edgelab.team_stats import load_team_stats
from edgelab.upcoming import compare_upcoming


# Trains on seasons through 2022, then prints the upcoming-games table.
def main() -> None:
    games = load_games()
    model = fit_model(time_split(load_labeled())[0])
    stats = load_team_stats(2006, int(games["season"].max()))
    table = compare_upcoming(get_odds(), games, stats, model)
    print(table.to_string(index=False) if len(table) else "No upcoming games with odds found.")
    print(f"{len(table)} games; mean absolute model-market gap {table['model_minus_market'].abs().mean():.3f}")


if __name__ == "__main__":
    main()
