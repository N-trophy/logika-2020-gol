from typing import Callable, Tuple, Dict, Any, Union
import copy
import itertools

from gol.models import Task
from gol.common import Grid, Reporter, Color, Point2D, grid_colors_valid
from gol.rules_parser import Rule

Ok = bool
Score = float
Rules = str
Evaluator = Callable[[Task, Rules, Grid, Reporter, Reporter],
                     Tuple[Ok, Score]]


def eval_empty(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
               user_reporter: Reporter) -> Tuple[Ok, Score]:
    return (True, 1)


def tick_pos(grid: Grid, new_grid: Grid, rule: Union[Rule, Color],
             pos: Point2D, global_config: Dict[str, Any]) -> None:
    x, y = pos
    if isinstance(rule, str):
        new_grid[y][x] = rule
    else:
        new_grid[y][x] = rule(grid, pos, global_config)


def tick(grid: Grid, rule: Union[Rule, Color],
         global_config: Dict[str, Any]) -> Grid:
    new_grid = copy.deepcopy(grid)
    for y in range(grid.height):
        for x in range(grid.width):
            tick_pos(grid, new_grid, rule, (x, y), global_config)
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


def all_neighbors(colors: str):
    return [
        Grid.fromlist(neigh, 3)
        for neigh in itertools.product(colors, repeat=9)
    ]


def validate_grid_colors(func):
    def wrapper(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
                user_reporter: Reporter) -> Tuple[Ok, Score]:
        if not grid_colors_valid(grid, task.allowed_colors):
            user_reporter('[ERR] Použili jste nepovolenou barvu!')
            return (False, 0)
        return func(task, rules, grid, int_reporter, user_reporter)
    return wrapper


def validate_grid_size(func):
    def wrapper(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
                user_reporter: Reporter) -> Tuple[Ok, Score]:
        if grid.width != task.klikatko_width or grid.height != task.klikatko_height:
            user_reporter('[ERR] Mřížka nemá správné rozměry!')
            return (False, 0)
        return func(task, rules, grid, int_reporter, user_reporter)
    return wrapper
