import logging
from typing import List, TextIO

import numpy as np

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    fish: List[int] = list(map(int, input.readline().strip().split(",")))
    breakpoint()
    return f"{0}"


if __name__ == "__main__":
    run_with_file_argument(main)
