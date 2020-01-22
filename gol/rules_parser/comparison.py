import operator
from typing import Dict, Callable, Union, Any

from gol.common import Grid, Point2D
from gol.rules_parser.selector import Selector, selector_or_number_webrepr
from gol.rules_parser.selector_operator import SelectorOperator

BinaryIntOperator = Callable[[int, int], bool]

COMPARES: Dict[str, BinaryIntOperator] = {
    '<=': operator.le,
    '>=': operator.ge,
    '<': operator.lt,
    '>': operator.gt,
    '==': operator.eq,
    '!=': lambda x, y: x != y,
}


ComparisonTerm = Union[Selector, int, SelectorOperator]


def _eval(operand, *args, **kwargs):
    if isinstance(operand, int):
        return operand
    return operand(*args, **kwargs)


class Comparison:
    def __init__(self, left: ComparisonTerm, operator: str,
                 right: ComparisonTerm):
        assert operator in COMPARES

        self.operator_text = operator
        self.operator = COMPARES[operator]
        self.left = left
        self.right = right

    def __str__(self):
        return f'{str(self.left)} {self.operator_text} {str(self.right)}'

    def __repr__(self):
        return (f'Comparison({repr(self.left)} {self.operator_text} '
                f'{repr(self.right)})')

    def web_repr(self):
        return {
            'className': 'Comparator',
            'args': [
                self.operator_text,
                selector_or_number_webrepr(self.left),
                selector_or_number_webrepr(self.right),
            ],
        }

    def __call__(self, grid: Grid, pos: Point2D,
                 global_config: Dict[str, Any]) -> bool:
        left = _eval(self.left, grid, pos, global_config)
        right = _eval(self.right, grid, pos, global_config)
        return self.operator(left, right)
