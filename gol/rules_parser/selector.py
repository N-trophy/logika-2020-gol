from typing import Dict, Union, Any

from gol.common import Grid, Point2D, points_add, NEIGHBOURHOOD, point_in_grid


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
        assert len(self.text) == 9

        count = 0
        for i, colour in enumerate(self.text):
            x, y = points_add(NEIGHBOURHOOD[i], pos)
            if point_in_grid((x, y), grid):
                if colour == '*' or grid[y][x] == colour:
                    count += 1
        return count


def selector_or_number_webrepr(sel_or_num: Union[int, Selector]) \
        -> Dict[str, Any]:
    if isinstance(sel_or_num, int):
        return {
            'className': 'ConstantSelector',
            'args': [str(sel_or_num)]
        }
    return sel_or_num.web_repr()
