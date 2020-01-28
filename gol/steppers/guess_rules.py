from typing import Callable

from gol.models import Task
from gol.common import Grid, grid_colors_valid
from .common import validate_grid_colors, validate_grid_size
from gol.evaluators.common import tick
from gol.rules_parser import parse


@validate_grid_colors
@validate_grid_size
def step_guess_rules_one(task: Task, grid: Grid) -> Grid:
    author_rules = parse(task.rules, task.allowed_colors)
    grid = tick(grid, author_rules, task.global_config())
    return grid


@validate_grid_colors
@validate_grid_size
def step_guess_rules_two(task: Task, grid: Grid) -> Grid:
    author_rules = parse(task.rules, task.allowed_colors)
    grid = tick(grid, author_rules, task.global_config())
    grid = tick(grid, author_rules, task.global_config())
    return grid
