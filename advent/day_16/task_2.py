import logging
from typing import TextIO

from ..cli import run_with_file_argument
from ..io_utils import read_line
from .task_1 import get_binary, read_packet

logger = logging.getLogger(__name__)


def main(input: TextIO) -> str:
    # read the map
    message = read_line(input)
    binary_message = get_binary(message)

    packet = read_packet(binary_message)
    logger.info("Packet read %s", packet)

    value = packet.get_value()
    return f"{value}"


if __name__ == "__main__":
    run_with_file_argument(main)
