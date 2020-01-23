from typing import Callable

from gol.models import Task
from gol.common import Grid

Stepper = Callable[[Task, Grid], Grid]


def step_empty(task: Task, grid: Grid) -> Grid:
    return grid
