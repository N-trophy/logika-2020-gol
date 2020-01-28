from typing import Tuple
import pyparsing

from gol.models import Task
from gol.common import Grid, Reporter
from gol.rules_parser import parse
from .common import Ok, Score, Rules, eval_same_func, compares_count, tick


GUESS_ONE_GRIDS = [
    Grid.fromstr("""
        xx
        xx
    """),
    Grid.fromstr("""
        xx
        xx
    """),
]


def eval_guess_rules_one(
        task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
        user_reporter: Reporter) -> Tuple[Ok, Score]:
    teacher_rules = parse(task.rules, task.allowed_colors)

    try:
        participant_rules = parse(rules, task.allowed_colors)
    except pyparsing.ParseException as e:
        user_reporter(f'[ERR] Napodařilo se načíst pravidla: {str(e)}')
        return (False, 0)

    for testgrid in GUESS_ONE_GRIDS:
        student_grid = tick(testgrid, participant_rules, task.global_config())
        teacher_grid = tick(testgrid, teacher_rules, task.global_config())

        if student_grid != teacher_grid:
            user_reporter('[ERR] Vámi zadaná pravidla se nechovají stejně'
                          ' na některé ze zadaných mřížek!')
            int_reporter(f'[ERR] Selhalo na mřížce: {grid}')
            return (False, 0)

    user_reporter('[OK] Vámi zadaná pravidla se chovají korektně.')

    compares = compares_count(rules)
    user_reporter(f'[INFO] Vámi zadaná pravidla obsahují {compares} '
                  'porovnání.')
    return (True, compares)


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
