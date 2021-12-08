import logging
from typing import List, TextIO

import numpy as np

from ..cli import run_with_file_argument

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    stripped_lines = (line.strip() for line in input)
    non_empty_stripped_lines = filter(None, stripped_lines)
    all_signals: List[List[str]] = []
    all_outputs: List[List[str]] = []
    for line in non_empty_stripped_lines:
        _signals, _outputs = line.split(" | ")
        signals = _signals.split(" ")
        outputs = _outputs.split(" ")
        assert len(signals) == 10
        assert len(outputs) == 4
        all_signals.append(signals)
        all_outputs.append(outputs)
    breakpoint()
    occurrences = 0
    return f"{occurrences}"


if __name__ == "__main__":
    run_with_file_argument(main)
