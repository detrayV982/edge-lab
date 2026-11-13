"""Prints the model-vs-market table. Uses cached odds; makes at most one live call per day."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from edgelab.compare import compare_to_market
from edgelab.games import load_games
from edgelab.odds_fetch import get_odds


# Loads odds and games, then prints the comparison table.
def main() -> None:
    table = compare_to_market(get_odds(), load_games())
    print(table.to_string(index=False) if len(table) else "No games with odds found.")


if __name__ == "__main__":
    main()
