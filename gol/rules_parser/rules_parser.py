#!/usr/bin/env python3

from pyparsing import Forward, Word, oneOf, infixNotation, opAssoc
import string
from typing import Dict, Union, Any
import sys
import json

if __name__ == '__main__':
    sys.path.append('../..')

from gol.rules_parser.selector import Selector
from gol.rules_parser.selector_operator import parse_selector_operator
from gol.rules_parser.bool_operator import parse_bool_expr
from gol.rules_parser.rule import Rule, parse_rule, rule_or_color_webrepr
from gol.rules_parser.comparison import Comparison

from gol.common import Color


def strip_comments(lines: str) -> str:
    result = ''
    for line in lines.split('\n'):
        result += (line[:line.find('#')] if '#' in line else line) + '\n'
    return result


def parse(lines: str, allowed_colors: str = '') -> Union[Rule, Color]:
    lines = strip_comments(lines)

    if allowed_colors == '':
        allowed_colors = string.ascii_lowercase + string.ascii_uppercase
    color = Word(allowed_colors, exact=1)
    integer = Word(string.digits).setParseAction(lambda t: int(t[0]))

    selector = Word(allowed_colors + '*', exact=1) * 9
    selector.setParseAction(lambda s: Selector(''.join(s)))

    num_operation = infixNotation(
        (selector | integer),
        [
            ('*', 2, opAssoc.LEFT, parse_selector_operator),
            ('/', 2, opAssoc.LEFT, parse_selector_operator),
            ('+', 2, opAssoc.LEFT, parse_selector_operator),
            ('-', 2, opAssoc.LEFT, parse_selector_operator),
            ('%', 2, opAssoc.LEFT, parse_selector_operator),
        ]
    )

    operator = oneOf('>= <= != > < ==')
    comparison_token = num_operation | selector | integer
    comparison = (comparison_token + operator + comparison_token).\
        setParseAction(lambda t: Comparison(*t))

    bool_expr = infixNotation(
        comparison,
        [
            ('and', 2, opAssoc.LEFT, parse_bool_expr),
            ('or', 2, opAssoc.LEFT, parse_bool_expr),
        ]
    )

    rule = Forward()
    rule << ((Word('if') + bool_expr + Word(':') + rule + Word('else:') +
             rule) | color).setParseAction(parse_rule)

    return rule.parseString(lines, parseAll=True)[0]


def webrepr(rule_or_color: Union[Rule, Color]) -> Dict[str, Any]:
    return rule_or_color_webrepr(rule_or_color)

###############################################################################


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
