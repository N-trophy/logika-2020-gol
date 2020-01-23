from typing import List, Tuple, Dict
import copy
import random

Color = str
Point2D = Tuple[int, int]  # x, y

NEIGHBOURHOOD = {  # x, y
    0: (-1, -1),
    1: (0, -1),
    2: (1, -1),
    3: (-1, 0),
    4: (0, 0),
    5: (1, 0),
    6: (-1, 1),
    7: (0, 1),
    8: (1, 1),
}


class Reporter:
    def __init__(self):
        self.lines = []

    def __call__(self, text: str) -> None:
        self.lines.append(text)

    def text(self) -> str:
        return '\n'.join(self.lines)


class Grid:
    def __init__(self, array: List[List[str]]):
        self.array = array

    @classmethod
    def fromstr(cls, s: str) -> 'Grid':
        array = [list(line.strip()) for line in s.strip().split('\n')]
        assert len(set([len(line) for line in array])) == 1  # assert square
        return cls(array)

    @classmethod
    def fromfill(cls, width: int, height: int, default: str = ' ') -> 'Grid':
        array = [[default for _ in range(width)] for _ in range(height)]
        return cls(array)

    @classmethod
    def fromlist(cls, lst: List[str], width: int) -> 'Grid':
        array = [lst[x:x+width] for x in range(0, len(lst), width)]
        return cls(array)

    @property
    def width(self):
        return len(self.array[0])

    @property
    def height(self):
        return len(self.array)

    def __getitem__(self, key) -> List[str]:
        return self.array[key]

    def __eq__(self, other: 'Grid') -> bool:
        return self.array == other

    def __neq__(self, other: 'Grid') -> bool:
        return not (self == other)

    def __str__(self) -> str:
        return str(self.array)

    def __repr__(self) -> str:
        return 'Grid(' + str(self) + ')'


def points_add(a: Point2D, b: Point2D) -> Point2D:
    return (a[0]+b[0], a[1]+b[1])


def point_in_grid(p: Point2D, grid: Grid) -> bool:
    return p[0] >= 0 and p[1] >= 0 and p[0] < grid.width and p[1] < grid.height


def recolor_grid(grid: Grid, color_map: Dict[str, str]) -> Grid:
    new_grid = copy.deepcopy(grid)
    for y in range(grid.height):
        for x in range(grid.width):
            new_grid[y][x] = color_map.get(grid[y][x], grid[y][x])
    return new_grid


def random_grid(background: str, colors: str) -> Grid:
    width = random.randint(10, 30)
    height = random.randint(10, 30)
    grid = Grid.fromfill(width, height, background)
    symbols_count = random.randint(10, 200)
    for _ in range(symbols_count):
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        grid[y][x] = random.choice(colors)
    return grid
