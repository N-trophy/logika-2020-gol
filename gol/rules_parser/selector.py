from enum import Enum

from gol.rules_parser.errors import EInvalidExpr


class SelectorVariant(Enum):
    GRID = 0
    NUMBER = 1


class Selector:
    def __init__(self, text: str, allowed_colors: str):
        self._parse(text, allowed_colors)

    def _parse(self, text: str, allowed_colors: str):
        if text.isdigit():
            self.type = SelectorVariant.NUMBER
            self.number = int(text)
        else:
            self.type = SelectorVariant.GRID
            self._parse_grid(text, allowed_colors)

    def _parse_grid(self, text: str, allowed_colors: str):
        if len(text) != 9:
            raise EInvalidExpr(f'Selektor "{text}" neobsahuje právě 9 znaků!')
        if allowed_colors != '':
            for char in text:
                if char not in allowed_colors and char != '*':
                    raise EInvalidExpr(f'Selektor: "{text}" obsahuje '
                                       'neplatné znaky!')
        self.grid = text

    def repr(self):
        if self.type == SelectorVariant.GRID:
            return {
                'className': 'GridSelector',
                'args': [self.grid]
            }
        return {
            'className': 'ConstantSelector',
            'args': [self.number]
        }

    def __call__(self, grid):
        pass  # TODO
