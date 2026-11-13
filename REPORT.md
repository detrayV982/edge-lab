# Report

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
