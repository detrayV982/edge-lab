# Change log (week 7)
- 2026-11-18 09:36:58 branch week-7 created; pip install matplotlib; requirements.txt updated; PLAN.md active week 7; LOG.md updated. Result: ok.
- 2026-11-18 09:38:21 steps 1-2: team_stats.py, features.py, elo_history, normalize_team_codes, tests/test_features.py. Cause found: old codes OAK/SD/STL caused 9.4% NaN features; fixed by normalizing. 26 pass.
- 2026-11-18 09:40:07 steps 3-6 built: model.py, evaluate.py, ledger.py, scripts/evaluate_week7.py; 38 tests pass. Held-out 2023-2026 (990 games): model brier .2219 ll .6336, elo .2267/.6448, market .2109/.6098. Model does not beat market.
- 2026-11-18 09:40:14 Mistake: stats CSVs in data/raw were committed locally (unpushed). Fixed by soft reset of that one unpushed commit, ignoring data/raw/*.csv, recommitting. Never pushed.
- 2026-11-18 09:41:14 steps 7-8: compare_live.py, upcoming.py, tests (41 pass), docs, REPORT.md. Live pull ok (29 games, 499 left).
