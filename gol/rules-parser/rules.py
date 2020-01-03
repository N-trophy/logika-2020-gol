from typing import List, Tuple
from enum import Enum
from errors import EInvalidExpr
from bool_operator import BoolOperator, OPERATORS
from comparator import Comparator
import brackets


class RuleType(Enum):
    CONSTANT = 0
    CONDITION = 1


class Rule:
    def __init__(self, line: str, allowed_colors: str):
        self.if_rule = None
        self.else_rule = None
        self.type = None
        self.color = None

        if line.startswith('if'):
            self._parse_if(line, allowed_colors)
        else:
            self._parse_constant(line, allowed_colors)

    def _parse_if(self, line: str, allowed_colors: str):
        if not line.endswith(':'):
            raise EInvalidExpr(f'Řádek nekončí dvojtečkou!')

        self.type = RuleType.CONDITION
        self.condition_text = brackets.remove_toplevel_brackets(line[2:-1])
        bool_op = any([op in self.condition_text for op in OPERATORS.keys()])

        if bool_op:
            self.condition = BoolOperator(self.condition_text, allowed_colors)
        else:
            self.condition = Comparator(self.condition_text, allowed_colors)

    def _parse_constant(self, line: str, allowed_colors: str):
        if line not in allowed_colors:
            raise EInvalidExpr(f'Neplatná barva: {line}!')
        self.type = RuleType.CONSTANT
        self.color = line

    def repr(self):
        if self.type == RuleType.CONSTANT:
            return {
                'className': 'ConstantRule',
                'args': [self.color],
            }

        return {
            'className': 'ConditionalRule',
            'args': [
                self.if_rule.repr() if self.if_rule is not None else None,
                self.else_rule.repr() if self.else_rule is not None else None,
                self.condition.repr(),
            ],
        }


def rules(lines: str, allowed_colors: str) -> Rule:
    lines = lines.split('\n')
    if not lines[0].strip().startswith('if'):
        raise EInvalidExpr(f'Řádek 1 nezačíná příkazem "if"!')

    stack = []

    for i, line in enumerate(lines):
        line = line.strip()
        if line == '':
            continue

        try:
            if line.startswith('else:'):
                if len(stack) < 2:
                    raise EInvalidExpr('else před sebou nemá "if" nebo tělo '
                                      'podmínky!')

                if (stack[-2].if_rule is not None and
                    stack[-1].type == RuleType.CONSTANT):
                    # else-branch constant rule to else-branch
                    rule = stack.pop()
                    if stack[-1].else_rule is not None:
                        raise EInvaliExpr('Více else větví!')
                    stack[-1].else_rule = rule

                while (stack[-1].if_rule is not None and
                       stack[-1].else_rule is None):
                    # Propagate to else-branches till else-branches are empty
                    # and if-branches are non-empty
                    rule = stack.pop()
                    stack[-1].else_rule = rule

                # Whole rule before else to if-branch
                rule = stack.pop()
                if not stack or stack[-1].if_rule is not None:
                    raise EInvalidExpr('Neplatný výraz!')
                stack[-1].if_rule = rule

            else:
                stack.append(Rule(line.replace(' ', ''), allowed_colors))
                if len(stack) >= 2 and stack[-2].type == RuleType.CONSTANT:
                    raise EInvalidExpr('Po barvě může následovat jedině else!')

            # print(len(stack))
            # for rule in stack:
            #    print(rule.repr())
            # print('--------------------')
        except EInvalidExpr as exc:
            args = list(exc.args)
            if args:
                args[0] = f"Chyba na řádku {i+1}: {args[0]}"
            exc.args = tuple(args)
            raise

    if (stack[-1].type == RuleType.CONDITION and
        (stack[-1].if_rule is None or stack[-1].else_rule is None)):
        raise EInvalidExpr('Výraz není řádně ukončen!')
    rule = stack.pop()
    if stack[-1].else_rule is not None:
        raise EInvaliExpr('Více else větví!')
    stack[-1].else_rule = rule
    while len(stack) > 1 and stack[-2].else_rule is None:
        # Pack all end else branches
        rule = stack.pop()
        stack[-1].else_rule = rule

    if len(stack) != 1:
        raise EInvaliExpr('Více top-level podmínek!')

    return stack[0]
