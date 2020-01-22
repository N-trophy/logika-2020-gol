from typing import Dict, Union, Any

from gol.common import Color, Grid, Point2D
from gol.rules_parser.bool_operator import BoolOperator
from gol.rules_parser.comparison import Comparison
from gol.rules_parser.selector import Selector


def _rule_eval_rec(rule, grid: Grid, pos: Point2D,
                   global_config: Dict[str, Any]) -> Color:
    if isinstance(rule, str):
        return rule
    if rule.bool_expr(grid, pos, global_config):
        return _rule_eval_rec(rule.if_rule, grid, pos, global_config)
    return _rule_eval_rec(rule.else_rule, grid, pos, global_config)


class Rule:
    def __init__(self, bool_expr: Union[BoolOperator, Comparison],
                 if_rule: Union['Rule', Color],
                 else_rule: Union['Rule', Color]):
        self.bool_expr = bool_expr
        self.if_rule = if_rule
        self.else_rule = else_rule

    def __str__(self):
        return (f'(if {str(self.bool_expr)}: {str(self.if_rule)} else: '
                f'{str(self.else_rule)})')

    def __repr__(self):
        return (f'Rule(if {repr(self.bool_expr)}: {repr(self.if_rule)} else:'
                f' {repr(self.else_rule)})')

    def pretty_print(self, indent=0):
        prefix = '    '*indent
        print(f'{prefix}if {str(self.bool_expr)}:')
        if isinstance(self.if_rule, Rule):
            self.if_rule.pretty_print(indent+1)
        else:
            print(prefix + '    ' + str(self.if_rule))
        print(prefix + 'else:')
        if isinstance(self.else_rule, Rule):
            self.else_rule.pretty_print(indent+1)
        else:
            print(prefix + '    ' + str(self.else_rule))

    def web_repr(self):
        return {
            'className': 'ConditionalRule',
            'args': [
                rule_or_color_webrepr(self.if_rule),
                rule_or_color_webrepr(self.else_rule),
                self.bool_expr.web_repr(),
            ],
        }

    def __call__(self, grid: Grid, pos: Point2D,
                 global_config: Dict[str, Any]) -> Color:
        return _rule_eval_rec(self, grid, pos, global_config)


def rule_or_color_webrepr(rule_or_col: Union[int, Selector]) \
        -> Dict[str, Any]:
    if isinstance(rule_or_col, Rule):
        return rule_or_col.web_repr()
    return {
        'className': 'ConstantRule',
        'args': [rule_or_col]
    }


def parse_rule(p):
    if len(p) == 1:
        return p[0].lower()
    _, bool_op, _, if_rule, _, else_rule = p
    return Rule(bool_op, if_rule, else_rule)
