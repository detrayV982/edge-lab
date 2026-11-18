"""Scoring for win probabilities: Brier score, log loss, calibration table and chart."""
from pathlib import Path

import numpy as np
import pandas as pd

from edgelab.odds_math import fair_probabilities

CLIP = 1e-6


# Average squared gap between the predicted probability and what happened (lower is better).
def brier_score(probabilities: pd.Series, outcomes: pd.Series) -> float:
    return float(np.mean((probabilities - outcomes) ** 2))


# Average penalty for confident wrong calls (lower is better).
def log_loss_score(probabilities: pd.Series, outcomes: pd.Series) -> float:
    clipped = probabilities.clip(CLIP, 1 - CLIP)
    return float(-np.mean(outcomes * np.log(clipped) + (1 - outcomes) * np.log(1 - clipped)))


# Groups predictions into equal-width bins and compares the average prediction to the real win rate.
def calibration_table(probabilities: pd.Series, outcomes: pd.Series, bins: int = 10) -> pd.DataFrame:
    edges = np.linspace(0, 1, bins + 1)
    labels = pd.cut(probabilities, edges, include_lowest=True)
    grouped = pd.DataFrame({"predicted": probabilities, "actual": outcomes}).groupby(labels, observed=True)
    table = grouped.agg(games=("actual", "size"), predicted=("predicted", "mean"), actual=("actual", "mean"))
    return table.reset_index(drop=True)


# Margin-free home win probability from the two moneylines; None if either is missing.
def market_home_probability(home_moneyline: float, away_moneyline: float) -> float | None:
    if pd.isna(home_moneyline) or pd.isna(away_moneyline):
        return None
    return fair_probabilities(home_moneyline, away_moneyline)[0]


# Adds the no-vig market probability column to a games table.
def add_market_probability(table: pd.DataFrame) -> pd.DataFrame:
    result = table.copy()
    result["market_prob"] = [
        market_home_probability(home, away) for home, away in zip(result["home_moneyline"], result["away_moneyline"])
    ]
    result["market_prob"] = result["market_prob"].astype(float)
    return result


# Draws every model's calibration curve against the perfect diagonal and saves it as a PNG.
def plot_calibration(curves: dict[str, pd.DataFrame], path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    figure, axis = plt.subplots(figsize=(6, 6))
    axis.plot([0, 1], [0, 1], "k--", label="perfect")
    for name, table in curves.items():
        axis.plot(table["predicted"], table["actual"], marker="o", label=name)
    axis.set_xlabel("Predicted home win probability")
    axis.set_ylabel("Actual home win rate")
    axis.set_title("Calibration on held-out seasons")
    axis.legend()
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=110, bbox_inches="tight")
    plt.close(figure)
