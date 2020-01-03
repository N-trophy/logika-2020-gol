from enum import Enum
from errors import EInvalidExpr


class SelectorVariant(Enum):
    GRID = 0
    NUMBER = 1


class Selector:
    def __init__(self, text: str, color_codes: str):
        self._parse(text, color_codes)

    def _parse(self, text: str, color_codes: str):
        if text.isdigit():
            self.type = SelectorVariant.NUMBER
            self.number = int(text)
        else:
            self.type = SelectorVariant.GRID
            self._parse_grid(text, color_codes)

    def _parse_grid(self, text: str, color_codes: str):
        if len(text) != 9:
            raise EInvalidExpr(f'Selektor {text} neobsahuje právě 9 znaků!')
        for char in text:
            if char not in color_codes and char != '*':
                raise EInvalidExpr(f'Selektor: {text} obsahuje neplatné znaky!')
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
