import logging
from typing import TextIO

import numpy as np

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    overlapping_points = 0
    return f"overlapping_points"


if __name__ == "__main__":
    run_with_file_argument(main)
