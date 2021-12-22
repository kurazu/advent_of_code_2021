from __future__ import annotations

import logging

from returns.curry import partial

from ..cli import run_with_file_argument
from .task_1 import main

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    run_with_file_argument(partial(main, iterations=50))
