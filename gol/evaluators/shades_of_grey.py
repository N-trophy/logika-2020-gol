from typing import Tuple
import copy

from gol.models import Task
from gol.common import Grid, Reporter
from gol.rules_parser import parse
from .common import Ok, Score, Rules, tick, validate_grid_colors, \
                    validate_grid_size

ITER_LIMIT = 50


def _red_count(grid: Grid) -> int:
    return sum([grid[y].count('r') for y in range(grid.height)])


def _all_grey(grid: Grid) -> bool:
    for y in range(grid.height):
        if grid[y].count('k') != grid.width:
            return False
    return True


@validate_grid_colors
@validate_grid_size
def eval_shades_of_grey(task: Task, rules: Rules, grid: Grid,
                        int_reporter: Reporter,
                        user_reporter: Reporter) -> Tuple[Ok, Score]:
    rules = parse(task.rules, task.allowed_colors)

    if _all_grey(grid):
        user_reporter('[ERR] Počáteční konfigurace nebosahuje červenou buňku!')
        return (False, 0)

    grid_start = copy.deepcopy(grid)
    i = 0
    while not _all_grey(grid) and i < ITER_LIMIT:
        grid = tick(grid, rules, task.global_config())
        i += 1

    if i == ITER_LIMIT:
        user_reporter('[ERR] Automat se nezastavil ani po '
                      f'{ITER_LIMIT} krocích!')
        return (False, 0)

    user_reporter(f'[OK] Skončilo po {i} iteracích.')
    score = _red_count(grid_start)
    user_reporter(f'[OK] Počet červených buňek na začátku: {score}.')
    return (True, score)
