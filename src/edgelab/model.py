"""Logistic regression win-probability model with a strict time-based train/test split."""
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from edgelab.features import FEATURE_COLUMNS

FIRST_TRAIN_SEASON = 2007  # earlier seasons only warm up the Elo ratings and rolling form
LAST_TRAIN_SEASON = 2022
FIRST_TEST_SEASON = 2023


# Keeps finished, non-tied games with full features and adds the 1/0 home_win target.
def labeled_games(features: pd.DataFrame) -> pd.DataFrame:
    table = features.dropna(subset=["home_score", "away_score"] + FEATURE_COLUMNS)
    table = table[table["home_score"] != table["away_score"]].copy()
    table["home_win"] = (table["home_score"] > table["away_score"]).astype(int)
    return table


# Splits by season: train on the past, test on later seasons, and refuses any overlap.
def time_split(labeled: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    train = labeled[(labeled["season"] >= FIRST_TRAIN_SEASON) & (labeled["season"] <= LAST_TRAIN_SEASON)]
    test = labeled[labeled["season"] >= FIRST_TEST_SEASON]
    if train["season"].max() >= test["season"].min():
        raise ValueError("Training data overlaps the test seasons")
    return train, test


# Fits a scaled logistic regression on the training games only.
def fit_model(train: pd.DataFrame):
    model = make_pipeline(StandardScaler(), LogisticRegression(C=1.0))
    return model.fit(train[FEATURE_COLUMNS], train["home_win"])


# Probability that the home team wins, for every row of the table.
def predict_home_probability(model, table: pd.DataFrame) -> pd.Series:
    probabilities = model.predict_proba(table[FEATURE_COLUMNS])[:, 1]
    return pd.Series(probabilities, index=table.index)
