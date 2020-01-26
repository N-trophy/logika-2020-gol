from typing import Tuple

from gol.models import Task
from gol.common import Grid, Reporter
from .common import Ok, Score, Rules, eval_same_func, compares_count


def _eval_gol_min(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
                  user_reporter: Reporter) -> Tuple[Ok, Score]:
    ok, _ = eval_same_func(task, rules, grid, int_reporter, user_reporter)
    if ok:
        user_reporter('[OK] Vámi zadaná pravidla jsou pravidla Game of Life.')
        return (ok, compares_count(rules))
    else:
        user_reporter('[ERR] Vámi zadaná pravidla nejsou pravidla '
                      'Game of Life!')
        return (False, 0)


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
