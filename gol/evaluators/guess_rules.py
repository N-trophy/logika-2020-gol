from typing import Tuple

from gol.models import Task
from gol.common import Grid, Reporter
from .common import Ok, Score, Rules, eval_same_func, compares_count


def eval_guess_rules_two(
        task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
        user_reporter: Reporter) -> Tuple[Ok, Score]:
    ok, _ = eval_same_func(task, rules, grid, int_reporter, user_reporter)

    if not ok:
        user_reporter('[ERR] Vámi zadaná pravidla nejsou správná!')
        return (False, 0)

    user_reporter('[OK] Vámi zadaná pravidla se chovají korektně.')

    compares = compares_count(rules)
    user_reporter(f'[INFO] Vámi zadaná pravidla obsahují {compares} '
                  'porovnání.')
    return (ok, compares)
