import operator
from typing import Tuple, Callable, Dict

from selector import Selector
from errors import EInvalidExpr


Operator = Callable[[int, int], bool]


COMPARES: Dict[str, Operator] = {
    '<=': operator.le,
    '>=': operator.ge,
    '<': operator.lt,
    '>': operator.ge,
    '==': operator.eq,
}


def _split_compare(text: str) -> Tuple[str, str, str, Operator]:
    operators = [operator for operator in COMPARES.keys() if operator in text]
    operators_set = set([text.index(operator) for operator in operators])
    if len(operators_set) == 0:
        raise EInvalidExpr(f'Výraz "{text}" neobsahuje operátor!')
    if len(operators_set) > 1:
        raise EInvalidExpr(f'Výraz "{text}" obsahuje více operátorů než '
                           'jeden!')

    left, right = text.split(operators[0])
    return left, right, operators[0], COMPARES[operators[0]]


class Comparator:
    def __init__(self, text: str, allowed_colors: str):
        self._parse(text, allowed_colors)

    def _parse(self, text: str, allowed_colors: str):
        text = text.replace(' ', '')
        self.left_text, self.right_text, self.operator_text, self.operator = \
            _split_compare(text)
        self.left = Selector(self.left_text, allowed_colors)
        self.right = Selector(self.right_text, allowed_colors)

    def repr(self):
        return {
            'className': 'Comparator',
            'args': [
                self.left.repr(),
                self.right.repr(),
                self.operator_text,
            ],
        }
