# pylint: disable=missing-module-docstring,missing-function-docstring,redefined-outer-name
# pylint: disable=no-member
import re

import pytest
from rpy2.robjects import packages, pandas2ri
import pandas as pd
from pandas.api.types import is_string_dtype, is_numeric_dtype, is_datetime64_dtype
import numpy as np

from candystore import CandyStore

pandas2ri.activate()

fitzroy = packages.importr("fitzRoy")


def clean_column_names(data_frame: pd.DataFrame):
    return data_frame.rename(
        columns=lambda col: re.sub(r"^\.+|\.+$", "", col).replace(".", "_").lower()
    )


fixtures = clean_column_names(fitzroy.get_fixture())
match_results = clean_column_names(fitzroy.get_match_results())
players = clean_column_names(
    fitzroy.get_afltables_stats(start_date="2019-01-01", end_date="2019-12-31")
)
betting_odds = clean_column_names(
    fitzroy.get_footywire_betting_odds(start_season="2019", end_season="2019")
)

data_factory = CandyStore(seasons=np.random.randint(1, 10))


@pytest.mark.parametrize(
    ["data_type", "fitzroy_data"],
    [
        ("fixtures", fixtures),
        ("betting_odds", betting_odds),
        ("match_results", match_results),
        ("players", players),
    ],
)
def test_matching_column_names(data_type, fitzroy_data):
    data = getattr(data_factory, data_type)(to_dict=None)
    data_columns = set(data.columns)

    fitzroy_data_columns = set(clean_column_names(fitzroy_data).columns)

    assert data_columns == fitzroy_data_columns


@pytest.mark.parametrize(
    ["data_type", "fitzroy_data"],
    [
        ("fixtures", fixtures),
        ("betting_odds", betting_odds),
        ("match_results", match_results),
        ("players", players),
    ],
)
def test_matching_data_types(data_type, fitzroy_data):
    data = getattr(data_factory, data_type)(to_dict=None)

    for column_name, fitzroy_column in fitzroy_data.iteritems():
        data_column = data[column_name]
        # rpy2 does some weird conversions for datetime columns, so we don't compare
        # the data frames directly.
        if column_name == "date":
            assert is_string_dtype(data_column)
            assert is_datetime64_dtype(pd.to_datetime(data_column))
            continue

        # rpy2 isn't super consistent with its numeric dtypes
        # (e.g. sometimes converting ints in R to floats in Pandas,
        # being all over the shop with 32- vs 64-bit numbers), so we use a generic
        # numeric or string dtype comparison.
        both_are_strings = is_string_dtype(data_column) and is_string_dtype(
            fitzroy_column
        )
        both_are_numeric = is_numeric_dtype(data_column) and is_numeric_dtype(
            fitzroy_column
        )
        assert (
            both_are_strings or both_are_numeric
        ), f"Candystore:\n{data_column}\n\nFitzRoy:\n{fitzroy_column}"
