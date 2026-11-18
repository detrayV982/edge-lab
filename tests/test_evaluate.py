"""Tests for scoring, calibration and the time split."""
import pandas as pd
import pytest

from edgelab.evaluate import add_market_probability, brier_score, calibration_table, log_loss_score
from edgelab.model import labeled_games, time_split


def test_brier_of_perfect_and_coin_flip():
    outcomes = pd.Series([1, 0, 1, 0])
    assert brier_score(pd.Series([1.0, 0.0, 1.0, 0.0]), outcomes) == 0.0
    assert brier_score(pd.Series([0.5] * 4), outcomes) == pytest.approx(0.25)


def test_log_loss_of_coin_flip_is_ln_two():
    assert log_loss_score(pd.Series([0.5] * 4), pd.Series([1, 0, 1, 0])) == pytest.approx(0.693147, abs=1e-5)


def test_log_loss_punishes_confident_wrong_call():
    outcomes = pd.Series([1])
    assert log_loss_score(pd.Series([0.01]), outcomes) > log_loss_score(pd.Series([0.4]), outcomes)


def test_calibration_table_bins_predictions():
    table = calibration_table(pd.Series([0.1, 0.12, 0.9, 0.95]), pd.Series([0, 0, 1, 1]), bins=2)
    assert list(table["games"]) == [2, 2] and list(table["actual"]) == [0.0, 1.0]


def test_market_probability_from_even_moneylines_is_half_and_missing_is_nan():
    table = pd.DataFrame({"home_moneyline": [-110, None], "away_moneyline": [-110, -110]})
    result = add_market_probability(table)["market_prob"]
    assert result[0] == pytest.approx(0.5) and pd.isna(result[1])


def test_time_split_never_mixes_seasons_and_drops_ties():
    rows = [{"season": year, "home_score": 20, "away_score": 10 if year != 2015 else 20,
             "elo_diff": 1.0, "offense_diff": 0.0, "defense_diff": 0.0, "rest_diff": 0.0}
            for year in [2010, 2015, 2022, 2023, 2024]]
    labeled = labeled_games(pd.DataFrame(rows))
    assert 2015 not in set(labeled["season"])
    train, test = time_split(labeled)
    assert train["season"].max() == 2022 and test["season"].min() == 2023
