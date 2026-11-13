# Edge Lab

NFL betting analysis tool. Paper bets only. It never places real bets or touches real money.
Course: TCSS 490 Artifact 5 (moonshot). Weekly work, one week at a time. See PLAN.md (active week is at the top) and LOG.md.

## Plan
Week 6 scaffold, week 7 stats + model + calibration + ledger, week 8 backtest, week 9 UI + deploy, week 10 polish. Details in PLAN.md.

## Layout
- src/edgelab/: odds_math.py, odds_fetch.py, teams.py, games.py, elo.py, compare.py
- scripts/: pull_odds.py, compare_upcoming.py
- tests/: pytest unit tests (run `.venv/bin/pytest`)
- data/raw/: cached API responses and downloads
- autopilot/: plan and change log for the course. DO NOT gitignore it.
- PLAN.md, LOG.md, REPORT.md, README.md at the root

## Off limits
- Sportsbook accounts or logins; placing or simulating bets through any real account
- Scraping sites whose terms forbid it; paid API tiers; spending money
- Deploying before week 9
- Printing or committing the API key (.env stays gitignored)
- Only official APIs and free downloads: The Odds API (free tier, cache everything, 1 live call per day) and nflverse

## Conventions
Plain English comment above every function, type hints, short single-purpose functions, full variable names, early returns.
Git: commit on branch week-<number>, push to origin; the user merges to main.
