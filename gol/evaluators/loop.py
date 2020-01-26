from typing import Tuple

from gol.models import Task
from gol.common import Grid, Reporter
from gol.rules_parser import parse
from .common import Ok, Score, Rules, tick, validate_grid_colors, \
                    validate_grid_size


@validate_grid_colors
@validate_grid_size
def eval_loop(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
              user_reporter: Reporter) -> Tuple[Ok, Score]:
    rules = parse(task.rules, task.allowed_colors)

    grid2 = tick(grid, rules, task.global_config())
    if grid2 == grid:
        user_reporter('[ERR] Konfigurace ve 2. iteraci je stejná jako '
                      'počáteční konfigurace!')
        return (False, 0)

    grid3 = tick(grid2, rules, task.global_config())
    if grid3 == grid2:
        user_reporter('[ERR] Konfigurace ve 3. iteraci je stejná jako '
                      'konfigurace ve 2. iteraci!')
        return (False, 0)

    if grid3 != grid:
        user_reporter('[ERR] Konfigurace ve 3. iteraci není stejná jako '
                      'počáteční konfigurace!')
        return (False, 0)

    user_reporter('[OK] Úloha úspěšně vyřešena.')
    return (True, 0)
