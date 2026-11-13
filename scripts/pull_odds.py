"""Pulls one week of NFL odds and caches it to data/raw/. Safe to re-run: cache wins."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from edgelab.odds_fetch import get_odds


# Fetches (or reads cached) odds and reports how many games came back.
def main() -> None:
    print(f"{len(get_odds())} games with odds cached.")


if __name__ == "__main__":
    main()
