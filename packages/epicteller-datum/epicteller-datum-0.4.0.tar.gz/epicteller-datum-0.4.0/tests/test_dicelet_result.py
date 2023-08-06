#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datum.result import *


class TestDiceletResult:
    def test_consts(self):
        origin = [ConstResult(1), ConstResult(1), ConstResult(4), ConstResult(5), ConstResult(1), ConstResult(4)]
        res = DiceletResult(origin)
        assert res.value == (1, 1, 4, 5, 1, 4)
        assert res.items == tuple(origin)
        assert len(res) == 6
        assert list(res) == origin
        assert str(res) == '1, 1, 4, 5, 1, 4'

    def test_repeat(self):
        res = DiceletResult([ConstResult(233), DiceletRepeatResult('6#D6', [1, 1, 4, 5, 1, 4])])
        assert res.value == (233, 1, 1, 4, 5, 1, 4)
        assert len(res) == 7
        assert str(res) == '233, {6#D6: 1, 1, 4, 5, 1, 4}'

    def test_repeat_with_value(self):
        res = DiceletResult([DiceletRepeatResult('6#D6', [1, 1, 4, 5, 1, 4])], [2, 2, 8, 10, 2, 8])
        assert res.value == (2, 2, 8, 10, 2, 8)
        assert len(res) == 6
        assert str(res) == '{6#D6: 1, 1, 4, 5, 1, 4}'


class TestDiceletContainerResult:
    def test_consts(self):
        res = DiceletContainerResult([ConstResult(233), ConstResult(810)])
        assert res.value == (233, 810)
        assert len(res) == 2
        assert str(res) == '{233, 810}'


class TestDiceletNegResult:
    def test_container(self):
        res = DiceletNegResult(DiceletContainerResult([ConstResult(233), ConstResult(810)]), [-233, -810])
        assert res.value == (-233, -810)
        assert len(res) == 2
        assert str(res) == '-{233, 810}'

    def test_bracket(self):
        res = DiceletNegResult(DiceletBracketResult(DiceletContainerResult([ConstResult(233), ConstResult(810)])),
                               [-233, -810])
        assert res.value == (-233, -810)
        assert len(res) == 2
        assert str(res) == '-({233, 810})'

    def test_repeat(self):
        res = DiceletNegResult(DiceletRepeatResult('6#D6', [1, 1, 4, 5, 1, 4]), [-1, -1, -4, -5, -1, -4])
        assert res.value == (-1, -1, -4, -5, -1, -4)
        assert len(res) == 6
        assert str(res) == '-{6#D6: 1, 1, 4, 5, 1, 4}'

    def test_calc_container(self):
        res = DiceletNegResult(DiceletBracketResult(DiceletCalculationResult(
            DiceletContainerResult([1, 2]), '+', DiceletContainerResult([2, 3]), [3, 5])), [-3, -5])
        assert res.value == (-3, -5)
        assert len(res) == 2
        assert str(res) == '-({1, 2} + {2, 3})'


class TestDiceletBracketResult:
    def test_consts(self):
        res = DiceletBracketResult(DiceletContainerResult([2, 3, 3]))
        assert res.value == (2, 3, 3)
        assert len(res) == 3
        assert str(res) == '({2, 3, 3})'


class TestDiceletRepeatResult:
    def test_repeat_const(self):
        res = DiceletRepeatResult('6#6', [6, 6, 6, 6, 6, 6])
        assert res.value == (6, 6, 6, 6, 6, 6)
        assert len(res) == 6
        assert str(res) == '{6#6: 6, 6, 6, 6, 6, 6}'

    def test_repeat_dice(self):
        res = DiceletRepeatResult('3#2D6', [7, 6, 8])
        assert res.value == (7, 6, 8)
        assert len(res) == 3
        assert str(res) == '{3#2D6: 7, 6, 8}'


class TestDiceletCalculationResult:
    def test_const_add_const(self):
        res = DiceletCalculationResult(
            DiceletContainerResult([ConstResult(1), ConstResult(2)]),
            '+',
            DiceletContainerResult([ConstResult(2), ConstResult(3)]),
            [3, 5],
        )
        assert res.value == (3, 5)
        assert len(res) == 2
        assert str(res) == '{1, 2} + {2, 3}'

    def test_const_add_repeat(self):
        res = DiceletCalculationResult(
            DiceletContainerResult([ConstResult(1), ConstResult(2)]),
            '+',
            DiceletRepeatResult('2D6', [6, 5]),
            [7, 7],
        )
        assert res.value == (7, 7)
        assert len(res) == 2
        assert str(res) == '{1, 2} + {2D6: 6, 5}'

    def test_const_add_repeat_container(self):
        res = DiceletCalculationResult(
            DiceletContainerResult([ConstResult(1), ConstResult(2), ConstResult(4)]),
            '+',
            DiceletContainerResult([ConstResult(3), DiceletRepeatResult('2D20', [23, 5])]),
            [4, 25, 9],
        )
        assert res.value == (4, 25, 9)
        assert len(res) == 3
        assert str(res) == '{1, 2, 4} + {3, {2D20: 23, 5}}'
