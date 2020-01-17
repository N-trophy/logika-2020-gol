#!/usr/bin/env python3

import operator
from pyparsing import Forward, Word, oneOf, infixNotation, opAssoc
import string
from typing import Dict, Callable, Union, Any
import sys
import json


Color = str


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
            'args': [self.text]
        }


def _selector_or_number_webrepr(sel_or_num: Union[int, Selector]) \
        -> Dict[str, Any]:
    if isinstance(sel_or_num, Selector):
        return sel_or_num.web_repr()
    return {
        'className': 'ConstantSelector',
        'args': [str(sel_or_num)]
    }

###############################################################################


BinaryIntOperator = Callable[[int, int], bool]
COMPARES: Dict[str, BinaryIntOperator] = {
    '<=': operator.le,
    '>=': operator.ge,
    '<': operator.lt,
    '>': operator.ge,
    '==': operator.eq,
    '!=': not operator.eq,
}


class Comparison:
    def __init__(self, left: Union[Selector, int], operator: str,
                 right: Union[Selector, int]):
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
                _selector_or_number_webrepr(self.left),
                _selector_or_number_webrepr(self.right),
                self.operator_text,
            ],
        }

###############################################################################


BOOL_OPERATORS = {
    'and': operator.and_,
    'or': operator.or_,
}


class BoolOperator:
    def __init__(self, left: Comparison, operator: str, right: Comparison):
        assert operator in BOOL_OPERATORS

        self.left = left
        self.operator = BOOL_OPERATORS[operator]
        self.operator_text = operator
        self.right = right

    def __str__(self):
        return f'({str(self.left)} {self.operator_text} {str(self.right)})'

    def __repr__(self):
        return (f'BoolOperator({repr(self.left)} {self.operator_text} '
                f'{repr(self.right)})')

    def web_repr(self):
        return {
            'className': 'BoolOperator',
            'args': [
                self.left.web_repr(),
                self.right.web_repr(),
                self.operator_text,
            ],
        }


def _parse_bool_expr(p):
    if isinstance(p[0], Comparison):
        return p[0]
    return BoolOperator(*p[0])

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
        return (f'Rule(if {str(self.bool_expr)}: {str(self.if_rule)} else:'
                f' {str(self.else_rule)})')

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

    selector = Word(allowed_colors + '*', exact=1) * 9
    selector.setParseAction(lambda s: Selector(''.join(s)))

    integer = Word(string.digits).setParseAction(lambda t: int(t[0]))
    operator = oneOf('>= <= != > < ==')
    comparison = ((selector | integer) + operator + (selector | integer)).\
        setParseAction(lambda t: Comparison(*t))

    bool_expr = infixNotation(
        comparison,
        [
            ("or", 2, opAssoc.LEFT, lambda t: t),
            ("and", 2, opAssoc.LEFT, lambda t: t),
        ]
    ).setParseAction(_parse_bool_expr)

    rule = Forward()
    rule << ((Word('if') + bool_expr + Word(':') + rule + Word('else:') +
             rule) | color).setParseAction(_parse_rule)

    return rule.parseString(lines, parseAll=True)[0]


def webrepr(rule_or_color: Union[Rule, Color]) -> Dict[str, Any]:
    print(_rule_or_color_webrepr(rule_or_color))
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
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: gen-json.py rules.txt\n')
        sys.exit(1)

    with open(sys.argv[1]) as f:
        print(json.dumps(webrepr(parse(f.read(), 'bw')), indent=4))
