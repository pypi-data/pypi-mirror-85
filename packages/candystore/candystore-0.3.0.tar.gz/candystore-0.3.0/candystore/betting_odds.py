"""Betting odds data factory for use in CandyStore class."""

from datetime import datetime

from mypy_extensions import TypedDict
import numpy as np
import pandas as pd

BettingData = TypedDict(
    "BettingData",
    {
        "date": datetime,
        "season": int,
        "round": int,
        "home_team": str,
        "away_team": str,
        "home_score": int,
        "away_score": int,
        "home_margin": int,
        "away_margin": int,
        "home_win_odds": float,
        "away_win_odds": float,
        "home_win_paid": float,
        "away_win_paid": float,
        "home_line_odds": float,
        "away_line_odds": float,
        "home_line_paid": float,
        "away_line_paid": float,
        "venue": str,
    },
)

# Reasonable ranges are two standard deviations plus/minus from the means
# for all recorded AFL matches
REASONABLE_SCORE_RANGE = (23, 148)
REASONABLE_MARGIN_RANGE = (0, 89)
# Roughly the payout when win odds are even
BASELINE_BET_PAYOUT = 1.92
# Hand-wavy math to get vaguely realistic win odds
WIN_ODDS_MULTIPLIER = 0.8


def convert_to_betting_odds(base_match_data_frame: pd.DataFrame) -> pd.DataFrame:
    """Convert base match data to betting odds data."""
    home_score, away_score = (
        np.random.randint(*REASONABLE_SCORE_RANGE, size=len(base_match_data_frame)),
        np.random.randint(*REASONABLE_SCORE_RANGE, size=len(base_match_data_frame)),
    )
    home_line_odds = np.random.randint(
        *REASONABLE_MARGIN_RANGE, size=len(base_match_data_frame)
    )
    win_odds_diff = np.round(
        (np.random.rand(len(base_match_data_frame)) * WIN_ODDS_MULTIPLIER),
        decimals=2,
    )
    home_win_odds_diff = np.where(home_line_odds > 0, win_odds_diff, -1 * win_odds_diff)
    home_win_odds = BASELINE_BET_PAYOUT + home_win_odds_diff
    away_win_odds = BASELINE_BET_PAYOUT - home_win_odds_diff

    return base_match_data_frame.assign(
        home_score=home_score,
        away_score=away_score,
        home_margin=home_score - away_score,
        away_margin=away_score - home_score,
        home_win_odds=home_win_odds,
        away_win_odds=away_win_odds,
        home_win_paid=home_win_odds * (home_score > away_score).astype(int),
        away_win_paid=away_win_odds * (away_score > home_score).astype(int),
        home_line_odds=home_line_odds,
        away_line_odds=home_line_odds * -1,
        home_line_paid=BASELINE_BET_PAYOUT * (home_score > away_score).astype(int),
        away_line_paid=BASELINE_BET_PAYOUT * (away_score > home_score).astype(int),
    ).astype({"date": str})
