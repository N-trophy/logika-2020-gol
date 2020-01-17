from typing import List, Tuple

Color = str
Grid = List[List[str]]
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


def points_add(a: Point2D, b: Point2D) -> Point2D:
    return (a[0]+b[0], a[1]+b[1])


def point_in_grid(p: Point2D, grid: Grid) -> bool:
    return p[0] >= 0 and p[1] >= 0 and p[0] < len(grid[0]) and p[1] < len(grid)
