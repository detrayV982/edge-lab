"""Paper-bet ledger. Fake money only: this file records pretend bets in a CSV and never touches a sportsbook."""
from datetime import datetime
from pathlib import Path

import pandas as pd

LEDGER_FILE = Path("data/ledger.csv")
STARTING_BANKROLL = 1000.0  # fake dollars
FLAT_STAKE = 10.0
COLUMNS = ["bet_id", "placed_at", "game_id", "side", "american_odds", "stake", "status", "profit", "bankroll_after"]


# Reads the ledger from disk, or returns an empty one if nothing has been recorded yet.
def load_ledger(path: Path = LEDGER_FILE) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=COLUMNS)
    return pd.read_csv(path)


# Writes the ledger back to disk.
def save_ledger(ledger: pd.DataFrame, path: Path = LEDGER_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ledger.to_csv(path, index=False)


# Profit on a winning bet at American odds, not counting the returned stake.
def winning_profit(american_odds: float, stake: float) -> float:
    if american_odds == 0:
        raise ValueError("American odds cannot be 0")
    if american_odds < 0:
        return stake * 100 / -american_odds
    return stake * american_odds / 100


# Fake bankroll after all settled bets (open bets are not counted yet).
def current_bankroll(ledger: pd.DataFrame) -> float:
    settled = ledger[ledger["status"] != "open"]
    return STARTING_BANKROLL + float(settled["profit"].sum())


# Fake money still tied up in bets that have not been settled.
def open_exposure(ledger: pd.DataFrame) -> float:
    return float(ledger.loc[ledger["status"] == "open", "stake"].sum())


# Records a new open paper bet; refuses bad odds, bad stakes, duplicates and bets bigger than free bankroll.
def place_paper_bet(game_id: str, side: str, american_odds: float, stake: float = FLAT_STAKE,
                    path: Path = LEDGER_FILE) -> pd.DataFrame:
    ledger = load_ledger(path)
    if american_odds == 0 or stake <= 0:
        raise ValueError("Odds cannot be 0 and stake must be positive")
    if stake > current_bankroll(ledger) - open_exposure(ledger):
        raise ValueError("Not enough fake bankroll for this stake")
    already_open = ((ledger["game_id"] == game_id) & (ledger["side"] == side) & (ledger["status"] == "open")).any()
    if already_open:
        raise ValueError("There is already an open bet on this game and side")
    row = {"bet_id": len(ledger) + 1, "placed_at": datetime.now().isoformat(timespec="seconds"),
           "game_id": game_id, "side": side, "american_odds": american_odds, "stake": stake,
           "status": "open", "profit": 0.0, "bankroll_after": None}
    ledger = pd.concat([ledger, pd.DataFrame([row])], ignore_index=True)
    save_ledger(ledger, path)
    return ledger


# Settles one open bet as won or lost and records the fake bankroll afterward.
def settle_paper_bet(bet_id: int, won: bool, path: Path = LEDGER_FILE) -> pd.DataFrame:
    ledger = load_ledger(path)
    position = ledger.index[(ledger["bet_id"] == bet_id) & (ledger["status"] == "open")]
    if len(position) == 0:
        raise ValueError("No open bet with that id")
    index = position[0]
    stake, odds = ledger.loc[index, "stake"], ledger.loc[index, "american_odds"]
    ledger.loc[index, "status"] = "won" if won else "lost"
    ledger.loc[index, "profit"] = winning_profit(odds, stake) if won else -stake
    ledger.loc[index, "bankroll_after"] = current_bankroll(ledger)
    save_ledger(ledger, path)
    return ledger
