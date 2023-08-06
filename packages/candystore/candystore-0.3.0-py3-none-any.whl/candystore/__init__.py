"""Factories for randomised AFL data sets for testing purposes."""

from typing import Union, Optional, List, Tuple

import pandas as pd

from .base_data import generate_base_data
from .fixtures import convert_to_fixtures, FixtureData
from .betting_odds import convert_to_betting_odds, BettingData
from .match_results import convert_to_match_results, MatchResultsData
from .players import convert_to_players, PlayerData

SeasonRange = Tuple[int, int]


class CandyStore:
    """Data factory for different data sets related to AFL matches."""

    def __init__(self, seasons: Union[int, SeasonRange] = 1):
        """
        Parameters
        ----------
        seasons
            The seasons to generate data for. If an integer, will start from a random\
            year for which AFL data exists and increment for the given number of years.\
            If a tuple of integers, will generate fixtures for the given range of years\
            (same rules as Python's `range`).

        Attributes
        ----------
        seasons
            The seasons for which fake data is generated.
        """
        self.seasons = seasons
        self._base_data = generate_base_data(seasons)

    def fixtures(
        self, to_dict: Optional[str] = None
    ) -> Union[pd.DataFrame, List[FixtureData]]:
        """Generate fixture data for the given seasons.

        Parameters
        ----------
        to_dict
            Type of dictionary data to return (passed directly to Panda's `to_dict`\
            method). `None` returns a DataFrame.

        Returns
        -------
        pd.DataFrame or list(dict)
            DataFrame or list of fixture dictionaries that replicate \
            fitzRoy's `get_fixture` function, but with Pythonic conventions \
            (e.g. snake_case keys)

        Examples
        --------
        .. code-block:: python

            {
                "date": "1967-03-16 12:37:19",
                "season": 1967,
                "season_game": 1,
                "round": 1,
                "home_team": "Melbourne",
                "away_team": "Brisbane Lions",
                "venue": "Sydney Showground"
            }
        """
        fixtures_data_frame = self._base_data.pipe(convert_to_fixtures)

        return (
            fixtures_data_frame
            if to_dict is None
            else fixtures_data_frame.to_dict(to_dict)
        )

    def betting_odds(
        self, to_dict: Optional[str] = None
    ) -> Union[pd.DataFrame, List[BettingData]]:
        """Generate betting odds data for the given seasons.

        Parameters
        ----------
        to_dict
            Type of dictionary data to return (passed directly to Panda's `to_dict`\
            method). `None` returns a DataFrame.

        Returns
        -------
        pd.DataFrame or list(dict)
            DataFrame or list of betting odds dictionaries that replicate fitzRoy's\
            `get_footywire_betting_odds` function, but with Pythonic conventions\
            (e.g. snake_case keys)

        Examples
        --------
        .. code-block:: python

            {
                "date": "1967-03-21 18:40:59",
                "season": 1967,
                "home_team": "Sydney",
                "away_team": "Fremantle",
                "venue": "Wellington",
                "round": 1,
                "home_score": 26,
                "away_score": 89,
                "home_margin": -63,
                "away_margin": 63,
                "home_win_odds": 2.71,
                "away_win_odds": 1.13,
                "home_win_paid": 0.0,
                "away_win_paid": 1.13,
                "home_line_odds": 33,
                "away_line_odds": -33,
                "home_line_paid": 0.0,
                "away_line_paid": 1.92
            }
        """
        betting_odds_data_frame = self._base_data.pipe(convert_to_betting_odds)

        return (
            betting_odds_data_frame
            if to_dict is None
            else betting_odds_data_frame.to_dict(to_dict)
        )

    def match_results(
        self, to_dict: Optional[str] = None
    ) -> Union[pd.DataFrame, List[MatchResultsData]]:
        """Generate match results data data for the given seasons.

        Parameters
        ----------
        to_dict
            Type of dictionary data to return (passed directly to Panda's `to_dict`\
            method). `None` returns a DataFrame.

        Returns
        -------
        pd.DataFrame or list(dict)
            DataFrame or list of match dictionaries that replicate \
            fitzRoy's `get_match_results` function, but with Pythonic conventions \
            (e.g. snake_case keys)

        Examples
        --------
        .. code-block:: python

            {
                "date": "1933-03-18",
                "season": 1933,
                "round": "R1",
                "home_team": "Gold Coast",
                "away_team": "Adelaide",
                "venue": "Princes Park",
                "game": 0,
                "round_number": 1,
                "round_type": "Regular",
                "home_goals": 2,
                "home_behinds": 11,
                "home_points": 23,
                "away_goals": 21,
                "away_behinds": 17,
                "away_points": 143,
                "margin": -120
            }
        """
        match_data_frame = self._base_data.pipe(convert_to_match_results)

        return (
            match_data_frame if to_dict is None else match_data_frame.to_dict(to_dict)
        )

    def players(
        self, to_dict: Optional[str] = None
    ) -> Union[pd.DataFrame, List[PlayerData]]:
        """Generate player data data for the given seasons.

        Parameters
        ----------
        to_dict
            Type of dictionary data to return (passed directly to Panda's `to_dict`\
            method). `None` returns a DataFrame.

        Returns
        -------
        pd.DataFrame or list(dict)
            DataFrame or list of player dictionaries that replicate \
            fitzRoy's `get_afltables_stats` function, but with Pythonic conventions \
            (e.g. snake_case keys)

        Examples
        --------
        .. code-block:: python

            {
                "date": "1933-03-18",
                "season": 1933,
                "round": 1,
                "home_team": "Gold Coast",
                "away_team": "Adelaide",
                "venue": "Princes Park",
                "local_start_time": 1437,
                "attendance": 42853,
                "hq1g": 3,
                "hq1b": 3,
                "hq2g": 2,
                "hq2b": 1,
                "hq3g": 1,
                "hq3b": 5,
                "hq4g": 3,
                "hq4b": 4,
                "home_score": 67,
                "aq1g": 1,
                "aq1b": 2,
                "aq2g": 5,
                "aq2b": 1,
                "aq3g": 0,
                "aq3b": 1,
                "aq4g": 2,
                "aq4b": 1,
                "away_score": 67,
                "umpire_1": "William Mayo",
                "umpire_2": "Justin Washington",
                "umpire_3": "Brian Nicholson",
                "umpire_4": "Barbara Lamb",
                "group_id": 353,
                "first_name": "Elizabeth",
                "surname": "Lewis",
                "id": 0,
                "jumper_no": 18,
                "playing_for": "Gold Coast",
                "kicks": 6,
                "marks": 8,
                "handballs": 10,
                "goals": 1,
                "behinds": 0,
                "hit_outs": 10,
                "tackles": 3,
                "rebounds": 4,
                "inside_50s": 4,
                "clearances": 2,
                "clangers": 0,
                "frees_for": 3,
                "frees_against": 4,
                "brownlow_votes": 1,
                "contested_possessions": 2,
                "uncontested_possessions": 6,
                "contested_marks": 2,
                "marks_inside_50": 1,
                "one_percenters": 3,
                "bounces": 2,
                "goal_assists": 0,
                "time_on_ground": 14,
                "substitute": 1
            }
        """
        player_data_frame = self._base_data.pipe(convert_to_players)

        return (
            player_data_frame if to_dict is None else player_data_frame.to_dict(to_dict)
        )
