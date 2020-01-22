import operator
from typing import Dict, Union, Any, List

from gol.common import Grid, Point2D
from gol.rules_parser.comparison import Comparison


BOOL_OPERATORS = {
    'and': operator.and_,
    'or': operator.or_,
}


class BoolOperator:
    def __init__(self, operator: str,
                 operands: List[Union[Comparison, 'BoolOperator']]):
        assert operator in BOOL_OPERATORS

        self.operands = operands
        self.operator = BOOL_OPERATORS[operator]
        self.operator_text = operator

    def __str__(self):
        return '(' + (' '+self.operator_text+' ').\
            join([str(op) for op in self.operands]) + ')'

    def __repr__(self):
        return 'BoolOperator(' + (' '+self.operator_text+' ').\
            join([str(op) for op in self.operands]) + ')'

    def web_repr(self):
        return {
            'className': 'BoolOperator',
            'args': ([self.operator_text] +
                     [op.web_repr() for op in self.operands]),
        }

    def __call__(self, grid: Grid, pos: Point2D,
                 global_config: Dict[str, Any]) -> bool:
        if self.operator == operator.and_:
            for operand in self.operands:
                if not operand(grid, pos, global_config):
                    return False
            return True
        elif self.operator == operator.or_:
            for operand in self.operands:
                if operand(grid, pos, global_config):
                    return True
            return False

        assert False, 'Invalid operator in evaluation!'


def parse_bool_expr(p):
    p_ = p[0]
    if len(p_) == 1:
        return p_

    operands = [p_[i] for i in range(0, len(p_), 2)]
    return BoolOperator(p_[1], operands)
