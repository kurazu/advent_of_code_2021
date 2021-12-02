from typing import TextIO

import pandas as pd

from ..cli import run_with_file_argument


def main(input: TextIO) -> str:
    df = pd.read_csv(input, names=["reading"])
    df["prev_reading"] = df.reading.shift(1)
    df.dropna(subset=["prev_reading"], inplace=True)
    count = (df["reading"] > df["prev_reading"]).sum()
    return f"{count}"


if __name__ == "__main__":
    run_with_file_argument(main)
