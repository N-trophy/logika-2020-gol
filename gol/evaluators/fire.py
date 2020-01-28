from typing import Tuple

from gol.models import Task
from gol.common import Grid, Reporter
from gol.rules_parser import parse
from .common import Ok, Score, Rules, tick, validate_grid_colors, \
                    validate_grid_size

ITER_LIMIT = 50


@validate_grid_colors
@validate_grid_size
def eval_fire(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
              user_reporter: Reporter) -> Tuple[Ok, Score]:
    rules = parse(task.rules, task.allowed_colors)
    author_grid = Grid.fromstr(task.start_config)

    red_present = False
    for y in range(grid.height):
        for x in range(grid.width):
            if author_grid[y][x] == 'k' and grid[y][x] != 'k':
                user_reporter(f'[ERR] Šedým polím nelze měnit barvu!')
                return (False, 0)
            if author_grid[y][x] == 'g' and grid[y][x] == 'k':
                user_reporter(f'[ERR] Zelená pole nelze přebarvovat na šedo!')
                return (False, 0)
            if author_grid[y][x] == 'b' and grid[y][x] != 'b':
                user_reporter(f'[ERR] Modrá pole nelze přebarvovat!')
                return (False, 0)
            if grid[y][x] == 'r':
                if author_grid[y][x] != 'g':
                    user_reporter('[ERR] Na červeno lze přebarvit jen zelené '
                                  'buňky!')
                    return (False, 0)
                if red_present:
                    user_reporter('[ERR] Nejvýše jedna buňka může být '
                                  'červená!')
                    return (False, 0)
                red_present = True

    user_reporter('[OK] Vaše konfigurace splňuje vstupní podmínky.')

    i = 0
    grid_start = grid
    grid = tick(grid_start, rules, task.global_config())
    while grid_start != grid and i < ITER_LIMIT:
        grid_start = grid
        grid = tick(grid_start, rules, task.global_config())
        i += 1

    grid = tick(grid_start, rules, task.global_config())
    if grid != grid_start:
        user_reporter(f'[ERR] Plán nedosáhl stabilního stavu v {ITER_LIMIT} '
                      'krocích!')
        return (False, 0)
    user_reporter(f'[OK] Plán dosáhl stabilního stavu po {i} krocích.')

    k_count = 0
    for y in range(grid.height):
        for x in range(grid.width):
            if grid[y][x] not in 'rk':
                user_reporter(f'[ERR] Ve stabilním stavu nejsou všechny buňky'
                              ' červené nebo šedé!')
                return (False, 0)
            if grid[y][x] == 'k':
                k_count += 1
    k_count -= 44

    user_reporter('[OK] Počet šedých buňek ve stabilním stavu bez buňek na '
                  f'okraji: {k_count}.')
    return (True, k_count)
