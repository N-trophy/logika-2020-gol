import brackets
from errors import EInvalidExpr
from comparator import Comparator


OPERATORS = {
    'and': lambda x, y: x and y,
    'or': lambda x, y: x or y,
}


class BoolOperator:
    def __init__(self, expr: str, allowed_colors: str):
        expr = expr.replace(' ', '')
        self.text = expr
        self._parse(expr, allowed_colors)

    def _parse(self, expr: str, allowed_colors: str):
        extracted = brackets.extract(expr, ['and', 'or'])
        if len(extracted) != 3:
            raise EInvalidExpr(f'Neplatná podmínka: {expr}!')
        if extracted[1] not in OPERATORS.keys():
            raise EInvalidExpr(f'{extracted[1]} musí být "and" nebo "or"!')

        self.operator = extracted[1]
        self.left_text = extracted[0]
        self.right_text = extracted[2]

        left_bool_op = any([op in self.left_text for op in OPERATORS.keys()])
        right_bool_op = any([op in self.left_text for op in OPERATORS.keys()])

        if left_bool_op:
            self.left = BoolOperator(self.left_text)
        else:
            self.left = Comparator(self.left_text, allowed_colors)

        if right_bool_op:
            self.right = BoolOperator(self.right_text)
        else:
            self.right = Comparator(self.right_text, allowed_colors)

    def repr(self):
        return {
            'className': 'BoolOperator',
            'args': [
                self.left.repr(),
                self.right.repr(),
                self.operator,
            ],
        }
