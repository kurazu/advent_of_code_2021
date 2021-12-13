import enum
import itertools
import logging
import re
from typing import Callable, Dict, Iterable, List, Optional, TextIO, Tuple

import numpy as np
import numpy.typing as npt

from ..cli import run_with_file_argument
from ..io_utils import get_lines

logger = logging.getLogger(__name__)
PATTERN = re.compile(r"^fold along (?P<axis>[xy])=(?P<value>\d+)$")


class FoldAxis(enum.Enum):
    FOLD_UP = "y"
    FOLD_LEFT = "x"


def get_paper(input: TextIO) -> npt.NDArray[bool]:
    stripped_lines = map(str.strip, input)
    point_x: List[int] = []
    point_y: List[int] = []
    for line in stripped_lines:
        if not line:
            break  # the dots sections is finished
        x, y = map(int, line.split(","))
        point_x.append(x)
        point_y.append(y)
    xs = np.array(point_x)
    ys = np.array(point_y)
    del point_x
    del point_y
    width = np.max(xs)
    height = np.max(ys)
    paper = np.zeros((height + 1, width + 1), dtype=bool)
    paper[[ys, xs]] = True
    return paper


def get_folds(input: TextIO) -> Iterable[Tuple[FoldAxis, int]]:
    for line in get_lines(input):
        match = PATTERN.match(line)
        assert match is not None
        axis = FoldAxis(match.group("axis"))
        value = int(match.group("value"))
        yield axis, value


bool_array_to_string = np.vectorize({False: ".", True: "#"}.__getitem__)


def format_paper(paper: npt.NDArray[bool]) -> str:
    string_array = bool_array_to_string(paper)
    return "\n".join(map("".join, string_array))


def fold_left(paper: npt.NDArray[bool], fold_line: int) -> npt.NDArray[bool]:
    # split along the verical line
    leftside = paper[:, :fold_line]
    rightside = paper[:, fold_line + 1 :]
    # flip the right side left-to-right
    flipped_rightside = rightside[:, ::-1]
    # create a new canvas the size of the bigger part
    height, leftside_width = leftside.shape
    height, rightside_width = flipped_rightside.shape
    canvas = np.zeros((height, max(leftside_width, rightside_width)), dtype=bool)
    # paint both leftside and flipped rightside onto the canvas
    # anchoring both at the canvas right
    canvas[:, -leftside_width:] |= leftside
    canvas[:, -rightside_width:] |= flipped_rightside
    return canvas


def fold_up(paper: npt.NDArray[bool], fold_line: int) -> npt.NDArray[bool]:
    # split along the horizontal line
    upside = paper[:fold_line, :]
    downside = paper[fold_line + 1 :, :]
    # flip the bottom part upside-down
    flipped_downside = downside[::-1, :]
    # create a new canvas the size of the bigger part
    upside_height, width = upside.shape
    downside_height = len(flipped_downside)
    canvas = np.zeros((max(upside_height, downside_height), width), dtype=bool)
    # paint both upside and flipped downside onto the canvas
    # anchoring both at the canvas bottom
    canvas[-upside_height:, :] |= upside
    canvas[-downside_height:, :] |= flipped_downside
    return canvas


FOLDING_MAP: Dict[FoldAxis, Callable[[npt.NDArray[bool], int], npt.NDArray[bool]]] = {
    FoldAxis.FOLD_LEFT: fold_left,
    FoldAxis.FOLD_UP: fold_up,
}


def main(input: TextIO) -> str:
    paper = get_paper(input)
    logger.info("Initial paper\n%s", format_paper(paper))
    # not now analyze only the first fold
    folds = get_folds(input)
    folds = itertools.islice(folds, 1)
    for axis, value in folds:
        folding_callback = FOLDING_MAP[axis]
        paper = folding_callback(paper, value)
        logger.info("After folding %s at %s\n%s", axis.name, value, format_paper(paper))

    number_of_points = np.sum(paper > 0)

    return f"{number_of_points}"


if __name__ == "__main__":
    run_with_file_argument(main)
