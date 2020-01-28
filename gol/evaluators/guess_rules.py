from typing import Tuple, List
import pyparsing

from gol.models import Task
from gol.common import Grid, Reporter
from gol.rules_parser import parse
from .common import Ok, Score, Rules, eval_same_func, compares_count, tick


GUESS_ONE_GRIDS = [
    Grid.fromstr("""
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkgggggggggggkkkkkkk
        kkkkkkgkkkkkkkkkkkgkkkkkk
        kkkkkgkkkkkkkkkkkkkgkkkkk
        kkkkgkkgggkkkkkgggkkgkkkk
        kkkkgkkkkkkkkkkkkkkkgkkkk
        kkkkgkkkgggkkkgggkkkgkkkk
        kkkkgkkkgkgkkkgkgkkkgkkkk
        kkkkgkkkgggkkkgggkkkgkkkk
        kkkkgkkkkkkkkkkkkkkkgkkkk
        kkkkgkkkkkkkkkkkkkkkgkkkk
        kkkkgkkkkkkgggkkkkkkgkkkk
        kkkkgkkkkkkkgkkkkkkkgkkkk
        kkkkgkgkkkkkkkkkkkgkgkkkk
        kkkkgkkgkkkkkkkkkgkkgkkkk
        kkkkkgkkgggggggggkkgkkkkk
        kkkkkkgkkkgkkkgkkkgkkkkkk
        kkkkkkkgkkkgggkkkgkkkkkkk
        kkkkkkkkgkkkkkkkgkkkkkkkk
        kkkkkkkkkgggggggkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
    """),
]


GUESS_TWO_GRIDS = [
    Grid.fromstr("""
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkgggggkkkkkkkkkk
        kkkkkkkkkkgggggkkkkkkkkkk
        kkkkkkkkkkgggggkkkkkkkkkk
        kkkkkkkkkkgggggkkkkkkkkkk
        kkkkkkkkkkgggggkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
    """),
    Grid.fromstr("""
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkgkkkkkkkkkkkk
        kkkkkkkkkkkkkgkkkkkkkkkkk
        kkkkkkkkkkgggggkkkkkkkkkk
        kkkkkkkkkkkkkgkkkkkkkkkkk
        kkkkkkkkkkkkgkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
    """),
    Grid.fromstr("""
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkgkkkgkkkkkkkkkk
        kkkkkkkkkkkgkgkkkkkkkkkkk
        kkkkkkkkkkkkgkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
        kkkkkkkkkkkkkkkkkkkkkkkkk
    """),
]


def _eval_guess(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
                user_reporter: Reporter, grids: List[Grid],
                no_steps: int) -> Tuple[Ok, Score]:
    teacher_rules = parse(task.rules, task.allowed_colors)

    try:
        participant_rules = parse(rules, task.allowed_colors)
    except pyparsing.ParseException as e:
        user_reporter(f'[ERR] Napodařilo se načíst pravidla: {str(e)}')
        return (False, 0)

    for testgrid in grids:
        student_grid = teacher_grid = testgrid
        for _ in range(no_steps):
            student_grid = tick(testgrid, participant_rules,
                                task.global_config())
            teacher_grid = tick(testgrid, teacher_rules,
                                task.global_config())

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


def eval_guess_rules_one(
        task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
        user_reporter: Reporter) -> Tuple[Ok, Score]:
    return _eval_guess(task, rules, grid, int_reporter, user_reporter,
                       GUESS_ONE_GRIDS, 1)


def eval_guess_rules_two(
        task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
        user_reporter: Reporter) -> Tuple[Ok, Score]:
    return _eval_guess(task, rules, grid, int_reporter, user_reporter,
                       GUESS_TWO_GRIDS, 2)
