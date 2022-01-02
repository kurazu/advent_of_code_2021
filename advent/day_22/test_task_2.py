import logging
from typing import Any, List, Tuple

import pytest

from .task_1 import Instruction
from .task_2 import apply_instructions, get_reactor

TASK_2_SAMPLES: List[Tuple[List[Instruction], int]] = [
    # manual sample 4 (line with break and a skip)
    (
        [
            Instruction(
                state=True, min_x=-6, max_x=4, min_y=1, max_y=1, min_z=1, max_z=1
            )
        ],
        11,
    ),
    # manual sample 4 (line with break and a skip)
    (
        [
            Instruction(
                state=True, min_x=-6, max_x=4, min_y=1, max_y=1, min_z=1, max_z=1
            ),
            Instruction(
                state=False, min_x=-3, max_x=-1, min_y=1, max_y=1, min_z=1, max_z=1
            ),
        ],
        11 - 3,
    ),
    # manual sample 4 (line with break and a skip)
    (
        [
            Instruction(
                state=True, min_x=-6, max_x=4, min_y=1, max_y=1, min_z=1, max_z=1
            ),
            Instruction(
                state=False, min_x=-3, max_x=-1, min_y=1, max_y=1, min_z=1, max_z=1
            ),
            Instruction(
                state=False, min_x=2, max_x=2, min_y=1, max_y=1, min_z=1, max_z=1
            ),
        ],
        11 - 3 - 1,
    ),
    # manual sample 3 (line with a break)
    (
        [
            Instruction(
                state=True, min_x=-6, max_x=1, min_y=1, max_y=1, min_z=1, max_z=1
            )
        ],
        8,
    ),
    # manual sample 3 (line with a break)
    (
        [
            Instruction(
                state=True, min_x=-6, max_x=1, min_y=1, max_y=1, min_z=1, max_z=1
            ),
            Instruction(
                state=False, min_x=-3, max_x=-2, min_y=1, max_y=1, min_z=1, max_z=1
            ),
        ],
        8 - 2,
    ),
    # manual sample 2 (donut)
    (
        [
            Instruction(
                state=True, min_x=-6, max_x=1, min_y=-2, max_y=2, min_z=1, max_z=1
            ),
        ],
        8 * 5,
    ),
    # manual sample 2 (donut)
    (
        [
            Instruction(
                state=True, min_x=-6, max_x=1, min_y=-2, max_y=2, min_z=1, max_z=1
            ),
            Instruction(
                state=False, min_x=-3, max_x=-2, min_y=-1, max_y=1, min_z=1, max_z=1
            ),
        ],
        8 * 5 - 2 * 3,
    ),
    # first manual sample
    (
        [
            Instruction(
                state=True, min_x=-2, max_x=3, min_y=1, max_y=1, min_z=1, max_z=1
            ),
            Instruction(
                state=False, min_x=0, max_x=6, min_y=1, max_y=1, min_z=1, max_z=1
            ),
            Instruction(
                state=True, min_x=4, max_x=8, min_y=1, max_y=1, min_z=1, max_z=1
            ),
        ],
        7,
    ),
    # first manual sample scaled to more dimensions
    (
        [
            Instruction(
                state=True, min_x=-2, max_x=3, min_y=1, max_y=2, min_z=1, max_z=3
            ),
            Instruction(
                state=False, min_x=0, max_x=6, min_y=1, max_y=2, min_z=1, max_z=3
            ),
            Instruction(
                state=True, min_x=4, max_x=8, min_y=1, max_y=2, min_z=1, max_z=3
            ),
        ],
        42,
    ),
    # task 1 sample
    (
        [
            Instruction(
                state=True, min_x=10, max_x=12, min_y=10, max_y=12, min_z=10, max_z=12
            ),
        ],
        27,
    ),
    # task 1 sample
    (
        [
            Instruction(
                state=True, min_x=10, max_x=12, min_y=10, max_y=12, min_z=10, max_z=12
            ),
            Instruction(
                state=True, min_x=11, max_x=13, min_y=11, max_y=13, min_z=11, max_z=13
            ),
        ],
        27 + 19,
    ),
    # task 1 sample
    (
        [
            Instruction(
                state=True, min_x=10, max_x=12, min_y=10, max_y=12, min_z=10, max_z=12
            ),
            Instruction(
                state=True, min_x=11, max_x=13, min_y=11, max_y=13, min_z=11, max_z=13
            ),
            Instruction(
                state=False, min_x=9, max_x=11, min_y=9, max_y=11, min_z=9, max_z=11
            ),
        ],
        27 + 19 - 8,
    ),
    # task 1 sample
    (
        [
            Instruction(
                state=True, min_x=10, max_x=12, min_y=10, max_y=12, min_z=10, max_z=12
            ),
            Instruction(
                state=True, min_x=11, max_x=13, min_y=11, max_y=13, min_z=11, max_z=13
            ),
            Instruction(
                state=False, min_x=9, max_x=11, min_y=9, max_y=11, min_z=9, max_z=11
            ),
            Instruction(
                state=True, min_x=10, max_x=10, min_y=10, max_y=10, min_z=10, max_z=10
            ),
        ],
        39,
    ),
    # task 2 sample
    (
        [
            Instruction(
                state=True, min_x=-20, max_x=26, min_y=-36, max_y=17, min_z=-47, max_z=7
            ),
            Instruction(
                state=True,
                min_x=-20,
                max_x=33,
                min_y=-21,
                max_y=23,
                min_z=-26,
                max_z=28,
            ),
            Instruction(
                state=True,
                min_x=-22,
                max_x=28,
                min_y=-29,
                max_y=23,
                min_z=-38,
                max_z=16,
            ),
            Instruction(
                state=True, min_x=-46, max_x=7, min_y=-6, max_y=46, min_z=-50, max_z=-1
            ),
            Instruction(
                state=True, min_x=-49, max_x=1, min_y=-3, max_y=46, min_z=-24, max_z=28
            ),
            Instruction(
                state=True, min_x=2, max_x=47, min_y=-22, max_y=22, min_z=-23, max_z=27
            ),
            Instruction(
                state=True,
                min_x=-27,
                max_x=23,
                min_y=-28,
                max_y=26,
                min_z=-21,
                max_z=29,
            ),
            Instruction(
                state=True, min_x=-39, max_x=5, min_y=-6, max_y=47, min_z=-3, max_z=44
            ),
            Instruction(
                state=True, min_x=-30, max_x=21, min_y=-8, max_y=43, min_z=-13, max_z=34
            ),
            Instruction(
                state=True,
                min_x=-22,
                max_x=26,
                min_y=-27,
                max_y=20,
                min_z=-29,
                max_z=19,
            ),
            Instruction(
                state=False,
                min_x=-48,
                max_x=-32,
                min_y=26,
                max_y=41,
                min_z=-47,
                max_z=-37,
            ),
            Instruction(
                state=True, min_x=-12, max_x=35, min_y=6, max_y=50, min_z=-50, max_z=-2
            ),
            Instruction(
                state=False,
                min_x=-48,
                max_x=-32,
                min_y=-32,
                max_y=-16,
                min_z=-15,
                max_z=-5,
            ),
            Instruction(
                state=True, min_x=-18, max_x=26, min_y=-33, max_y=15, min_z=-7, max_z=46
            ),
            Instruction(
                state=False,
                min_x=-40,
                max_x=-22,
                min_y=-38,
                max_y=-28,
                min_z=23,
                max_z=41,
            ),
            Instruction(
                state=True, min_x=-16, max_x=35, min_y=-41, max_y=10, min_z=-47, max_z=6
            ),
            Instruction(
                state=False,
                min_x=-32,
                max_x=-23,
                min_y=11,
                max_y=30,
                min_z=-14,
                max_z=3,
            ),
            Instruction(
                state=True, min_x=-49, max_x=-5, min_y=-3, max_y=45, min_z=-29, max_z=18
            ),
            Instruction(
                state=False, min_x=18, max_x=30, min_y=-20, max_y=-8, min_z=-3, max_z=13
            ),
            Instruction(
                state=True, min_x=-41, max_x=9, min_y=-7, max_y=43, min_z=-33, max_z=15
            ),
        ],
        590784,
    ),
    (
        [
            Instruction(
                state=True, min_x=-5, max_x=47, min_y=-31, max_y=22, min_z=-19, max_z=33
            ),
            Instruction(
                state=True, min_x=-44, max_x=5, min_y=-27, max_y=21, min_z=-14, max_z=35
            ),
            Instruction(
                state=True,
                min_x=-49,
                max_x=-1,
                min_y=-11,
                max_y=42,
                min_z=-10,
                max_z=38,
            ),
            Instruction(
                state=True, min_x=-20, max_x=34, min_y=-40, max_y=6, min_z=-44, max_z=1
            ),
            Instruction(
                state=False, min_x=26, max_x=39, min_y=40, max_y=50, min_z=-2, max_z=11
            ),
            Instruction(
                state=True, min_x=-41, max_x=5, min_y=-41, max_y=6, min_z=-36, max_z=8
            ),
            Instruction(
                state=False,
                min_x=-43,
                max_x=-33,
                min_y=-45,
                max_y=-28,
                min_z=7,
                max_z=25,
            ),
            Instruction(
                state=True,
                min_x=-33,
                max_x=15,
                min_y=-32,
                max_y=19,
                min_z=-34,
                max_z=11,
            ),
            Instruction(
                state=False,
                min_x=35,
                max_x=47,
                min_y=-46,
                max_y=-34,
                min_z=-11,
                max_z=5,
            ),
            Instruction(
                state=True, min_x=-14, max_x=36, min_y=-6, max_y=44, min_z=-16, max_z=29
            ),
            Instruction(
                state=True,
                min_x=-57795,
                max_x=-6158,
                min_y=29564,
                max_y=72030,
                min_z=20435,
                max_z=90618,
            ),
            Instruction(
                state=True,
                min_x=36731,
                max_x=105352,
                min_y=-21140,
                max_y=28532,
                min_z=16094,
                max_z=90401,
            ),
            Instruction(
                state=True,
                min_x=30999,
                max_x=107136,
                min_y=-53464,
                max_y=15513,
                min_z=8553,
                max_z=71215,
            ),
            Instruction(
                state=True,
                min_x=13528,
                max_x=83982,
                min_y=-99403,
                max_y=-27377,
                min_z=-24141,
                max_z=23996,
            ),
            Instruction(
                state=True,
                min_x=-72682,
                max_x=-12347,
                min_y=18159,
                max_y=111354,
                min_z=7391,
                max_z=80950,
            ),
            Instruction(
                state=True,
                min_x=-1060,
                max_x=80757,
                min_y=-65301,
                max_y=-20884,
                min_z=-103788,
                max_z=-16709,
            ),
            Instruction(
                state=True,
                min_x=-83015,
                max_x=-9461,
                min_y=-72160,
                max_y=-8347,
                min_z=-81239,
                max_z=-26856,
            ),
            Instruction(
                state=True,
                min_x=-52752,
                max_x=22273,
                min_y=-49450,
                max_y=9096,
                min_z=54442,
                max_z=119054,
            ),
            Instruction(
                state=True,
                min_x=-29982,
                max_x=40483,
                min_y=-108474,
                max_y=-28371,
                min_z=-24328,
                max_z=38471,
            ),
            Instruction(
                state=True,
                min_x=-4958,
                max_x=62750,
                min_y=40422,
                max_y=118853,
                min_z=-7672,
                max_z=65583,
            ),
            Instruction(
                state=True,
                min_x=55694,
                max_x=108686,
                min_y=-43367,
                max_y=46958,
                min_z=-26781,
                max_z=48729,
            ),
            Instruction(
                state=True,
                min_x=-98497,
                max_x=-18186,
                min_y=-63569,
                max_y=3412,
                min_z=1232,
                max_z=88485,
            ),
            Instruction(
                state=True,
                min_x=-726,
                max_x=56291,
                min_y=-62629,
                max_y=13224,
                min_z=18033,
                max_z=85226,
            ),
            Instruction(
                state=True,
                min_x=-110886,
                max_x=-34664,
                min_y=-81338,
                max_y=-8658,
                min_z=8914,
                max_z=63723,
            ),
            Instruction(
                state=True,
                min_x=-55829,
                max_x=24974,
                min_y=-16897,
                max_y=54165,
                min_z=-121762,
                max_z=-28058,
            ),
            Instruction(
                state=True,
                min_x=-65152,
                max_x=-11147,
                min_y=22489,
                max_y=91432,
                min_z=-58782,
                max_z=1780,
            ),
            Instruction(
                state=True,
                min_x=-120100,
                max_x=-32970,
                min_y=-46592,
                max_y=27473,
                min_z=-11695,
                max_z=61039,
            ),
            Instruction(
                state=True,
                min_x=-18631,
                max_x=37533,
                min_y=-124565,
                max_y=-50804,
                min_z=-35667,
                max_z=28308,
            ),
            Instruction(
                state=True,
                min_x=-57817,
                max_x=18248,
                min_y=49321,
                max_y=117703,
                min_z=5745,
                max_z=55881,
            ),
            Instruction(
                state=True,
                min_x=14781,
                max_x=98692,
                min_y=-1341,
                max_y=70827,
                min_z=15753,
                max_z=70151,
            ),
            Instruction(
                state=True,
                min_x=-34419,
                max_x=55919,
                min_y=-19626,
                max_y=40991,
                min_z=39015,
                max_z=114138,
            ),
            Instruction(
                state=True,
                min_x=-60785,
                max_x=11593,
                min_y=-56135,
                max_y=2999,
                min_z=-95368,
                max_z=-26915,
            ),
            Instruction(
                state=True,
                min_x=-32178,
                max_x=58085,
                min_y=17647,
                max_y=101866,
                min_z=-91405,
                max_z=-8878,
            ),
            Instruction(
                state=True,
                min_x=-53655,
                max_x=12091,
                min_y=50097,
                max_y=105568,
                min_z=-75335,
                max_z=-4862,
            ),
            Instruction(
                state=True,
                min_x=-111166,
                max_x=-40997,
                min_y=-71714,
                max_y=2688,
                min_z=5609,
                max_z=50954,
            ),
            Instruction(
                state=True,
                min_x=-16602,
                max_x=70118,
                min_y=-98693,
                max_y=-44401,
                min_z=5197,
                max_z=76897,
            ),
            Instruction(
                state=True,
                min_x=16383,
                max_x=101554,
                min_y=4615,
                max_y=83635,
                min_z=-44907,
                max_z=18747,
            ),
            Instruction(
                state=False,
                min_x=-95822,
                max_x=-15171,
                min_y=-19987,
                max_y=48940,
                min_z=10804,
                max_z=104439,
            ),
            Instruction(
                state=True,
                min_x=-89813,
                max_x=-14614,
                min_y=16069,
                max_y=88491,
                min_z=-3297,
                max_z=45228,
            ),
            Instruction(
                state=True,
                min_x=41075,
                max_x=99376,
                min_y=-20427,
                max_y=49978,
                min_z=-52012,
                max_z=13762,
            ),
            Instruction(
                state=True,
                min_x=-21330,
                max_x=50085,
                min_y=-17944,
                max_y=62733,
                min_z=-112280,
                max_z=-30197,
            ),
            Instruction(
                state=True,
                min_x=-16478,
                max_x=35915,
                min_y=36008,
                max_y=118594,
                min_z=-7885,
                max_z=47086,
            ),
            Instruction(
                state=False,
                min_x=-98156,
                max_x=-27851,
                min_y=-49952,
                max_y=43171,
                min_z=-99005,
                max_z=-8456,
            ),
            Instruction(
                state=False,
                min_x=2032,
                max_x=69770,
                min_y=-71013,
                max_y=4824,
                min_z=7471,
                max_z=94418,
            ),
            Instruction(
                state=True,
                min_x=43670,
                max_x=120875,
                min_y=-42068,
                max_y=12382,
                min_z=-24787,
                max_z=38892,
            ),
            Instruction(
                state=False,
                min_x=37514,
                max_x=111226,
                min_y=-45862,
                max_y=25743,
                min_z=-16714,
                max_z=54663,
            ),
            Instruction(
                state=False,
                min_x=25699,
                max_x=97951,
                min_y=-30668,
                max_y=59918,
                min_z=-15349,
                max_z=69697,
            ),
            Instruction(
                state=False,
                min_x=-44271,
                max_x=17935,
                min_y=-9516,
                max_y=60759,
                min_z=49131,
                max_z=112598,
            ),
            Instruction(
                state=True,
                min_x=-61695,
                max_x=-5813,
                min_y=40978,
                max_y=94975,
                min_z=8655,
                max_z=80240,
            ),
            Instruction(
                state=False,
                min_x=-101086,
                max_x=-9439,
                min_y=-7088,
                max_y=67543,
                min_z=33935,
                max_z=83858,
            ),
            Instruction(
                state=False,
                min_x=18020,
                max_x=114017,
                min_y=-48931,
                max_y=32606,
                min_z=21474,
                max_z=89843,
            ),
            Instruction(
                state=False,
                min_x=-77139,
                max_x=10506,
                min_y=-89994,
                max_y=-18797,
                min_z=-80,
                max_z=59318,
            ),
            Instruction(
                state=False,
                min_x=8476,
                max_x=79288,
                min_y=-75520,
                max_y=11602,
                min_z=-96624,
                max_z=-24783,
            ),
            Instruction(
                state=True,
                min_x=-47488,
                max_x=-1262,
                min_y=24338,
                max_y=100707,
                min_z=16292,
                max_z=72967,
            ),
            Instruction(
                state=False,
                min_x=-84341,
                max_x=13987,
                min_y=2429,
                max_y=92914,
                min_z=-90671,
                max_z=-1318,
            ),
            Instruction(
                state=False,
                min_x=-37810,
                max_x=49457,
                min_y=-71013,
                max_y=-7894,
                min_z=-105357,
                max_z=-13188,
            ),
            Instruction(
                state=False,
                min_x=-27365,
                max_x=46395,
                min_y=31009,
                max_y=98017,
                min_z=15428,
                max_z=76570,
            ),
            Instruction(
                state=False,
                min_x=-70369,
                max_x=-16548,
                min_y=22648,
                max_y=78696,
                min_z=-1892,
                max_z=86821,
            ),
            Instruction(
                state=True,
                min_x=-53470,
                max_x=21291,
                min_y=-120233,
                max_y=-33476,
                min_z=-44150,
                max_z=38147,
            ),
            Instruction(
                state=False,
                min_x=-93533,
                max_x=-4276,
                min_y=-16170,
                max_y=68771,
                min_z=-104985,
                max_z=-24507,
            ),
        ],
        2758514936282235,
    ),
]


@pytest.mark.parametrize("instructions,expected_cubes_lit", TASK_2_SAMPLES)
def test_task_2(
    instructions: List[Instruction], expected_cubes_lit: int, caplog: Any
) -> None:
    caplog.set_level(logging.DEBUG)
    reactor = get_reactor(instructions)
    apply_instructions(instructions, reactor)
    if expected_cubes_lit == 34:
        breakpoint()
    actual = reactor.sum()
    assert actual == expected_cubes_lit
