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

## Status (week 7)
Added: nflverse team stats pipeline, leak-free pre-game features, logistic regression model, time split (train through 2022, test 2023 on), Brier and log loss scoring, calibration chart, fake-money paper ledger (data/ledger.csv).
Result: on 990 held-out games the model beats plain Elo but not the no-vig market. See REPORT.md.

    .venv/bin/python scripts/evaluate_week7.py   # held-out comparison, writes reports/
    .venv/bin/python scripts/compare_live.py     # upcoming games: Elo vs model vs market
