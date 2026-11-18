# Report

## Read this first (week 7)
- The model does NOT beat the market. On 990 held-out games (2023 to 2026) the market has the best Brier score and log loss. The gap in Brier (model minus market) is +0.011 with a 95% bootstrap interval of +0.006 to +0.016, so the model is reliably worse, not just unlucky.
- The model does beat plain Elo (Brier 0.2219 vs 0.2267, log loss 0.6336 vs 0.6448).
- The moneylines in nflverse_games.csv are NOT documented as closing lines. The nflverse data dictionary only says "Odds for home team to win the game" with no timestamp. Treat them as "a late-week line, probably close to closing, but unverified". If they are earlier than close, the real closing line would be even harder to beat.
- 2026 is a partial season (136 test games so far), and it is included.
- One mistake, fixed: downloaded stats CSVs were briefly in a local, unpushed commit. I rewrote those two local commits so nothing from data/raw was ever pushed. data/raw/*.csv is now gitignored.
- Rest days are assumed equal in the live comparison because the odds feed has no rest data (tiny effect, coefficient 0.07 per standard deviation).

## Week 7 test results

| Test | Result |
|---|---|
| Full pytest suite (41 tests: 20 from week 6, 21 new) | pass, 41 of 41 |
| Leakage: earlier games' features unchanged when a later game changes | pass |
| Leakage: a game's own stats never enter its own features | pass |
| Time split: train 2007 to 2022, test 2023 onward, ties dropped, overlap raises | pass |
| Brier and log loss on known values (perfect, coin flip, confident wrong) | pass |
| Calibration bins on a known example | pass |
| No-vig market probability (even money is 0.5, missing is NaN) | pass |
| Paper ledger: win, loss, duplicate, zero odds, oversize, double settle | pass |
| Stats cache makes no network call when the file exists | pass |
| Old team codes (OAK, SD, STL) renamed to LV, LAC, LA | pass |
| Upcoming-game features and recent form | pass |
| Held-out evaluation script runs end to end (scripts/evaluate_week7.py) | pass |
| Live odds pull, one cached call (29 games, 499 requests left) | pass |
| Live comparison (scripts/compare_live.py, 29 games) | pass |
| Cold start: fresh shell, full pytest and both scripts from cache | pass |

## Held-out comparison (990 games, 2023 to 2026, same games for all three)

| Source | Brier (lower is better) | Log loss (lower is better) |
|---|---|---|
| Market, no-vig moneyline | 0.2109 | 0.6098 |
| Logistic model | 0.2219 | 0.6336 |
| Elo only | 0.2267 | 0.6448 |

Model: logistic regression on Elo gap, recent offense EPA/play gap, recent defense EPA/play gap, rest gap. Trained on 4,296 games from 2007 to 2022. Features use only earlier games (8-game rolling form, Elo before kickoff).

Calibration (reports/calibration.png, plus text bins in reports/week7_run.txt): the market's curve hugs the diagonal across all 10 bins. The model is close in the middle bins but overstates home teams in the 0.3 to 0.4 range (predicts 0.35, actual 0.28 on 116 games) and is too cautious at the extremes (no predictions above 0.92 and few above 0.85). Overall it predicts home wins 56.2% of the time vs 54.1% actual.

## Live comparison
.env has a key, so one cached live pull ran on 2026-11-18 (29 games, 499 requests remaining). Table saved in reports/live_comparison.txt. Mean absolute gap between model and market is 0.086. Given the held-out result, treat these gaps as model error, not as edges.

## Check by hand
Open reports/calibration.png and confirm three curves and a dashed diagonal are drawn.

## Where everything is, and how to restore
Code in src/edgelab, scripts in scripts, tests in tests, outputs in reports/. Plan and log in autopilot/. Undo everything with autopilot/restore.sh (use --dry-run first); it returns to main at c22f324.

## Card 5 progress
Edge Lab week 7: I built a real nflverse stats pipeline, a logistic regression model, a time-based split (train through 2022, test 2023 onward, no future data), a calibration curve and a fake-money paper ledger. My instructor asked for a first real comparison, so I scored the model, plain Elo and the no-vig market on 990 held-out games. The market won on both Brier score (0.211 vs 0.222) and log loss (0.610 vs 0.634), and the gap is outside the bootstrap interval, so my model does not beat the market. It does beat Elo. The moneylines are not documented as closing lines, so that comparison is an estimate. Next week is the backtester with a leakage guard.

---

# Week 6 (earlier)

## Week 6 test results

| Test | Result |
|---|---|
| test_compare.py::test_market_probability_even_market | pass |
| test_compare.py::test_market_probability_none_without_bookmakers | pass |
| test_compare.py::test_compare_table_columns_and_gap | pass |
| test_compare.py::test_completed_and_upcoming_split | pass |
| test_compare.py::test_cache_hit_makes_no_network_call | pass |
| test_elo.py::test_equal_teams_favor_home | pass |
| test_elo.py::test_home_field_bonus_is_applied | pass |
| test_elo.py::test_update_is_zero_sum | pass |
| test_elo.py::test_winner_gains_rating | pass |
| test_elo.py::test_regress_moves_toward_mean | pass |
| test_elo.py::test_build_ratings_rewards_winner | pass |
| test_odds_math.py::test_negative_odds_implied | pass |
| test_odds_math.py::test_positive_odds_implied | pass |
| test_odds_math.py::test_even_money_is_half | pass |
| test_odds_math.py::test_zero_odds_rejected | pass |
| test_odds_math.py::test_overround_of_standard_minus_110_market | pass |
| test_odds_math.py::test_remove_margin_sums_to_one | pass |
| test_odds_math.py::test_remove_margin_keeps_ratio | pass |
| test_odds_math.py::test_fair_probabilities_symmetric_market | pass |
| test_odds_math.py::test_fair_probabilities_favorite | pass |

Live odds pull: not tested (no API key yet).

## Card 5 progress

Edge Lab: week 6 scaffold

The odds-to-probability math, the margin removal, and the Elo baseline work, and all 20 unit tests pass. The comparison table works on a made-up sample game, and the cache logic is tested to make no network call when a cached file exists. The live odds pull is untested because I have not added The Odds API key yet, so no real model-vs-market numbers exist. The Elo model has not been checked for accuracy or calibration. Next week is the real stats pipeline, a better model, a time-based split, a calibration curve, and the paper-bet ledger.
