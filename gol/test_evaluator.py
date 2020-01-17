#!/usr/bin/env python3

import sys

if __name__ == '__main__':
    sys.path.append('..')

from rules_parser.rules_parser import Selector, SelectorOperator

GRID = [
    'ccc',
    'bbb',
    'aaa',
]


def _test_evaluator():
    assert Selector('aaaaaaaaa')(GRID, (1, 1), {}) == 3
    assert Selector('aaaaaaaaa')(GRID, (0, 1), {}) == 2
    assert Selector('*********')(GRID, (1, 1), {}) == 9
    assert Selector('*********')(GRID, (0, 1), {}) == 6


def _test_selector_evaluator():
    assert SelectorOperator('+', [1, 1])(GRID, (0, 0), {}) == 2
    assert SelectorOperator('-', [1, 2])(GRID, (0, 0), {}) == -1
    assert SelectorOperator('*', [2, 2])(GRID, (0, 0), {}) == 4
    assert SelectorOperator('/', [6, 2])(GRID, (0, 0), {}) == 3
    assert SelectorOperator('%', [5, 2])(GRID, (0, 0), {}) == 1

    assert SelectorOperator('+', [1, 1, 1])(GRID, (0, 0), {}) == 3
    assert SelectorOperator('-', [5, 2, 2])(GRID, (0, 0), {}) == 1


if __name__ == '__main__':
    _test_evaluator()
    _test_selector_evaluator()
