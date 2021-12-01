from typing import TextIO

import click
import pandas as pd

WINDOW = 3


@click.command()
@click.argument("input", type=click.File("r", encoding="utf-8"), required=True)
def main(input: TextIO) -> None:
    df = pd.read_csv(input, names=["reading"])
    df["current_sum"] = df.reading.rolling(WINDOW).sum()
    df["previous_sum"] = df.reading.shift(1).rolling(WINDOW).sum()
    df.dropna(subset=["previous_sum"], inplace=True)
    count = (df["current_sum"] > df["previous_sum"]).sum()
    click.echo(f"{count}")


if __name__ == "__main__":
    main()
