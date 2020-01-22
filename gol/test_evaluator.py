#!/usr/bin/env python3

import sys

if __name__ == '__main__':
    sys.path.append('..')

from gol.rules_parser import Selector, SelectorOperator, Comparison, \
    BoolOperator, Rule, parse

GRID = [
    'ccc',
    'bbb',
    'aaa',
]

config = {
    'torus': True,
}


def _test_evaluator():
    assert Selector('aaaaaaaaa')(GRID, (1, 1), {}) == 3
    assert Selector('aaaaaaaaa')(GRID, (0, 1), {}) == 2
    assert Selector('---------')(GRID, (1, 1), {}) == 0
    assert Selector('---------')(GRID, (0, 1), {}) == 0
    assert Selector('--j------')(GRID, (1, 1), {}) == 0
    assert Selector('aaacccbbb')(GRID, (1, 1), {}) == 0
    assert Selector('----b----')(GRID, (1, 1), {}) == 1
    assert Selector('----a----')(GRID, (1, 1), {}) == 0
    assert Selector('ccccbcccc')(GRID, (1, 1), {}) == 4

    assert Selector('aaaaaaaaa')(GRID, (4, 1), config) == 3
    assert Selector('---------')(GRID, (3, 1), config) == 0
    assert Selector('----b----')(GRID, (1, 4), config) == 1
    assert Selector('---------')(GRID, (0, 1), config) == 0

    assert Selector('----b----')(GRID, (1, 4), {}) == 0
    # TODO: add more tests


def _test_selector_evaluator():
    assert SelectorOperator('+', [1, 1])(GRID, (0, 0), {}) == 2
    assert SelectorOperator('-', [1, 2])(GRID, (0, 0), {}) == -1
    assert SelectorOperator('*', [2, 2])(GRID, (0, 0), {}) == 4
    assert SelectorOperator('/', [6, 2])(GRID, (0, 0), {}) == 3
    assert SelectorOperator('%', [5, 2])(GRID, (0, 0), {}) == 1

    assert SelectorOperator('+', [1, 1, 1])(GRID, (0, 0), {}) == 3
    assert SelectorOperator('-', [5, 2, 2])(GRID, (0, 0), {}) == 1
    assert SelectorOperator('-', [5, 2, 2])(GRID, (0, 0), config) == 1

    assert SelectorOperator('*', [Selector('aaaaaaaaa'), 2]) \
               (GRID, (1, 1), {}) == 6
    assert SelectorOperator('*', [Selector('aaaaaaaaa'), 3]) \
               (GRID, (1, 1), {}) == 9
    assert SelectorOperator('*', [Selector('aaaaaaaaa'), 0]) \
               (GRID, (1, 1), {}) == 0
    assert SelectorOperator('+', [Selector('aaaaaaaaa'), 2]) \
               (GRID, (1, 1), {}) == 5
    assert SelectorOperator('+', [Selector('aaaaaaaaa'),
                                  Selector('aaaaaaaaa')]) \
               (GRID, (1, 1), {}) == 6
    assert SelectorOperator('*', [Selector('aaaaaaaaa'),
                                  Selector('aaaaaaaaa')]) \
               (GRID, (1, 1), {}) == 9
    assert SelectorOperator('%', [Selector('aaa---aaa'),
                                  Selector('---aaaa-a')]) \
               (GRID, (1, 1), {}) == 1
    assert SelectorOperator('%', [Selector('----b---a'),
                                  Selector('aaaaaaaaa')]) \
               (GRID, (1, 1), {}) == 2
    assert SelectorOperator('/', [Selector('ac--bb--a'),
                                  Selector('------aaa')]) \
               (GRID, (1, 1), {}) == 1
    # TODO: add more tests


def _test_comparison_evaluator():
    assert Comparison(5, '<', 10)(GRID, (0, 0), {}) is True
    assert Comparison(5, '>', 10)(GRID, (0, 0), {}) is False
    assert Comparison(5, '<=', 10)(GRID, (0, 0), {}) is True
    assert Comparison(5, '>=', 10)(GRID, (0, 0), {}) is False
    assert Comparison(5, '==', 10)(GRID, (0, 0), {}) is False
    assert Comparison(5, '!=', 10)(GRID, (0, 0), {}) is True
    assert Comparison(1, '<', 1)(GRID, (0, 0), {}) is False

    assert Comparison(Selector('cccaaaaaa'), '>=', 6)(GRID, (1, 1), {}) is True
    assert Comparison(Selector('cccaaaaaa'), '>=', 5)(GRID, (1, 1), {}) is True
    assert Comparison(Selector('cccaaaaaa'), '>=', 7)(GRID, (1, 1),
                                                      {}) is False
    assert Comparison(Selector('cccaaaaaa'), '>', 6)(GRID, (1, 1), {}) is False

    assert Comparison(Selector('cccaaaaaa'), '>=',
                      Selector('cccaaaaaa'))(GRID, (1, 1), {}) is True
    assert Comparison(Selector('cccaaaaaa'), '==',
                      Selector('cccaaaaaa'))(GRID, (1, 1), {}) is True
    assert Comparison(Selector('cccaaaaaa'), '!=',
                      Selector('cccaaaaaa'))(GRID, (1, 1), {}) is False
    assert Comparison(Selector('cccaaaaaa'), '==',
                      Selector('cccbbbbbb'))(GRID, (1, 1), {}) is True
    assert Comparison(Selector('ccc---aaa'), '==',
                      Selector('cccbbb---'))(GRID, (1, 1), {}) is True
    assert Comparison(Selector('ccc---aaa'), '<',
                      Selector('cccbbb---'))(GRID, (1, 1), {}) is False
    # TODO: some SelectorOperators


def _test_bool_op_evaluator():
    assert BoolOperator('and', [Comparison(5, '<', 10),
                                Comparison(0, '<', 1)]
                        )(GRID, (1, 1), {}) is True
    assert BoolOperator('and', [Comparison(5, '<', 10),
                                Comparison(1, '<', 1)]
                        )(GRID, (1, 1), {}) is False
    assert BoolOperator('or', [Comparison(5, '<', 10),
                               Comparison(0, '<', 1)]
                        )(GRID, (1, 1), {}) is True
    assert BoolOperator('or', [Comparison(5, '<', 10),
                               Comparison(1, '<', 1)]
                        )(GRID, (1, 1), {}) is True
    assert BoolOperator('or', [Comparison(5, '>', 10),
                               Comparison(1, '<', 1)]
                        )(GRID, (1, 1), {}) is False
    assert BoolOperator('or', [Comparison(Selector('ccc---aaa'), '<',
                                          Selector('cccbbb---')),
                               Comparison(1, '<', 1)]
                        )(GRID, (1, 1), {}) is False
    assert BoolOperator('or', [Comparison(Selector('ccc---aaa'), '<',
                                          Selector('cccbbb---')),
                               Comparison(Selector('cccaaaaaa'), '!=',
                                          Selector('cccaaaaaa'))]
                        )(GRID, (1, 1), {}) is False


def _test_rule_evaluator():
    c1_f = Comparison(Selector('ccc---aaa'), '<', Selector('cccbbb---'))
    c2_f = Comparison(1, '<', 1)
    c3_f = Comparison(10, '<', 5)
    c1_t = Comparison(1, '>', 0)
    c2_t = Comparison(5, '<=', 10)
    b1_f = BoolOperator('or', [c1_f, c2_f])
    assert Rule(Comparison(5, '<', 10), 'r', 'g')(GRID, (1, 1,), {}) == 'r'
    assert Rule(Comparison(5, '>', 10), 'r', 'g')(GRID, (1, 1,), {}) == 'g'
    assert Rule(c3_f, 'g', Rule(c1_t, 'x', 'y'))(GRID, (1, 1), {}) == 'x'
    assert Rule(c3_f, 'g', Rule(c1_t, 'x', 'y'))(GRID, (1, 1), {}) == 'x'
    assert Rule(b1_f, 'g', 'b')(GRID, (1, 1), {}) == 'b'
    assert Rule(b1_f, 'g', Rule(c1_t, 'x', 'y'))(GRID, (1, 1), {}) == 'x'
    assert Rule(b1_f, 'g', Rule(c1_t, Rule(c2_t, 'x', 'z'), 'y'),
                )(GRID, (1, 1), {}) == 'x'
    assert Rule(b1_f, 'g',
                Rule(c1_t, Rule(c2_t, Rule(c2_f, 'v', 'x'), 'z'), 'y'),
                )(GRID, (1, 1), {}) == 'x'
    assert Rule(b1_f, 'g',
                Rule(c1_t, Rule(c2_t, Rule(c2_f, 'v', 'x'), 'z'), 'y'),
                )(GRID, (1, 1), {}) == 'x'
    assert Rule(b1_f, 'g',
                Rule(c1_t, Rule(c2_t, Rule(c2_f, 'v',
                                           Rule(b1_f, 'a',
                                                Rule(c3_f, 'b',
                                                     'x'))), 'z'), 'y'),
                )(GRID, (1, 1), config) == 'x'


if __name__ == '__main__':
    _test_evaluator()
    _test_selector_evaluator()
    _test_comparison_evaluator()
    _test_bool_op_evaluator()
    _test_rule_evaluator()
