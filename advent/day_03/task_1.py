import logging
from typing import TextIO

import pandas as pd

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    pd.read_csv(input, names="binary")
    gamma = 0
    epsilon = 0
    logger.info("gamma=%d, epsilon=%d", gamma, epsilon)
    return f"{gamma * epsilon}"


if __name__ == "__main__":
    run_with_file_argument(main)
