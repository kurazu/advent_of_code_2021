import logging
from typing import TextIO

import numpy as np

from ..cli import run_with_file_argument
from .task_1 import FOLDING_MAP, format_paper, get_folds, get_paper

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    paper = get_paper(input)
    logger.info("Initial paper\n%s", format_paper(paper))
    # not now analyze only the first fold
    folds = get_folds(input)
    for axis, value in folds:
        folding_callback = FOLDING_MAP[axis]
        paper = folding_callback(paper, value)
        logger.info("After folding %s at %s\n%s", axis.name, value, format_paper(paper))

    number_of_points = np.sum(paper > 0)

    return f"{number_of_points}"


if __name__ == "__main__":
    run_with_file_argument(main)
