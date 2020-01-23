from typing import Callable, Tuple

from gol.models import Task
from gol.common import Grid, Reporter

Ok = bool
Points = float
Rules = str
Evaluator = Callable[[Task, Rules, Grid, Reporter, Reporter],
                     Tuple[Ok, Points]]


def eval_empty(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
               user_reporter: Reporter) -> Tuple[Ok, Points]:
    return (True, 1)
