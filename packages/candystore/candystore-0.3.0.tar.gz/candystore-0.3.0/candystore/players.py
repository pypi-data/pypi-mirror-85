"""Player data factory for use in CandyStore class."""

from typing import List, Dict, Tuple
import itertools

from mypy_extensions import TypedDict
import numpy as np
import pandas as pd
from faker import Faker

PlayerData = TypedDict(
    "PlayerData",
    {
        "season": int,
        "round": str,
        "date": str,
        "local_start_time": str,
        "venue": str,
        "attendance": int,
        "home_team": str,
        "hq1g": int,
        "hq1b": int,
        "hq2g": int,
        "hq2b": int,
        "hq3g": int,
        "hq3b": int,
        "hq4g": int,
        "hq4b": int,
        "home_score": int,
        "away_team": str,
        "aq1g": int,
        "aq1b": int,
        "aq2g": int,
        "aq2b": int,
        "aq3g": int,
        "aq3b": int,
        "aq4g": int,
        "aq4b": int,
        "away_score": int,
        "first_name": str,
        "surname": str,
        "id": int,
        "jumper_no": int,
        "playing_for": str,
        "kicks": int,
        "marks": int,
        "handballs": int,
        "goals": int,
        "behinds": int,
        "hit_outs": int,
        "tackles": int,
        "rebounds": int,
        "inside_50s": int,
        "clearances": int,
        "clangers": int,
        "frees_for": int,
        "frees_against": int,
        "brownlow_votes": int,
        "contested_possessions": int,
        "uncontested_possessions": int,
        "contested_marks": int,
        "marks_inside_50": int,
        "one_percenters": int,
        "bounces": int,
        "goal_assists": int,
        "time_on_ground": int,
        "substitute": int,
        "umpire_1": str,
        "umpire_2": str,
        "umpire_3": str,
        "umpire_4": str,
        "group_id": int,
    },
)

FAKE = Faker()

# Reasonable ranges are two standard deviations plus/minus from the means
# for all recorded AFL matches
REASONABLE_GOAL_RANGE = (2, 23)
REASONABLE_BEHIND_RANGE = (3, 22)
# Uses minimum attendance, because standard deviation was too large
REASONABLE_ATTENDANCE_RANGE = (1071, 61120)

FINALS_ROUND_LABELS = ["QF", "EF", "SF", "PF", "GF"]

# The following are ranges for per-player, per-match stats since 1965
REASONABLE_KICK_RANGE = (0, 21)
REASONABLE_MARK_RANGE = (0, 10)
REASONABLE_HANDBALL_RANGE = (0, 14)
REASONABLE_PLAYER_GOAL_RANGE = (0, 4)
REASONABLE_PLAYER_BEHIND_RANGE = (0, 3)
REASONABLE_HIT_OUT_RANGE = (0, 12)
REASONABLE_TACKLE_RANGE = (0, 6)
REASONABLE_REBOUND_RANGE = (0, 5)
REASONABLE_INSIDE_50_RANGE = (0, 6)
REASONABLE_CLEARANCE_RANGE = (0, 5)
REASONABLE_CLANGER_RANGE = (0, 5)
REASONABLE_FREE_FOR_RANGE = (0, 5)
REASONABLE_FREE_AGAINST_RANGE = (0, 5)
REASONABLE_CONTESTED_POSSESSION_RANGE = (0, 11)
REASONABLE_UNCONTESTED_POSSESSION_RANGE = (0, 17)
REASONABLE_CONTESTED_MARK_RANGE = (0, 3)
REASONABLE_MARK_INSIDE_50_RANGE = (0, 3)
REASONABLE_ONE_PERCENTER_RANGE = (0, 5)
REASONABLE_BOUNCE_RANGE = (0, 3)
REASONABLE_GOAL_ASSIST_RANGE = (0, 2)
REASONABLE_TIME_ON_GROUND_RANGE = (0, 116)

SUBSTITUTE_RANGE = (0, 3)
BROWNLOW_VOTES_RANGE = (0, 4)

N_PLAYERS_PER_TEAM = 22


def _calculate_quarter_values(
    value_range: Tuple[int, int], size: int
) -> List[np.array]:
    return [
        (np.random.randint(*value_range, size=size) / 4).astype(int) for _ in range(4)
    ]


def _parse_player_start_time(player_data_frame: pd.DataFrame) -> pd.Series:
    # It's a little wonky, but for player data, fitzRoy returns match times
    # in the form of 'hhmm' as an integer
    return (
        player_data_frame["date"].dt.hour.astype(str)
        + player_data_frame["date"].dt.minute.astype(str)
    ).astype(int)


def _season_finals_round_map(max_round: int) -> Dict[int, str]:
    finals_round_numbers = enumerate(
        range(max_round - len(FINALS_ROUND_LABELS) + 2, max_round + 1)
    )
    # First two finals labels (EF & QF) apply to the first round of finals
    # (i.e. they take place in the same week), so we randomly divy them up
    # for the first round before proceeding with one label per round
    round_label = lambda idx: (
        np.random.choice(FINALS_ROUND_LABELS[:2])
        if idx == 0
        else FINALS_ROUND_LABELS[idx + 1]
    )

    return {
        round_number: round_label(idx) for idx, round_number in finals_round_numbers
    }


def _generate_match_players(
    player_match_index: int, player_match_row: pd.Series
) -> List[pd.DataFrame]:
    return [
        _generate_players(player_match_index, player_match_row, team_column)
        for team_column in ["home_team", "away_team"]
    ]


def _map_player_round_per_season(season_group: pd.DataFrame) -> pd.Series:
    max_round = season_group["round"].max()
    finals_round_map = _season_finals_round_map(max_round)

    return season_group["round"].map(lambda round: finals_round_map.get(round) or round)


def _map_player_round(player_data_frame: pd.DataFrame) -> pd.Series:
    return pd.concat(
        [
            _map_player_round_per_season(season_group)
            for _season, season_group in player_data_frame.groupby("season")
        ]
    ).astype(str)


def _generate_players(
    player_match_index: int, player_match_row: pd.Series, team_column: str
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "match_id": player_match_index,
            "first_name": np.array(
                [FAKE.first_name() for _ in range(N_PLAYERS_PER_TEAM)]
            ),
            "surname": np.array([FAKE.last_name() for _ in range(N_PLAYERS_PER_TEAM)]),
            "id": np.array(range(N_PLAYERS_PER_TEAM))
            + (player_match_index * N_PLAYERS_PER_TEAM * 2),
            "jumper_no": np.random.randint(0, 100, size=N_PLAYERS_PER_TEAM),
            "playing_for": player_match_row[team_column],
            "kicks": np.random.randint(*REASONABLE_KICK_RANGE, size=N_PLAYERS_PER_TEAM),
            "marks": np.random.randint(*REASONABLE_MARK_RANGE, size=N_PLAYERS_PER_TEAM),
            "handballs": np.random.randint(
                *REASONABLE_HANDBALL_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            # Acknowledging that this means that the sum of player goals
            # is unlikely to equal the sum of team quarter goals,
            # but no point in over-complicating calculations until we need to.
            "goals": np.random.randint(
                *REASONABLE_PLAYER_GOAL_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "behinds": np.random.randint(
                *REASONABLE_PLAYER_BEHIND_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "hit_outs": np.random.randint(
                *REASONABLE_HIT_OUT_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "tackles": np.random.randint(
                *REASONABLE_TACKLE_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "rebounds": np.random.randint(
                *REASONABLE_REBOUND_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "inside_50s": np.random.randint(
                *REASONABLE_INSIDE_50_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "clearances": np.random.randint(
                *REASONABLE_CLEARANCE_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "clangers": np.random.randint(
                *REASONABLE_CLANGER_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "frees_for": np.random.randint(
                *REASONABLE_FREE_FOR_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "frees_against": np.random.randint(
                *REASONABLE_FREE_AGAINST_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            # Acknowledging that this won't restrict brownlow votes to 3 players
            # per match, but no point in over-complicating calculations
            # until we need to.
            "brownlow_votes": np.random.randint(
                *BROWNLOW_VOTES_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "contested_possessions": np.random.randint(
                *REASONABLE_CONTESTED_POSSESSION_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "uncontested_possessions": np.random.randint(
                *REASONABLE_UNCONTESTED_POSSESSION_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "contested_marks": np.random.randint(
                *REASONABLE_CONTESTED_MARK_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "marks_inside_50": np.random.randint(
                *REASONABLE_MARK_INSIDE_50_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "one_percenters": np.random.randint(
                *REASONABLE_ONE_PERCENTER_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "bounces": np.random.randint(
                *REASONABLE_BOUNCE_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "goal_assists": np.random.randint(
                *REASONABLE_GOAL_ASSIST_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "time_on_ground": np.random.randint(
                *REASONABLE_TIME_ON_GROUND_RANGE, size=N_PLAYERS_PER_TEAM
            ),
            "substitute": np.random.randint(*SUBSTITUTE_RANGE, size=N_PLAYERS_PER_TEAM),
        }
    )


def convert_to_players(base_match_data_frame: pd.DataFrame) -> pd.DataFrame:
    """Convert base match data to player data."""
    match_count = len(base_match_data_frame)

    home_quarter_goals = _calculate_quarter_values(REASONABLE_GOAL_RANGE, match_count)
    home_quarter_behinds = _calculate_quarter_values(
        REASONABLE_BEHIND_RANGE, match_count
    )
    away_quarter_goals = _calculate_quarter_values(REASONABLE_GOAL_RANGE, match_count)
    away_quarter_behinds = _calculate_quarter_values(
        REASONABLE_BEHIND_RANGE, match_count
    )

    player_match_data = (
        base_match_data_frame.assign(
            round=_map_player_round,
            local_start_time=_parse_player_start_time,
            date=lambda df: df["date"].dt.date.astype(str),
            attendance=np.random.randint(
                *REASONABLE_ATTENDANCE_RANGE, size=match_count
            ),
            hq1g=home_quarter_goals[0],
            hq1b=home_quarter_behinds[0],
            hq2g=home_quarter_goals[1],
            hq2b=home_quarter_behinds[1],
            hq3g=home_quarter_goals[2],
            hq3b=home_quarter_behinds[2],
            hq4g=home_quarter_goals[3],
            hq4b=home_quarter_behinds[3],
            home_score=(np.sum(home_quarter_goals, axis=0) * 6)
            + np.sum(home_quarter_behinds, axis=0),
            aq1g=away_quarter_goals[0],
            aq1b=away_quarter_behinds[0],
            aq2g=away_quarter_goals[1],
            aq2b=away_quarter_behinds[1],
            aq3g=away_quarter_goals[2],
            aq3b=away_quarter_behinds[2],
            aq4g=away_quarter_goals[3],
            aq4b=away_quarter_behinds[3],
            away_score=(np.sum(home_quarter_goals, axis=0) * 6)
            + np.sum(home_quarter_behinds, axis=0),
            umpire_1=np.array([FAKE.name() for _ in range(match_count)]),
            umpire_2=np.array([FAKE.name() for _ in range(match_count)]),
            umpire_3=np.array([FAKE.name() for _ in range(match_count)]),
            umpire_4=np.array([FAKE.name() for _ in range(match_count)]),
            # Not totally sure what this is for, so a random integer
            # should be good enough
            group_id=np.random.randint(1000, size=match_count),
        )
        .reset_index()
        .rename(columns={"index": "match_id"})
    )

    player_data = pd.concat(
        list(
            itertools.chain.from_iterable(
                [
                    _generate_match_players(idx, row)
                    for idx, row in player_match_data.iterrows()
                ]
            )
        )
    )

    return player_match_data.merge(player_data, how="right", on="match_id").drop(
        "match_id", axis=1
    )
