from typing import List
import math

from errors import EInvalidExpr


def is_correctly_bracked(expr: str) -> str:
    depth = 0

    for c in expr:
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
        if depth < 0:
            return False

    if depth != 0:
        return False
    return True


def assert_correctly_bracked(expr: str):
    if not is_correctly_bracked(expr):
        raise EInvalidExpr(f'Výraz {expr} není korektně uzávorkován!')


def end_closing_brackets_start(expr: str) -> int:
    i = len(expr)-1
    while i > 0 and expr[i] == ')':
        i -= 1
    return i


def remove_toplevel_brackets(expr: str) -> str:
    assert_correctly_bracked(expr)

    depth = 0
    min_depth = math.inf
    for c in expr[:end_closing_brackets_start(expr)]:
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth < min_depth:
                min_depth = depth

    start = 0
    while start < len(expr) and expr[start] == '(' and start < min_depth:
        start += 1

    end = len(expr)
    while end > 0 and expr[end-1] == ')' and len(expr)-end < min_depth:
        end -= 1

    return expr[start:end]


def extract(expr: str, splitters: List[str]) -> List[str]:
    assert_correctly_bracked(expr)
    expr = remove_toplevel_brackets(expr)

    result = []
    starti = 0
    depth = 0
    for i, c in enumerate(expr):
        if c == '(':
            if depth == 0:
                if expr[starti:i] in splitters:
                    result.append(expr[starti:i])
                    starti = i
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                result.append(expr[starti+1:i])
                starti = i+1

    if starti < len(expr):
        result.append(expr[starti:])
    return result


if __name__ == '__main__':
    assert remove_toplevel_brackets('()') == ''
    assert remove_toplevel_brackets('(())') == ''
    assert remove_toplevel_brackets('(()())') == '()()'
    assert remove_toplevel_brackets('(()()())') == '()()()'
    assert remove_toplevel_brackets('((()()()))') == '()()()'
    assert remove_toplevel_brackets('((()()(aa)))') == '()()(aa)'

    assert extract('()and()', ['and']) == ['', 'and', '']
    assert extract('(a=5)and(b=10)', ['and']) == ['a=5', 'and', 'b=10']
    assert extract('(a=5)and(b=10)(x)', ['and']) == ['a=5', 'and', 'b=10', 'x']
