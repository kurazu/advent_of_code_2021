import logging
from typing import TextIO

import pandas as pd

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    df = pd.read_csv(input, names=["direction", "distance"], delimiter=" ")
    df["x_factor"] = df["direction"].map({"forward": 1, "down": 0, "up": 0})
    df["y_factor"] = df["direction"].map({"forward": 0, "down": 1, "up": -1})
    df["x"] = df["x_factor"] * df["distance"]
    df["y"] = df["y_factor"] * df["distance"]
    x = df["x"].sum()
    y = df["y"].sum()
    logger.info("X=%d, Y=%d", x, y)
    return f"{x * y}"


if __name__ == "__main__":
    run_with_file_argument(main)
