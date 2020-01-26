from typing import Tuple
import pyparsing

from gol.models import Task
from gol.common import Grid, Reporter
from gol.rules_parser import parse
import gol.rules_parser.comparison
from .common import Ok, Score, Rules, tick_pos, all_neighbors


def _eval_gol_min(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
                  user_reporter: Reporter) -> Tuple[Ok, Score]:
    author_rules = parse(task.rules, task.allowed_colors)

    try:
        participant_rules = parse(rules, task.allowed_colors)
    except pyparsing.ParseException as e:
        user_reporter(f'[ERR] Napodařilo se načíst pravidla: {str(e)}')
        return (False, 0)

    out_grida = Grid.fromfill(3, 3)
    out_gridb = Grid.fromfill(3, 3)
    for grid in all_neighbors(task.allowed_colors):
        tick_pos(grid, out_grida, participant_rules, (1, 1),
                 task.global_config())
        tick_pos(grid, out_gridb, author_rules, (1, 1), task.global_config())

        if out_grida[1][1] != out_gridb[1][1]:
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
                 user_reporter: Reporter) -> Tuple[Ok, Score]:
    ok, compares = _eval_gol_min(
        task, rules, grid, int_reporter, user_reporter
    )
    if ok:
        user_reporter(f'[INFO] Vámi zadaná pravidla obsahují {compares} '
                      'porovnání.')
    return ok, compares


def eval_gol(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
             user_reporter: Reporter) -> Tuple[Ok, Score]:
    return _eval_gol_min(task, rules, grid, int_reporter, user_reporter)
