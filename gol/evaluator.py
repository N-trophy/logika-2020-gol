from typing import List, Tuple, Any, Dict
import operator

Grid = List[List[str]]
Point2D = Tuple[int, int]  # x, y


NEIGHBOURHOOD = {  # x, y
    0: (-1, -1),
    1: (0, -1),
    2: (1, -1),
    3: (-1, 0),
    4: (0, 0),
    5: (1, 0),
    6: (-1, 1),
    7: (0, 1),
    8: (1, 1),
}


def points_add(a: Point2D, b: Point2D) -> Point2D:
    return (a[0]+b[0], a[1]+b[1])


def point_in_grid(p: Point2D, grid: Grid) -> bool:
    return p[0] >= 0 and p[1] >= 0 and p[0] < len(grid[0]) and p[1] < len(grid)


def selector_eval(selector: str, grid: Grid, pos: Point2D,
                  global_config: Dict[str, Any]) -> int:
    assert len(selector) == 9

    count = 0
    for i, colour in enumerate(selector):
        x, y = points_add(NEIGHBOURHOOD[i], pos)
        if point_in_grid((x, y), grid):
            if colour == '*' or grid[y][x] == colour:
                count += 1
    return count


def _eval(operand, *args, **kwargs):
    if isinstance(operand, int):
        return operand
    return operand(*args, **kwargs)


def selector_op_eval(selector_op, grid: Grid, pos: Point2D,
                     global_config: Dict[str, Any]) -> int:
    result = _eval(selector_op.operands[0], grid, pos, global_config)
    for operand in selector_op.operands[1:]:
        result = selector_op.operator(
            result,
            _eval(operand, grid, pos, global_config)
        )
    return result


def comparison_eval(comparison, grid: Grid, pos: Point2D,
                    global_config: Dict[str, Any]) -> bool:
    left = _eval(comparison.left, grid, pos, global_config)
    right = _eval(comparison.right, grid, pos, global_config)
    return comparison.operator(left, right)


def bool_op_eval(bool_op, grid: Grid, pos: Point2D,
                 global_config: Dict[str, Any]) -> bool:
    if bool_op.operator == operator.and_:
        for operand in bool_op.operands:
            if not bool_op.operands[0](grid, pos, global_config):
                return False
        return True
    elif bool_op.operator == operator.or_:
        for operand in bool_op.operands:
            if bool_op.operands[0](grid, pos, global_config):
                return True
        return False

    assert False, 'Invalid operator in evaluation!'


def rule_eval(rule, grid: Grid, pos: Point2D,
              global_config: Dict[str, Any]) -> bool:
    if isinstance(rule, str):
        return rule
    if rule.bool_expr(grid, pos, global_config):
        return rule_eval(rule.if_rule, grid, pos, global_config)
    return rule_eval(rule.else_rule, grid, pos, global_config)
