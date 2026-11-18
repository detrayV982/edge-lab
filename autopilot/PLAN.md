# Edge Lab week 7 autopilot plan
Re-read this file after every compaction. It is the source of truth.

## Where things stand
- Python 3.11.15 in .venv; pandas 3.1.1, numpy 2.4.6, scikit-learn 1.9.1, matplotlib 3.11.2, pytest 9.2.0.
- Base commit on main: c22f324. Work branch: week-7. Restore: autopilot/restore.sh (--dry-run tested).
- data/raw/nflverse_games.csv has 7548 rows, seasons 1999 to 2026; moneylines exist from about 2009.
- Weekly team stats are available at github.com/nflverse/nflverse-data/releases/download/stats_team/stats_team_week_<season>.csv (HTTP 200 for 2023).
- .env exists and has an ODDS_API_KEY line (checked by count only, never printed).
- Week 6 had 20 passing unit tests.
Everything marked DONE below is finished. Don't redo it unless a test shows it broke. Running a test again is fine.

## Done means
Every step DONE, all tests pass, REPORT.md has pass or fail per week 7 test plus a short honest "Card 5 progress" paragraph, work pushed to GitHub and week-7 fast-forward merged into main and pushed.

## My preferences
Model: logistic regression on pre-game features. Split: train through 2022, test 2023 onward. Ledger: CSV with fake bankroll. Style per CLAUDE.md: plain English comment above every function, type hints, short functions, full names, early returns.

## Approved
New branch week-7; pip install into .venv; downloads from github.com and raw/objects/release-assets githubusercontent.com into data/raw/; commit after each tested step; git push -u origin week-7; after all tests pass, ff-merge into main and git push origin main; one cached live odds pull if a key exists.

## Off limits
Reading or printing .env or keys; sportsbook accounts; real money or bets; paid APIs; scraping; deploying; force-push; deleting history; anything outside ~/edge-lab; week 8 and 9 work.

## How to work
Small batches, test each, log in change_log.md, three-strike rule, no asking. Never use training data from the future: features for a game use only earlier games.

## Steps
1. Stats pipeline: download and load nflverse weekly team stats (src/edgelab/team_stats.py). Test: loads, row counts, no network when cached.
2. Features: pre-game Elo, rolling EPA for and against, rest, with shift so no leakage (src/edgelab/features.py). Test: a game's features never change when later games change.
3. Model + time split: logistic regression, train through 2022, test 2023+ (src/edgelab/model.py). Test: no test-season row in training.
4. Evaluation + calibration: Brier, log loss, calibration bins and PNG (src/edgelab/evaluate.py).
5. Market comparison: no-vig moneyline probabilities vs model vs Elo on held-out seasons (scripts/evaluate_week7.py); check what moneyline columns mean.
6. Paper-bet ledger: CSV, fake bankroll, flat stake (src/edgelab/ledger.py).
7. Live pull: one cached call if key exists; compare upcoming games.
8. Docs, REPORT.md, push, merge.

## Test plan
pytest all pass; leakage tests; split test; metric tests on known values; ledger tests; cold start: fresh shell, run scripts/evaluate_week7.py from cache.

## Check by hand
Open reports/calibration.png and confirm both curves are drawn.

## Goal message
See the /goal message the user pasted in the session on 2026-11-18 (week 7 goal). Summary: do only week 7, stop after 4 hours.
