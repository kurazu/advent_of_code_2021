from collections import deque
from typing import Deque, Iterator, TextIO

import click

WINDOW = 3


@click.command()
@click.argument("input", type=click.File("r", encoding="utf-8"), required=True)
def main(input: TextIO) -> None:
    parsed_numbers: Iterator[int] = iter(map(int, filter(None, input)))
    previous_observations: Deque[int] = deque(maxlen=WINDOW)
    for _ in range(WINDOW):
        previous_observations.append(next(parsed_numbers))

    count = 0
    previous_sum = sum(previous_observations)
    for number in parsed_numbers:
        previous_observations.append(number)
        current_sum = sum(previous_observations)
        if current_sum > previous_sum:
            count += 1
        previous_sum = current_sum
    click.echo(f"{count}")


if __name__ == "__main__":
    main()
