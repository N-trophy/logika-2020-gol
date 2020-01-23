from typing import Callable, Tuple, Dict, Any, Union
import copy

from gol.models import Task
from gol.common import Grid, Reporter, Color
from gol.rules_parser import Rule

Ok = bool
Points = float
Rules = str
Evaluator = Callable[[Task, Rules, Grid, Reporter, Reporter],
                     Tuple[Ok, Points]]


def eval_empty(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
               user_reporter: Reporter) -> Tuple[Ok, Points]:
    return (True, 1)


def tick(grid: Grid, rule: Union[Rule, Color],
         global_config: Dict[str, Any]) -> Grid:
    new_grid = copy.deepcopy(grid)
    for y in range(grid.height):
        for x in range(grid.width):
            if isinstance(rule, str):
                new_grid[y][x] = rule
            else:
                new_grid[y][x] = rule(grid, (x, y), global_config)
    return new_grid


def test_rules_eq(grid: Grid, rulea: Rule, ruleb: Rule,
                  global_config: Dict[str, Any],
                  no_iterations: int = 10) -> bool:
    grida = copy.deepcopy(grid)
    gridb = copy.deepcopy(grid)
    for _ in range(no_iterations):
        grida = tick(grida, rulea, global_config)
        gridb = tick(gridb, ruleb, global_config)
        if grida != gridb:
            return False
    return True
