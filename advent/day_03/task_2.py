import logging
from typing import Callable, TextIO

import pandas as pd

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)


def get_most_common_character(column: pd.Series) -> str:
    counts = column.value_counts()
    one_count = counts.loc["1"]
    zero_count = counts.loc["0"]
    if one_count >= zero_count:
        return "1"
    else:
        return "0"


def get_least_common_character(column: pd.Series) -> str:
    counts = column.value_counts()
    one_count = counts.loc["1"]
    zero_count = counts.loc["0"]
    if zero_count <= one_count:
        return "0"
    else:
        return "1"


def find_rating(
    positional_df: pd.DataFrame, criterion: Callable[[pd.Series], str]
) -> str:
    filtered_df = positional_df.copy()
    for column_name in filtered_df.columns:
        column = filtered_df[column_name]
        desired_character = criterion(column)
        filtered_df = filtered_df[column == desired_character]
        if len(filtered_df) == 1:
            break
        elif len(filtered_df) == 0:
            raise AssertionError("Out of data")
        else:
            continue

    assert len(filtered_df) == 1
    rating = "".join(filtered_df.iloc[0])
    return rating


def main(input: TextIO) -> str:
    df = pd.read_csv(input, names=["binary"], dtype={"binary": str})
    positional_df = df["binary"].apply(
        lambda binary_number: pd.Series(list(binary_number))
    )

    oxygen_rating_string = find_rating(positional_df, get_most_common_character)
    co2_rating_string = find_rating(positional_df, get_least_common_character)
    oxygen_rating = int(oxygen_rating_string, 2)
    co2_rating = int(co2_rating_string, 2)
    logger.info("oxygen_rating=%d, co2_rating=%d", oxygen_rating, co2_rating)
    return f"{oxygen_rating * co2_rating}"


if __name__ == "__main__":
    run_with_file_argument(main)
