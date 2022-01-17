import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


class Var(Enum):
    W = "w"
    X = "x"
    Y = "y"
    Z = "z"


VARS = "(" + "|".join(var.value for var in Var) + ")"


@instruction(rf"inp\s {VARS}")
def inp(alu: ALU, a: Var) -> None:
    alu.vars[a] = alu.read_input()


def add_reg(alu: ALU, a: Var, b: Var) -> None:
    alu.vars[a] += alu.vars[b]


def add_const(alu: ALU, a: Var, b: int) -> None:
    alu.vars[a] += alu.vars[b]


@dataclass
class ALU:
    vars: Dict[Var, int] = field(default_factory=lambda: {var: 0 for var in Var})


def program(inputs: List[int]) -> Tuple[int, int, int, int]:
    w = x = y = z = 0
    # inp w
    w = inputs.pop(0)
    return w, z, y, z
