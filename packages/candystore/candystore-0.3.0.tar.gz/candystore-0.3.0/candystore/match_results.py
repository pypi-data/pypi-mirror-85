"""Match results data factory for use in CandyStore class."""

from typing import Dict

import pandas as pd
import numpy as np
from mypy_extensions import TypedDict


MatchResultsData = TypedDict(
    "MatchResultsData",
    {
        "date": str,
        "game": int,
        "season": int,
        "round": str,
        "round_number": int,
        "round_type": str,
        "home_team": str,
        "home_goals": int,
        "home_behinds": int,
        "home_points": int,
        "away_team": str,
        "away_goals": int,
        "away_behinds": int,
        "away_points": int,
        "margin": int,
        "venue": str,
    },
)

FINALS_ROUND_LABELS = ["QF", "EF", "SF", "PF", "GF"]
# Reasonable ranges are two standard deviations plus/minus from the means
# for all recorded AFL matches
REASONABLE_GOAL_RANGE = (2, 23)
REASONABLE_BEHIND_RANGE = (3, 22)


def _season_round_type_map(max_round: int) -> Dict[int, str]:
    finals_round_numbers = list(
        range(max_round - len(FINALS_ROUND_LABELS) + 2, max_round + 1)
    )

    return {round_number: "Finals" for round_number in finals_round_numbers}


def _map_round_type_per_season(season_group: pd.DataFrame) -> pd.Series:
    max_round = season_group["round"].max()
    finals_round_map = _season_round_type_map(max_round)

    return season_group["round"].map(
        lambda round: finals_round_map.get(round) or "Regular"
    )


def _map_round_type(match_data_frame: pd.DataFrame) -> pd.Series:
    return pd.concat(
        [
            _map_round_type_per_season(season_group)
            for _season, season_group in match_data_frame.groupby("season")
        ]
    )


def convert_to_match_results(base_match_data_frame: pd.DataFrame) -> pd.DataFrame:
    """Convert base match data to match results data."""
    match_count = len(base_match_data_frame)

    home_goals, away_goals = (
        np.random.randint(*REASONABLE_GOAL_RANGE, size=match_count),
        np.random.randint(*REASONABLE_GOAL_RANGE, size=match_count),
    )
    home_behinds, away_behinds = (
        np.random.randint(*REASONABLE_BEHIND_RANGE, size=match_count),
        np.random.randint(*REASONABLE_BEHIND_RANGE, size=match_count),
    )
    home_points, away_points = (home_goals * 6) + home_behinds, (
        away_goals * 6
    ) + away_behinds

    return base_match_data_frame.assign(
        date=lambda df: df["date"].dt.date.astype(str),
        game=lambda df: df.groupby("season").cumcount(),
        round_type=_map_round_type,
        round_number=lambda df: df["round"],
        round=lambda df: "R" + df["round"].astype(str),
        home_goals=home_goals,
        home_behinds=home_behinds,
        home_points=home_points,
        away_goals=away_goals,
        away_behinds=away_behinds,
        away_points=away_points,
        # fitzRoy gets the margin by always subtracting away points from home points
        margin=home_points - away_points,
    )
