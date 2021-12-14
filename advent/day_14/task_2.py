from returns.curry import partial

from ..cli import run_with_file_argument
from .task_1 import main

if __name__ == "__main__":
    run_with_file_argument(partial(main, steps=40))
