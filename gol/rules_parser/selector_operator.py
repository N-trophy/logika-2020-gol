import operator
from typing import Dict, Callable, Union, Any, List

from gol.common import Grid, Point2D
from gol.rules_parser.selector import Selector, selector_or_number_webrepr


BinaryIntOperator = Callable[[int, int], bool]


NUMERIC_OPERATORS: Dict[str, BinaryIntOperator] = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
    '%': operator.mod,
}


def _eval(operand, *args, **kwargs):
    if isinstance(operand, int):
        return operand
    return operand(*args, **kwargs)


class SelectorOperator:
    def __init__(self, operator: str, operands: List[Union[Selector, int]]):
        assert operator in NUMERIC_OPERATORS

        self.operands = operands
        self.operator = NUMERIC_OPERATORS[operator]
        self.operator_text = operator

    def __str__(self):
        return '(' + (' '+self.operator_text+' ').\
            join([str(op) for op in self.operands]) + ')'

    def __repr__(self):
        return 'SelectorOperator(' + (' '+self.operator_text+' ').\
            join([repr(op) for op in self.operands]) + ')'

    def web_repr(self):
        return {
            'className': 'OperatorSelector',
            'args': ([self.operator_text] +
                     [selector_or_number_webrepr(op)
                      for op in self.operands]),
        }

    def __call__(self, grid: Grid, pos: Point2D,
                 global_config: Dict[str, Any]):
        result = _eval(self.operands[0], grid, pos, global_config)
        for operand in self.operands[1:]:
            result = self.operator(
                result,
                _eval(operand, grid, pos, global_config)
            )
        return result


def parse_selector_operator(p):
    p_ = p[0]
    if len(p_) == 1:
        return p_

    operands = [p_[i] for i in range(0, len(p_), 2)]
    return SelectorOperator(p_[1], operands)
