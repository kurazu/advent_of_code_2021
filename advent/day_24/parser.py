import logging
import re
from io import StringIO
from types import ModuleType
from typing import Callable, List, TextIO, Tuple

from ..io_utils import get_lines

logger = logging.getLogger(__name__)
VAR = r"(w|x|y|z)"
INT = r"(\-?\d+)"
VAR_OR_INT = rf"({VAR}|{INT})"

INSTRUCTIONS: List[Tuple[str, str]] = [
    (rf"^inp (?P<a>{VAR})$", "{a} = inputs.pop(0)"),
    (rf"^add (?P<a>{VAR}) (?P<b>{VAR_OR_INT})$", "{a} += {b}"),
    (rf"^mul (?P<a>{VAR}) (?P<b>{VAR_OR_INT})$", "{a} *= {b}"),
    (rf"^div (?P<a>{VAR}) (?P<b>{VAR_OR_INT})$", "{a} //= {b}"),
    (rf"^mod (?P<a>{VAR}) (?P<b>{VAR_OR_INT})$", "{a} %= {b}"),
    (rf"^eql (?P<a>{VAR}) (?P<b>{VAR_OR_INT})$", "{a} = int({a} == {b})"),
]


def parse_line(line: str) -> str:
    for pattern, format_string in INSTRUCTIONS:
        match = re.match(pattern, line)
        if match is not None:
            break
    else:
        raise AssertionError(f"Line not matched {line!r}")
    return format_string.format(**match.groupdict())


def parse_program(buf: StringIO, input: TextIO) -> None:
    for line in get_lines(input):
        code = parse_line(line)
        buf.write(f"    {code}\n")


def convert_to_python(input: TextIO) -> str:
    buf = StringIO()
    buf.write("from typing import List, Tuple\n")
    buf.write("\n")
    buf.write("def program(inputs: List[int]) -> Tuple[int, int, int, int]:\n")
    buf.write("    w = x = y = z = 0\n")
    parse_program(buf, input)
    buf.write("    return w, x, y, z\n")
    return buf.getvalue()


def compile_program(input: TextIO) -> Callable[[List[int]], Tuple[int, int, int, int]]:
    python_text = convert_to_python(input)
    logger.debug("Python code:\n%s", python_text)
    code = compile(python_text, "<string>", "exec")
    module = ModuleType("fake")
    exec(code, module.__dict__)
    program: Callable[[List[int]], Tuple[int, int, int, int]] = getattr(
        module, "program"
    )
    return program
