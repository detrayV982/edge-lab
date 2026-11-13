"""Odds conversion: American odds to implied probability, and bookmaker margin removal."""


# Turns American odds (like -150 or +130) into the probability the price implies, margin included.
def american_to_implied(american_odds: float) -> float:
    if american_odds == 0:
        raise ValueError("American odds cannot be 0")
    if american_odds < 0:
        return -american_odds / (-american_odds + 100)
    return 100 / (american_odds + 100)


# Sum of implied probabilities minus 1; this is the bookmaker's built-in margin (the "vig").
def overround(implied_probabilities: list[float]) -> float:
    return sum(implied_probabilities) - 1.0


# Rescales implied probabilities so they sum to 1, which removes the margin proportionally.
def remove_margin(implied_probabilities: list[float]) -> list[float]:
    total = sum(implied_probabilities)
    if total <= 0:
        raise ValueError("Implied probabilities must sum to a positive number")
    return [probability / total for probability in implied_probabilities]


# Convenience for a two-way market: returns the fair (margin-free) home and away probabilities.
def fair_probabilities(home_american: float, away_american: float) -> tuple[float, float]:
    home_implied = american_to_implied(home_american)
    away_implied = american_to_implied(away_american)
    home_fair, away_fair = remove_margin([home_implied, away_implied])
    return home_fair, away_fair
