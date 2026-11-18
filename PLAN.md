# Edge Lab Plan

Active week: 7

Edge Lab is an NFL betting analysis tool. It never places real bets or touches real money. Paper bets use fake money only.
Goal: compare my own win-probability model to the market. Finding that the model does not beat the market is a valid result and gets reported honestly.

## Week 6 (due Sun Nov 15): scaffold and first slice
- [DONE] Repo layout, venv, .gitignore, .env.example
- [DONE] CLAUDE.md, PLAN.md (all five weeks), LOG.md
- [DONE] Odds pull script with on-disk cache (scripts/pull_odds.py) -- code and cache logic tested; live pull BLOCKED until the API key is in .env
- [DONE] American odds to implied probability, and margin removal (src/edgelab/odds_math.py)
- [DONE] Baseline model: home field plus Elo (src/edgelab/elo.py)
- [DONE] Model vs market table (scripts/compare_upcoming.py), tested on a made-up sample event; needs the live pull to show real numbers
- [DONE] Unit tests and README

## Week 7: data and model
- [DONE] Real stats pipeline from nflverse
- [DONE] Better model than plain Elo
- [DONE] Time-based train/test split
- [DONE] Calibration curve
- [DONE] Paper-bet ledger (fake money)
- [DONE] Added (instructor request): first real model-vs-market comparison on held-out seasons, using moneylines in nflverse_games.csv as the market; Brier, log loss, calibration side by side; optional cached live pull if a key exists

## Week 8: backtest (light scope, Thanksgiving week)
- [ ] Backtester with a data-leakage guard
- [ ] Compare results to the closing line

## Week 9: UI and show and tell
- [ ] Simple web UI
- [ ] Plain-language explanation for each pick
- [ ] Deploy (first week this is allowed)
- [ ] Prep show and tell for Mon Dec 7

## Week 10 (final due Sun Dec 13): polish
- [ ] Polish
- [ ] Honest final analysis
- [ ] Final README
