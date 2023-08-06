"""Fixture data factory for use in CandyStore class."""

import pandas as pd
from mypy_extensions import TypedDict

FixtureData = TypedDict(
    "FixtureData",
    {
        "date": str,
        "season": int,
        "season_game": int,
        "round": int,
        "home_team": str,
        "away_team": str,
        "venue": str,
    },
)


def convert_to_fixtures(base_match_data_frame: pd.DataFrame) -> pd.DataFrame:
    """Convert base match data to fixture data."""
    return base_match_data_frame.assign(
        season_game=lambda df: df.groupby("season").cumcount()
    ).astype({"date": str})
