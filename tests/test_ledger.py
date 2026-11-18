"""Tests for the fake-money paper-bet ledger. Every test writes to a temporary folder."""
import pytest

from edgelab.ledger import (STARTING_BANKROLL, current_bankroll, load_ledger, place_paper_bet,
                            settle_paper_bet, winning_profit)


def test_winning_profit_negative_and_positive_odds():
    assert winning_profit(-200, 10) == pytest.approx(5.0)
    assert winning_profit(150, 10) == pytest.approx(15.0)


def test_empty_ledger_has_starting_bankroll(tmp_path):
    assert current_bankroll(load_ledger(tmp_path / "ledger.csv")) == STARTING_BANKROLL


def test_win_and_loss_change_bankroll(tmp_path):
    path = tmp_path / "ledger.csv"
    place_paper_bet("g1", "home", -200, 10, path)
    place_paper_bet("g2", "away", 150, 10, path)
    settle_paper_bet(1, True, path)
    settle_paper_bet(2, False, path)
    assert current_bankroll(load_ledger(path)) == pytest.approx(STARTING_BANKROLL + 5.0 - 10.0)


def test_open_bet_does_not_change_bankroll(tmp_path):
    path = tmp_path / "ledger.csv"
    place_paper_bet("g1", "home", -110, 10, path)
    assert current_bankroll(load_ledger(path)) == STARTING_BANKROLL


def test_rejects_zero_odds_duplicate_and_oversized_bets(tmp_path):
    path = tmp_path / "ledger.csv"
    with pytest.raises(ValueError):
        place_paper_bet("g1", "home", 0, 10, path)
    place_paper_bet("g1", "home", -110, 10, path)
    with pytest.raises(ValueError):
        place_paper_bet("g1", "home", -110, 10, path)
    with pytest.raises(ValueError):
        place_paper_bet("g2", "home", -110, STARTING_BANKROLL, path)


def test_cannot_settle_twice(tmp_path):
    path = tmp_path / "ledger.csv"
    place_paper_bet("g1", "home", -110, 10, path)
    settle_paper_bet(1, True, path)
    with pytest.raises(ValueError):
        settle_paper_bet(1, True, path)
