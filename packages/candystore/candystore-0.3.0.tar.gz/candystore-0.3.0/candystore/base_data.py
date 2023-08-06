"""Generic, pseudo-random match data to serve as the base for realistic data sets."""

from typing import Tuple, Union, List
from datetime import date, datetime, timedelta
import itertools
import math
from functools import partial

from faker import Faker
from mypy_extensions import TypedDict
import numpy as np
import pandas as pd


BaseMatchData = TypedDict(
    "BaseMatchData",
    {
        "date": datetime,
        "season": int,
        "round": int,
        "home_team": str,
        "away_team": str,
        "venue": str,
    },
)
DateRange = TypedDict(
    "DateRange", {"datetime_start": datetime, "datetime_end": datetime}
)


FAKE = Faker()

FIRST_AFL_SEASON = 1897
MAR = 3
FIFTEENTH = 15
SEP = 9
THIRTIETH = 30
WEDNESDAY = 2
# About as early as matches ever start
MIN_MATCH_HOUR = 12
# About as late as matches ever start
MAX_MATCH_HOUR = 20

WEEK_IN_DAYS = 7
DAY_IN_HOURS = 24

NON_BRISBANE_TEAMS = [
    "Richmond",
    "Carlton",
    "Melbourne",
    "Greater Western Sydney",
    "Essendon",
    "Sydney",
    "Collingwood",
    "North Melbourne",
    "Western Bulldogs",
    "Fremantle",
    "Port Adelaide",
    "St Kilda",
    "Hawthorn",
    "Adelaide",
    "Gold Coast",
    "Geelong",
    "West Coast",
    "Fitzroy",
    "University",
]
BRISBANE_TEAMS = [
    "Brisbane Bears",
    "Brisbane Lions",
]

VENUES = [
    # AFL Tables venues
    "Football Park",
    "S.C.G.",
    "Windy Hill",
    "Subiaco",
    "Moorabbin Oval",
    "M.C.G.",
    "Kardinia Park",
    "Victoria Park",
    "Waverley Park",
    "Princes Park",
    "Western Oval",
    "W.A.C.A.",
    "Carrara",
    "Gabba",
    "Docklands",
    "York Park",
    "Manuka Oval",
    "Sydney Showground",
    "Adelaide Oval",
    "Bellerive Oval",
    "Marrara Oval",
    "Traeger Park",
    "Perth Stadium",
    "Stadium Australia",
    "Wellington",
    "Lake Oval",
    "East Melbourne",
    "Corio Oval",
    "Junction Oval",
    "Brunswick St",
    "Punt Rd",
    "Glenferrie Oval",
    "Arden St",
    "Olympic Park",
    "Yarraville Oval",
    "Toorak Park",
    "Euroa",
    "Coburg Oval",
    "Brisbane Exhibition",
    "North Hobart",
    "Bruce Stadium",
    "Yallourn",
    "Cazaly's Stadium",
    "Eureka Stadium",
    "Blacktown",
    "Jiangwan Stadium",
    "Albury",
    "Riverway Stadium",
    # Footywire venues
    "AAMI Stadium",
    "ANZ Stadium",
    "UTAS Stadium",
    "Blacktown International",
    "Blundstone Arena",
    "Domain Stadium",
    "Etihad Stadium",
    "GMHBA Stadium",
    "MCG",
    "Mars Stadium",
    "Metricon Stadium",
    "Optus Stadium",
    "SCG",
    "Spotless Stadium",
    "TIO Stadium",
    "Westpac Stadium",
    "Marvel Stadium",
    "Canberra Oval",
    # Correct spelling is 'Traeger', but footywire.com is spelling it 'Traegar' in its
    # fixtures
    "TIO Traegar Park",
]


def _tuple_season_range(seasons: Tuple[int, int], current_year: int) -> range:
    assert (
        len(seasons) == 2
    ), f"Must provide two seasons to have a valid range, but {seasons} was given."

    assert min(seasons) >= FIRST_AFL_SEASON and max(seasons) <= current_year + 1, (
        f"Provided seasons must be in the range of {FIRST_AFL_SEASON} to "
        f"{current_year + 1} (inclusive) to generate valid data."
    )

    assert (
        seasons[0] < seasons[1]
    ), "First season must be less than second to create a valid range."

    return range(*seasons)


def _int_season_range(seasons: int, current_year: int) -> range:
    assert seasons > 0, "Must generate fixture data for at least one season."

    # We add 2, because we are open to the possibility of including matches
    # from the current year in the data.
    max_start_season = current_year - seasons + 2
    start_season = np.random.choice(np.arange(FIRST_AFL_SEASON, max_start_season))
    end_season = start_season + seasons

    return range(start_season, end_season)


def _season_range(seasons: Union[int, Tuple[int, int]]) -> range:
    current_year = date.today().year

    if isinstance(seasons, int):
        return _int_season_range(seasons, current_year)

    if isinstance(seasons, tuple):
        return _tuple_season_range(seasons, current_year)

    raise TypeError(
        "seasons argument must be either an integer or a tuple of two integers"
    )


def _generate_teams():
    # We only want one Brisbane team per round, because depending on how team names
    # are normalised we can end up with duplicate teams, which is invalid.
    # It seems that there's more consensus on how to handle other teams that moved
    # or folded.
    valid_teams = NON_BRISBANE_TEAMS + [np.random.choice(BRISBANE_TEAMS)]
    return (team for team in np.random.permutation(valid_teams))


def _match_date_time(round_start_date: datetime) -> datetime:
    raw_match_date_time = FAKE.date_time_between_dates(
        datetime_start=round_start_date,
        datetime_end=(round_start_date + timedelta(days=WEEK_IN_DAYS)),
    )
    # We need to generate the time separately to make sure we have
    # a realistic start time for the match on the randomly-generated day.
    raw_match_time = FAKE.date_time_between_dates(
        datetime_start=raw_match_date_time.replace(
            hour=MIN_MATCH_HOUR, minute=0, second=0
        ),
        datetime_end=raw_match_date_time.replace(
            hour=MAX_MATCH_HOUR, minute=0, second=0
        ),
    ).time()

    return raw_match_date_time.replace(
        hour=raw_match_time.hour,
        minute=raw_match_time.minute,
        second=raw_match_time.second,
    )


def _generate_match(
    round_number: int,
    round_start_date: datetime,
    teams: Tuple[str, str],
    venue: str,
) -> BaseMatchData:
    match_date_time = _match_date_time(round_start_date)
    home_team, away_team = teams

    return {
        "date": match_date_time,
        "season": match_date_time.year,
        "round": round_number,
        "home_team": home_team,
        "away_team": away_team,
        "venue": venue,
    }


def _generate_round(season_start: datetime, week: int) -> List[BaseMatchData]:
    round_start = season_start + timedelta(days=(WEEK_IN_DAYS * week))
    round_number = week + 1

    team_count = len(NON_BRISBANE_TEAMS) + 1
    match_count = math.floor(team_count / 2)
    min_match_number = (week * match_count) + 1
    max_match_number = min_match_number + match_count

    teams = _generate_teams()
    venues = (venue for venue in np.random.permutation(VENUES))

    match_data_func = partial(
        _generate_match,
        round_number,
        round_start,
    )

    return [
        match_data_func(teams=(next(teams), next(teams)), venue=next(venues))
        for _ in range(min_match_number, max_match_number)
    ]


def _generate_season(season: int) -> List[BaseMatchData]:
    # Seasons have typically started in mid-to-late March since the 70s
    start_date = datetime(season, MAR, FIFTEENTH)
    # Typically, rounds start on Thursday or Friday and end on Sunday,
    # but can range from Wednesday to Tuesday, with a few exceptions.
    difference_from_wed = WEDNESDAY - start_date.weekday()
    season_start = start_date + timedelta(days=difference_from_wed)

    # Seasons typically end somewhere between mid September and mid October,
    # so we split the difference.
    season_end = datetime(season, SEP, THIRTIETH)
    week_count = math.floor((season_end - season_start).days / WEEK_IN_DAYS)

    return list(
        itertools.chain.from_iterable(
            [_generate_round(season_start, week) for week in range(week_count)]
        )
    )


def generate_base_data(seasons: Union[int, Tuple[int, int]]) -> pd.DataFrame:
    """Generate generic match data on which to base other data sets."""
    return pd.DataFrame(
        list(
            itertools.chain.from_iterable(
                [_generate_season(season) for season in _season_range(seasons)]
            )
        )
    )
