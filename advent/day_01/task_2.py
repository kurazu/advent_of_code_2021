from typing import TextIO

import pandas as pd

from ..cli import run_with_file_argument

WINDOW = 3


def main(input: TextIO) -> str:
    df = pd.read_csv(input, names=["reading"])
    df["current_sum"] = df.reading.rolling(WINDOW).sum()
    df["previous_sum"] = df.reading.shift(1).rolling(WINDOW).sum()
    df.dropna(subset=["previous_sum"], inplace=True)
    count = (df["current_sum"] > df["previous_sum"]).sum()
    return f"{count}"


if __name__ == "__main__":
    run_with_file_argument(main)
