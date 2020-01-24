from typing import Callable

from gol.models import Task
from gol.common import Grid, grid_colors_valid

Stepper = Callable[[Task, Grid], Grid]


def step_empty(task: Task, grid: Grid) -> Grid:
    return grid


def validate_grid_colors(func):
    def wrapper(task: Task, grid: Grid) -> Grid:
        if not grid_colors_valid(grid, task.allowed_colors):
            raise Exception('Invalid colors in grid!')
        return func(task, grid)
    return wrapper


def validate_grid_size(func):
    def wrapper(task: Task, grid: Grid) -> Grid:
        if grid.width != task.klikatko_width or grid.height != task.klikatko_height:
            raise Exception('Invalid grid size!')
        return func(task, grid)
    return wrapper
