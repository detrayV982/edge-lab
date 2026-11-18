# Log

## 2026-11-13 (Fri), Week 6
- Built the scaffold, odds math, Elo baseline, cached odds script, comparison table, tests, README.
- Interview answers that changed the plan:
  - No Odds API key yet, so the live odds pull is blocked this week. Everything is tested against a made-up sample response, and the cache logic is tested with no network.
  - No GitHub origin yet, so the week-6 branch is committed locally and not pushed.
- Interview answers that did not change the plan: NFL confirmed; default python3 (3.11); live odds calls capped at 1 per day, all responses cached to data/raw/.
- nflverse games.csv downloaded once (read-only) and used to build Elo ratings; top team by rating sanity-checked (BUF).
- GitHub repo was created on Nov 13. Week 6 was pushed and merged to main on Nov 15.

## 2026-11-18 (Wed), Week 7
- Instructor feedback: do a first real model-versus-market comparison now, not later. Run it on held-out seasons with the moneylines in nflverse_games.csv as the market, report Brier score, log loss and calibration for both, and say plainly if the model does not beat the market.
- Added that as a week 7 step in PLAN.md. Also confirm in REPORT.md whether those moneylines are closing lines.
- Choices made without asking: logistic regression on pre-game features; train through 2022, test 2023 onward; CSV ledger with a fake bankroll.
