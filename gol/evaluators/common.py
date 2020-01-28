from typing import Callable, Tuple, Dict, Any, Union
import copy
import itertools
import pyparsing

from gol.models import Task
from gol.common import Grid, Reporter, Color, Point2D, grid_colors_valid
from gol.rules_parser import Rule, parse
import gol.rules_parser.comparison

Ok = bool
Score = float
Rules = str
Evaluator = Callable[[Task, Rules, Grid, Reporter, Reporter],
                     Tuple[Ok, Score]]


def eval_empty(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
               user_reporter: Reporter) -> Tuple[Ok, Score]:
    return (True, 1)


def eval_same_func(task: Task, rules: Rules, grid: Grid,
                   int_reporter: Reporter,
                   user_reporter: Reporter) -> Tuple[Ok, Score]:
    author_rules = parse(task.rules, task.allowed_colors)

    try:
        participant_rules = parse(rules, task.allowed_colors)
    except pyparsing.ParseException as e:
        user_reporter(f'[ERR] Napodařilo se načíst pravidla: {str(e)}')
        return (False, 0)

    out_grida = Grid.fromfill(3, 3)
    out_gridb = Grid.fromfill(3, 3)
    for grid in all_neighbors(task.allowed_colors):
        tick_pos(grid, out_grida, participant_rules, (1, 1),
                 task.global_config())
        tick_pos(grid, out_gridb, author_rules, (1, 1), task.global_config())

        if out_grida[1][1] != out_gridb[1][1]:
            int_reporter(f'[ERR] Selhalo na mřížce: {grid}')
            return (False, 0)

    return (True, 0)


def compares_count(rules: Rules) -> int:
    comparisons_cnt = sum([
        rules.count(comparator)
        for comparator in gol.rules_parser.comparison.COMPARES.keys()
    ])

    return comparisons_cnt


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
        if (grid.width != task.klikatko_width or
                grid.height != task.klikatko_height):
            user_reporter('[ERR] Mřížka nemá správné rozměry!')
            return (False, 0)
        return func(task, rules, grid, int_reporter, user_reporter)
    return wrapper


def _is_arithmetic_operator(rule: Union[Rule, Color]):
    if isinstance(rule, Color):
        return False
    return 'SelectorOperator' in repr(rule)


def no_arithmetic_operators(func):
    def wrapper(task: Task, rules: Rules, grid: Grid, int_reporter: Reporter,
                user_reporter: Reporter) -> Tuple[Ok, Score]:
        try:
            rules_ = parse(rules, task.allowed_colors)
        except pyparsing.ParseException as e:
            user_reporter(f'[ERR] Napodařilo se načíst pravidla: {str(e)}')
            return (False, 0)

        if _is_arithmetic_operator(rules_):
            user_reporter('[ERR] Pravidla obsahují aritmetické operátory!')
            return (False, 0)
        return func(task, rules, grid, int_reporter, user_reporter)
    return wrapper
