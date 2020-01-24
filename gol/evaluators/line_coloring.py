from typing import Tuple

from gol.models import Task
from gol.common import Grid, Reporter
from gol.rules_parser import parse
from .common import Ok, Score, Rules, tick


def _red_top_count(grid: Grid):
    return grid[0].count('r')


def eval_line_coloring(task: Task, rules: Rules, grid: Grid,
                       int_reporter: Reporter,
                       user_reporter: Reporter) -> Tuple[Ok, Score]:
    rules = parse(task.rules)
    grid = Grid.fromstr(grid)

    for y in range(grid.height-1):
        for x in range(grid.width):
            if grid[y][x] != 'b':
                user_reporter('[ERR] Obarvili jste víc, než jen spodní řádek!')
                return (False, 0)

    for i in range(11):
        grid = tick(grid, rules, task.global_config())
        int_reporter(f'[OK] Po {i+1}. iteraci v horním řádku '
                     f'{_red_top_count(grid)} červených buňek.')

    score = _red_top_count(grid)
    user_reporter(f'[OK] Počet červených buňek v horním řádku po 11. iteraci:'
                  f' {score}.')
    return (True, score)
