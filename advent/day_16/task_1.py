import functools
import io
import logging
import operator
from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Protocol, TextIO

from ..cli import run_with_file_argument
from ..io_utils import read_line

logger = logging.getLogger(__name__)


@dataclass
class Packet:
    version: int

    def get_value(self) -> int:
        raise NotImplementedError()


@dataclass
class LiteralPacket(Packet):
    value: int

    def get_value(self) -> int:
        return self.value


@dataclass
class OperatorPacket(Packet):
    cargo: List[Packet]

    def get_values(self) -> Iterable[int]:
        return (packet.get_value() for packet in self.cargo)


@dataclass
class SumPacket(OperatorPacket):
    def get_value(self) -> int:
        return sum(self.get_values())


@dataclass
class ProductPacket(OperatorPacket):
    def get_value(self) -> int:
        return functools.reduce(operator.mul, self.get_values())


@dataclass
class MinPacket(OperatorPacket):
    def get_value(self) -> int:
        return min(self.get_values())


@dataclass
class MaxPacket(OperatorPacket):
    def get_value(self) -> int:
        return max(self.get_values())


@dataclass
class GreaterPacket(OperatorPacket):
    def get_value(self) -> int:
        first, second = self.get_values()
        return first > second


@dataclass
class LessPacket(OperatorPacket):
    def get_value(self) -> int:
        first, second = self.get_values()
        return first < second


@dataclass
class EqualPacket(OperatorPacket):
    def get_value(self) -> int:
        first, second = self.get_values()
        return first == second


class OperatorPacketCreator(Protocol):
    def __call__(self, version: int, cargo: List[Packet]) -> OperatorPacket:
        ...


LITERAL_PACKET_TYPE_ID = 4
OPERATOR_PACKET_TYPES: Dict[int, OperatorPacketCreator] = {
    0: SumPacket,
    1: ProductPacket,
    2: MinPacket,
    3: MaxPacket,
    5: GreaterPacket,
    6: LessPacket,
    7: EqualPacket,
}


def read_literal_packet(version: int, buf: io.StringIO) -> LiteralPacket:
    literal_value_buf = io.StringIO()
    continue_flag = True
    while continue_flag:
        continue_flag = buf.read(1) == "1"
        value = buf.read(4)
        literal_value_buf.write(value)
    literal_value = int(literal_value_buf.getvalue(), 2)
    return LiteralPacket(version=version, value=literal_value)


def read_subpackets_by_length(buf: io.StringIO) -> List[Packet]:
    length = int(buf.read(15), 2)
    position = buf.tell()
    subpackets: List[Packet] = []
    while buf.tell() < position + length:
        subpackets.append(read_packet(buf))
    assert buf.tell() == position + length
    return subpackets


def read_subpackets_by_count(buf: io.StringIO) -> List[Packet]:
    count = int(buf.read(11), 2)
    return [read_packet(buf) for _ in range(count)]


def read_operator_packet(
    *, version: int, type_id: int, buf: io.StringIO
) -> OperatorPacket:
    length_mode = buf.read(1)
    subpackets: List[Packet] = []
    if length_mode == "0":
        subpackets = read_subpackets_by_length(buf)
    else:
        assert length_mode == "1"
        subpackets = read_subpackets_by_count(buf)
    return OPERATOR_PACKET_TYPES[type_id](version=version, cargo=subpackets)


def read_packet(buf: io.StringIO) -> Packet:
    version = int(buf.read(3), 2)
    type_id = int(buf.read(3), 2)
    if type_id == LITERAL_PACKET_TYPE_ID:
        return read_literal_packet(version, buf)
    else:
        return read_operator_packet(version=version, type_id=type_id, buf=buf)


def get_binary(message: str) -> io.StringIO:
    buf = io.StringIO()
    for char in message:
        value = int(char, 16)
        binary_string = bin(value)[2:].rjust(4, "0")
        assert len(binary_string) == 4
        buf.write(binary_string)
    buf.seek(0)
    return buf


def get_packets(root: Packet) -> Iterable[Packet]:
    yield root
    if isinstance(root, OperatorPacket):
        for packet in root.cargo:
            yield from get_packets(packet)


def get_version_sum(root: Packet) -> int:
    return sum(packet.version for packet in get_packets(root))


def main(input: TextIO) -> str:
    # read the map
    message = read_line(input)
    binary_message = get_binary(message)

    packet = read_packet(binary_message)
    logger.info("Packet read %s", packet)

    version_sum = get_version_sum(packet)
    return f"{version_sum}"


if __name__ == "__main__":
    run_with_file_argument(main)
