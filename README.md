# Edge Lab

NFL betting analysis for a class project. It uses paper money only and never places real bets.
It turns sportsbook odds into implied probabilities, builds its own win-probability model, and compares the two.
The market is hard to beat, so finding the model does not beat it is a valid result.

## Setup
    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    cp .env.example .env   # then paste your free The Odds API key into .env

## Run
    .venv/bin/python scripts/pull_odds.py          # one live call per day at most, then cached
    .venv/bin/python scripts/compare_upcoming.py   # model vs market table
    .venv/bin/pytest                               # unit tests

## Status (week 6)
Odds math, Elo baseline, caching, and comparison table are built and unit tested. The live odds pull has not been run yet because no API key has been added.
