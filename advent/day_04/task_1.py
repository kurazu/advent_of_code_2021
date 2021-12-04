import logging
from typing import TextIO

import pandas as pd

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    last_number = 0
    winning_board_sum = 0
    logger.info("last_number=%d, winning_board_sum=%d", last_number, winning_board_sum)
    return f"{last_number * winning_board_sum}"


if __name__ == "__main__":
    run_with_file_argument(main)
