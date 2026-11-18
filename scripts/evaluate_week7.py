"""Trains on seasons through 2022 and compares model, Elo and the no-vig market on 2023 onward."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import numpy as np
import pandas as pd

from edgelab.elo import HOME_FIELD_POINTS
from edgelab.evaluate import (add_market_probability, brier_score, calibration_table,
                              log_loss_score, plot_calibration)
from edgelab.features import build_features
from edgelab.games import completed_games, load_games
from edgelab.model import fit_model, labeled_games, predict_home_probability, time_split
from edgelab.team_stats import load_team_stats

REPORT_FOLDER = Path("reports")


# Elo-only win probability from the pre-game rating gap plus the home-field bonus.
def elo_probability(table: pd.DataFrame) -> pd.Series:
    return 1.0 / (1.0 + 10 ** (-(table["elo_diff"] + HOME_FIELD_POINTS) / 400.0))


# Builds the labeled feature table for every finished game.
def load_labeled() -> pd.DataFrame:
    games = load_games()
    finished = completed_games(games)
    stats = load_team_stats(2006, int(finished["season"].max()))
    return labeled_games(build_features(finished, stats, finished))


# Scores each named set of probabilities on the same games.
def score_all(probabilities: dict[str, pd.Series], outcomes: pd.Series) -> pd.DataFrame:
    rows = [{"source": name, "games": len(outcomes), "brier": brier_score(values, outcomes),
             "log_loss": log_loss_score(values, outcomes)} for name, values in probabilities.items()]
    return pd.DataFrame(rows)


# Paired bootstrap of (model Brier minus market Brier); negative means the model is better.
def brier_gap_interval(model: pd.Series, market: pd.Series, outcomes: pd.Series) -> tuple[float, float]:
    generator = np.random.default_rng(7)
    squared_gap = ((model - outcomes) ** 2 - (market - outcomes) ** 2).to_numpy()
    means = [generator.choice(squared_gap, len(squared_gap)).mean() for _ in range(2000)]
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


# Runs the whole held-out comparison and saves the metrics table and calibration chart.
def main() -> None:
    train, test = time_split(load_labeled())
    model = fit_model(train)
    test = add_market_probability(test).dropna(subset=["market_prob"])
    probabilities = {"model": predict_home_probability(model, test), "elo": elo_probability(test),
                     "market": test["market_prob"]}
    outcomes = test["home_win"]
    metrics = score_all(probabilities, outcomes)
    REPORT_FOLDER.mkdir(exist_ok=True)
    metrics.to_csv(REPORT_FOLDER / "week7_metrics.csv", index=False)
    plot_calibration({name: calibration_table(values, outcomes) for name, values in probabilities.items()},
                     REPORT_FOLDER / "calibration.png")
    low, high = brier_gap_interval(probabilities["model"], probabilities["market"], outcomes)
    print(f"train games {len(train)} (seasons {train.season.min()}-{train.season.max()}), "
          f"test games {len(test)} (seasons {test.season.min()}-{test.season.max()})")
    print(metrics.round(4).to_string(index=False))
    print(f"Brier gap model minus market: 95% interval {low:.4f} to {high:.4f} (negative = model better)")
    print(dict(zip(["intercept"] + list(model.feature_names_in_), [round(float(model[-1].intercept_[0]), 3)] + [round(float(c), 3) for c in model[-1].coef_[0]])))


if __name__ == "__main__":
    main()
