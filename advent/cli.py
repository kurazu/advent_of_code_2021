import gzip
import logging
from pathlib import Path
from typing import Callable, TextIO, cast

import click

from .logs import setup_logging

logger = logging.getLogger(__name__)


def run_with_file_argument(callback: Callable[[TextIO], str]) -> None:
    @click.command()
    @click.argument(
        "input_file_path",
        type=click.Path(file_okay=True, dir_okay=False, readable=True, path_type=Path),
        required=True,
    )
    def main(input_file_path: Path) -> None:
        if input_file_path.suffix == ".gz":
            logger.debug("Reading %s as GZIP file", input_file_path)
            file_opener = gzip.open(input_file_path, mode="rt", encoding="utf-8")
        else:
            logger.debug("Reading %s as plain file", input_file_path)
            file_opener = input_file_path.open(mode="r", encoding="utf-8")
        with file_opener as file:
            result = callback(file)
        click.echo(result)

    setup_logging()
    main()
