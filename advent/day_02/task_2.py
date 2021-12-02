import logging
from typing import TextIO

import pandas as pd

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    df = pd.read_csv(input, names=["direction", "distance"], delimiter=" ")
    df["horizontal_factor"] = df["direction"].map({"forward": 1, "down": 0, "up": 0})
    df["aim_factor"] = df["direction"].map({"forward": 0, "down": 1, "up": -1})
    df["horizontal"] = df["horizontal_factor"] * df["distance"]
    df["aim"] = df["aim_factor"] * df["distance"]
    df["current_aim"] = df["aim"].cumsum()
    df["vertical"] = df["horizontal_factor"] * df["distance"] * df["current_aim"]

    horizontal = df["horizontal"].sum()
    vertical = df["vertical"].sum()
    logger.info("horizontal=%d, vertical=%d", horizontal, vertical)
    return f"{horizontal * vertical}"


if __name__ == "__main__":
    run_with_file_argument(main)
