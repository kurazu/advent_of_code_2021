from typing import Iterator, TextIO

import click


@click.command()
@click.argument(
    "input", type=click.File("r", encoding="utf-8"), required=True, default="-"
)
def main(input: TextIO) -> None:
    parsed_numbers: Iterator[int] = iter(map(int, filter(None, input)))
    last = next(parsed_numbers)
    count = 0
    for number in parsed_numbers:
        if number > last:
            count += 1
        last = number
    click.echo(f"{count}")


if __name__ == "__main__":
    main()
