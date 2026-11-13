import pytest

from edgelab.odds_math import american_to_implied, fair_probabilities, overround, remove_margin


def test_negative_odds_implied():
    assert american_to_implied(-150) == pytest.approx(0.6)


def test_positive_odds_implied():
    assert american_to_implied(150) == pytest.approx(0.4)


def test_even_money_is_half():
    assert american_to_implied(100) == pytest.approx(0.5)
    assert american_to_implied(-100) == pytest.approx(0.5)


def test_zero_odds_rejected():
    with pytest.raises(ValueError):
        american_to_implied(0)


def test_overround_of_standard_minus_110_market():
    implied = [american_to_implied(-110), american_to_implied(-110)]
    assert overround(implied) == pytest.approx(0.0476, abs=1e-3)


def test_remove_margin_sums_to_one():
    assert sum(remove_margin([0.55, 0.52])) == pytest.approx(1.0)


def test_remove_margin_keeps_ratio():
    first, second = remove_margin([0.6, 0.3])
    assert first / second == pytest.approx(2.0)


def test_fair_probabilities_symmetric_market():
    home, away = fair_probabilities(-110, -110)
    assert home == pytest.approx(0.5)
    assert away == pytest.approx(0.5)


def test_fair_probabilities_favorite():
    home, away = fair_probabilities(-200, 170)
    assert home > away
    assert home + away == pytest.approx(1.0)
