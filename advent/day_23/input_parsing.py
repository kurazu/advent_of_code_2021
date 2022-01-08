from __future__ import annotations

import re
from typing import Dict, Optional, TextIO

from .enums import Amphipod

PATTERN = re.compile(
    r"^\#\#\#\#\#\#\#\#\#\#\#\#\#\n"
    r"\#\.\.\.\.\.\.\.\.\.\.\.\#\n"
    r"\#\#\#(?P<AH>[A-D])\#(?P<BH>[A-D])\#(?P<CH>[A-D])\#(?P<DH>[A-D])\#\#\#\n"
    r"\s\s\#(?P<AL>[A-D])\#(?P<BL>[A-D])\#(?P<CL>[A-D])\#(?P<DL>[A-D])\#\n"
    r"\s\s\#\#\#\#\#\#\#\#\#$"
)


def read_board(input: TextIO) -> Dict[str, Optional[Amphipod]]:
    text = input.read()
    match = PATTERN.match(text)
    assert match
    match_groups = match.groupdict()
    return {key: Amphipod(value) for key, value in match_groups.items()}
