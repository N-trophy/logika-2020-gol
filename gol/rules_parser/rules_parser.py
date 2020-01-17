#!/usr/bin/env python3

import operator
from pyparsing import Forward, Word, oneOf, infixNotation, opAssoc
import string
from typing import Dict, Callable, Union, Any, List
import sys
import json

if __name__ == '__main__':
    sys.path.append('../..')

import gol.evaluator as evaluator
from gol.evaluator import Point2D


Color = str
BinaryIntOperator = Callable[[int, int], bool]
Grid = List[List[str]]


class Selector:
    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'Selector({str(self)})'

    def web_repr(self):
        return {
            'className': 'GridSelector',
            'args': [self.text],
        }

    def __call__(self, grid: Grid, pos: Point2D,
                 global_config: Dict[str, Any]):
        return evaluator.selector_eval(self.text, grid, pos, global_config)


def _selector_or_number_webrepr(sel_or_num: Union[int, Selector]) \
        -> Dict[str, Any]:
    if isinstance(sel_or_num, int):
        return {
            'className': 'ConstantSelector',
            'args': [str(sel_or_num)]
        }
    return sel_or_num.web_repr()


###############################################################################


NUMERIC_OPERATORS: Dict[str, BinaryIntOperator] = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
    '%': operator.mod,
}


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
                     [_selector_or_number_webrepr(op)
                      for op in self.operands]),
        }

    def __call__(self, grid: Grid, pos: Point2D,
                 global_config: Dict[str, Any]):
        return evaluator.selector_op_eval(self, grid, pos, global_config)

def _parse_selector_operator(p):
    p_ = p[0]
    if len(p_) == 1:
        return p_

    operands = [p_[i] for i in range(0, len(p_), 2)]
    return SelectorOperator(p_[1], operands)


###############################################################################


COMPARES: Dict[str, BinaryIntOperator] = {
    '<=': operator.le,
    '>=': operator.ge,
    '<': operator.lt,
    '>': operator.gt,
    '==': operator.eq,
    '!=': not operator.eq,
}


ComparisonTerm = Union[Selector, int, SelectorOperator]


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
                _selector_or_number_webrepr(self.left),
                _selector_or_number_webrepr(self.right),
            ],
        }

    def __call__(self, grid: Grid, pos: Point2D,
                 global_config: Dict[str, Any]):
        return evaluator.comparison_eval(self, grid, pos, global_config)

###############################################################################


BOOL_OPERATORS = {
    'and': operator.and_,
    'or': operator.or_,
}


class BoolOperator:
    def __init__(self, operator: str, operands: List[Comparison]):
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


def _parse_bool_expr(p):
    p_ = p[0]
    if len(p_) == 1:
        return p_

    operands = [p_[i] for i in range(0, len(p_), 2)]
    return BoolOperator(p_[1], operands)

###############################################################################


class Rule:
    def __init__(self, bool_expr, if_rule, else_rule):
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
                _rule_or_color_webrepr(self.if_rule),
                _rule_or_color_webrepr(self.else_rule),
                self.bool_expr.web_repr(),
            ],
        }


def _rule_or_color_webrepr(rule_or_col: Union[int, Selector]) \
        -> Dict[str, Any]:
    if isinstance(rule_or_col, Rule):
        return rule_or_col.web_repr()
    return {
        'className': 'ConstantRule',
        'args': [rule_or_col]
    }


def _parse_rule(p):
    if len(p) == 1:
        return p[0]
    _, bool_op, _, if_rule, _, else_rule = p
    return Rule(bool_op, if_rule, else_rule)

###############################################################################


def parse(lines: str, allowed_colors: str = '') -> Union[Rule, Color]:
    if allowed_colors == '':
        allowed_colors = string.ascii_lowercase + string.ascii_uppercase
    color = Word(allowed_colors, exact=1)
    integer = Word(string.digits).setParseAction(lambda t: int(t[0]))

    selector = Word(allowed_colors + '*', exact=1) * 9
    selector.setParseAction(lambda s: Selector(''.join(s)))

    num_operation = infixNotation(
        (selector | integer),
        [
            ('*', 2, opAssoc.LEFT, _parse_selector_operator),
            ('/', 2, opAssoc.LEFT, _parse_selector_operator),
            ('+', 2, opAssoc.LEFT, _parse_selector_operator),
            ('-', 2, opAssoc.LEFT, _parse_selector_operator),
            ('%', 2, opAssoc.LEFT, _parse_selector_operator),
        ]
    )

    operator = oneOf('>= <= != > < ==')
    comparison_token = num_operation | selector | integer
    comparison = (comparison_token + operator + comparison_token).\
        setParseAction(lambda t: Comparison(*t))

    bool_expr = infixNotation(
        comparison,
        [
            ('and', 2, opAssoc.LEFT, _parse_bool_expr),
            ('or', 2, opAssoc.LEFT, _parse_bool_expr),
        ]
    )

    rule = Forward()
    rule << ((Word('if') + bool_expr + Word(':') + rule + Word('else:') +
             rule) | color).setParseAction(_parse_rule)

    return rule.parseString(lines, parseAll=True)[0]


def webrepr(rule_or_color: Union[Rule, Color]) -> Dict[str, Any]:
    return _rule_or_color_webrepr(rule_or_color)

###############################################################################


"""
print(selector.parseString('bb*bbbbbb', parseAll=True)[0])
print(comparison.parseString('wwwbbbwww != 5', parseAll=True)[0].web_repr())
print(bool_expr.parseString(
    '***bbb*** > 5 or (5 <10 and 10 > 5)', parseAll=True
)[0].web_repr())
print(_rule_or_color_webrepr(
    rule.parseFile('gol-rules.txt', parseAll=True)[0])
)
"""

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: gen-json.py rules.txt [-w]\n')
        sys.exit(1)

    web_print = '-w' in sys.argv
    repr_print = '-r' in sys.argv
    if '-w' in sys.argv:
        sys.argv.remove('-w')
    if '-r' in sys.argv:
        sys.argv.remove('-r')

    with open(sys.argv[1]) as f:
        result = parse(f.read(), 'bw')

    if web_print:
        print(json.dumps(webrepr(result), indent=4))
    elif repr_print:
        print(repr(result))
    else:
        print(result)
