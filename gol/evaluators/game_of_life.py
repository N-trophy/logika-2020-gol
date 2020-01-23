from typing import Tuple

from gol.models import Task
from gol.common import Grid, Reporter, recolor_grid, random_grid
from gol.rules_parser import parse
import gol.rules_parser.comparison
from .common import Ok, Points, Rules, test_rules_eq

TESTGRIDS = [
    Grid.fromstr("""
        -X-
        -X-
        -X-
    """),
    Grid.fromstr("""
        ---
        XXX
        ---
    """),
    Grid.fromstr("""
        -X-
        XXX
        -X-
    """),
    Grid.fromstr("""
        -XX--------X---
        -XX-------X-X--
        -----------X---
        ---------------
        ----X-----X----
        ---X-X----X----
        ----XX----X----
        ---------------
        ---------------
    """),
]

RECOLOR_MAP = {
    '-': 'k',
    'X': 'g',
}


def _eval_gol_min(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
                  user_reporter: Reporter) -> Tuple[Ok, Points]:
    author_rules = parse(task.rules)
    participant_rules = parse(rules)
    random_grids = [random_grid('k', 'g') for _ in range(5)]
    for grid in TESTGRIDS+random_grids:
        proper_colored = recolor_grid(grid, RECOLOR_MAP)
        if not test_rules_eq(proper_colored, participant_rules,
                             author_rules, {}):
            int_reporter(f'[ERR] Selhalo na mřížce: {grid}')
            user_reporter('[ERR] Vámi zadaná pravidla nejsou pravidla '
                          'Game of Life!')
            return (False, 0)

    user_reporter('[OK] Vámi zadaná pravidla jsou pravidla Game of Life.')

    comparisons_cnt = sum([
        rules.count(comparator)
        for comparator in gol.rules_parser.comparison.COMPARES.keys()
    ])

    return (True, comparisons_cnt)


def eval_gol_min(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
                 user_reporter: Reporter) -> Tuple[Ok, Points]:
    ok, compares = _eval_gol_min(
        task, rules, grid, int_reporter, user_reporter
    )
    if ok:
        user_reporter(f'[INFO] Vámi zadaná pravidla obsahují {compares} '
                      'porovnání.')
    return ok, compares


def eval_gol(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
             user_reporter: Reporter) -> Tuple[Ok, Points]:
    return _eval_gol_min(task, rules, grid, int_reporter, user_reporter)
