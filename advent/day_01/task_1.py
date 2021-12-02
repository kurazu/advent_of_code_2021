from typing import TextIO

import click
import pandas as pd


@click.command()
@click.argument("input", type=click.File("r", encoding="utf-8"), required=True)
def main(input: TextIO) -> None:
    df = pd.read_csv(input, names=["reading"])
    df["prev_reading"] = df.reading.shift(1)
    df.dropna(subset=["prev_reading"], inplace=True)
    count = (df["reading"] > df["prev_reading"]).sum()
    click.echo(f"{count}")


if __name__ == "__main__":
    main()
