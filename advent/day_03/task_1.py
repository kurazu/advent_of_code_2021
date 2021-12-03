import logging
from typing import TextIO

import pandas as pd

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    df = pd.read_csv(input, names=["binary"], dtype={"binary": str})
    positional_df = df["binary"].apply(
        lambda binary_number: pd.Series(list(binary_number))
    )

    most_common_characters = positional_df.apply(
        lambda column: column.value_counts().sort_values().index[-1], axis="index"
    )
    least_common_characters = most_common_characters.map({"0": "1", "1": "0"})
    epsilon_string = "".join(most_common_characters)
    epsilon = int(epsilon_string, 2)
    gamma_string = "".join(least_common_characters)
    gamma = int(gamma_string, 2)
    logger.info("gamma=%d, epsilon=%d", gamma, epsilon)
    return f"{gamma * epsilon}"


if __name__ == "__main__":
    run_with_file_argument(main)
