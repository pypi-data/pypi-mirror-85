#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from unittest.mock import patch

from datum.component import *


class TestDiceletContainer:
    def test_single_const(self):
        com = DiceletContainer(ConstResult(2))
        assert str(com) == '{2}'
        res = com.to_result()
        assert res.value == (2,)
        assert str(res) == '{2}'

    def test_multiple_const(self):
        com = DiceletContainer([ConstResult(2), ConstResult(3), ConstResult(3)])
        assert str(com) == '{2, 3, 3}'
        res = com.to_result()
        assert res.value == (2, 3, 3)
        assert str(res) == '{2, 3, 3}'

    @patch('random.randint')
    def test_dices(self, mocker):
        mocker.return_value = 12
        com = DiceletContainer([ConstResult(2), Dice(1, 20), Dice(2, 15)])
        assert str(com) == '{2, 1D20, 2D15}'
        res = com.to_result()
        assert res.value == (2, 12, 24)
        assert str(res) == '{2, [1D20: 12], [2D15: 12 + 12 = 24]}'

    @patch('random.randint')
    def test_repeat(self, mocker):
        mocker.return_value = 11
        com = DiceletContainer([ConstResult(1), DiceletRepeat(5, Dice(2, 20))])
        assert str(com) == '{1, 5#2D20}'
        assert len(com) == 6
        res = com.to_result()
        assert res.value == (1, 22, 22, 22, 22, 22)
        assert str(res) == '{1, {5#2D20: 22, 22, 22, 22, 22}}'

    def test_iadd(self):
        com = DiceletContainer([ConstResult(1)])
        assert str(com) == '{1}'
        assert len(com) == 1
        res = com.to_result()
        assert res.value == (1,)
        com += DiceletRepeat(5, ConstResult(3))
        assert str(com) == '{1, 5#3}'
        assert len(com) == 6
        res = com.to_result()
        assert res.value == (1, 3, 3, 3, 3, 3)
        assert str(res) == '{1, {5#3: 3, 3, 3, 3, 3}}'

    def test_getitem(self):
        origin = [ConstResult(1), ConstResult(2)]
        com = DiceletContainer(origin)
        assert com[0] == origin[0]
        assert com[1] == origin[1]

    def test_iter(self):
        origin = [ConstResult(1), ConstResult(2)]
        com = DiceletContainer(origin)
        coms = list(com)
        assert coms == origin


class TestDiceletBracket:
    def test_container(self):
        origin = [ConstResult(1), ConstResult(2)]
        com = DiceletBracket(DiceletContainer(origin))
        assert len(com) == 2
        assert str(com) == '({1, 2})'
        res = com.to_result()
        assert res.value == (1, 2)
        assert str(res) == '({1, 2})'

    def test_neg(self):
        origin = [ConstResult(1), ConstResult(2)]
        com = DiceletBracket(DiceletNeg(DiceletContainer(origin)))
        assert len(com) == 2
        assert str(com) == '(-{1, 2})'
        res = com.to_result()
        assert res.value == (-1, -2)
        assert str(res) == '(-{1, 2})'

    def test_repeat(self):
        com = DiceletBracket(DiceletRepeat(5, ConstResult(3)))
        assert len(com) == 5
        assert str(com) == '(5#3)'
        res = com.to_result()
        assert res.value == (3, 3, 3, 3, 3)
        assert str(res) == '({5#3: 3, 3, 3, 3, 3})'

    def test_calc(self):
        com = DiceletBracket(DiceletCalculation(DiceletContainer([1, 2]),
                                                '+',
                                                DiceletContainer([2, 3])))
        assert len(com) == 2
        assert str(com) == '({1, 2} + {2, 3})'
        res = com.to_result()
        assert res.value == (3, 5)
        assert str(res) == '({1, 2} + {2, 3})'


class TestDiceletNeg:
    def test_container(self):
        origin = [ConstResult(1), ConstResult(2)]
        com = DiceletNeg(DiceletContainer(origin))
        assert len(com) == 2
        assert str(com) == '-{1, 2}'
        res = com.to_result()
        assert res.value == (-1, -2)
        assert str(res) == '-{1, 2}'

    def test_bracket(self):
        com = DiceletNeg(DiceletBracket(DiceletContainer([ConstResult(1), ConstResult(2)])))
        assert len(com) == 2
        assert str(com) == '-({1, 2})'
        res = com.to_result()
        assert res.value == (-1, -2)
        assert str(res) == '-({1, 2})'

    def test_repeat(self):
        com = DiceletNeg(DiceletRepeat(3, 5))
        assert len(com) == 3
        assert str(com) == '-3#5'
        res = com.to_result()
        assert res.value == (-5, -5, -5)
        assert str(res) == '-{3#5: 5, 5, 5}'

    def test_calc(self):
        com = DiceletNeg(DiceletBracket(DiceletCalculation(DiceletContainer([1, 2]),
                                                           '+',
                                                           DiceletContainer([2, 3]))))
        assert len(com) == 2
        assert str(com) == '-({1, 2} + {2, 3})'
        res = com.to_result()
        assert res.value == (-3, -5)
        assert str(res) == '-({1, 2} + {2, 3})'


class TestDiceletRepeat:
    def test_const(self):
        com = DiceletRepeat(3, 5)
        assert len(com) == 3
        assert str(com) == '3#5'
        res = com.to_result()
        assert res.value == (5, 5, 5)
        assert str(res) == '{3#5: 5, 5, 5}'

    @patch('random.randint')
    def test_pure_dice(self, mocker):
        mocker.return_value = 9
        com = DiceletRepeat(3, Dice(4, 20))
        assert len(com) == 3
        assert str(com) == '3#4D20'
        res = com.to_result()
        assert res.value == (36, 36, 36)
        assert str(res) == '{3#4D20: 36, 36, 36}'

    def test_times_is_expr(self):
        com = DiceletRepeat(ConstBracket(ConstCalculation(ConstResult(3), '-', ConstResult(1))), ConstResult(6))
        assert len(com) == 2
        assert str(com) == '2#6'
        res = com.to_result()
        assert res.value == (6, 6)
        assert str(res) == '{2#6: 6, 6}'

    def test_invalid_times(self):
        com = DiceletRepeat(ConstResult(10000), 5)
        with pytest.raises(error.DiceletOverSizeError):
            com.to_result()


class TestDiceletCalculation:
    def test_consts_add_consts(self):
        com = DiceletCalculation(DiceletContainer([2, 3]), '+', DiceletContainer([3, 5]))
        assert len(com) == 2
        assert str(com) == '{2, 3} + {3, 5}'
        res = com.to_result()
        assert res.value == (5, 8)
        assert str(res) == '{2, 3} + {3, 5}'

    def test_consts_add_single(self):
        com = DiceletCalculation(DiceletContainer([2, 3]), '+', 5)
        assert len(com) == 2
        assert str(com) == '{2, 3} + {5}'
        res = com.to_result()
        assert res.value == (7, 8)
        assert str(res) == '{2, 3} + {5}'

    def test_consts_add_single_container(self):
        com = DiceletCalculation(DiceletContainer([2, 3]), '+', DiceletContainer([5]))
        assert len(com) == 2
        assert str(com) == '{2, 3} + {5}'
        res = com.to_result()
        assert res.value == (7, 8)
        assert str(res) == '{2, 3} + {5}'

    def test_single_add_consts(self):
        com = DiceletCalculation(5, '+', DiceletContainer([2, 3]))
        assert len(com) == 2
        assert str(com) == '{5} + {2, 3}'
        res = com.to_result()
        assert res.value == (7, 8)
        assert str(res) == '{5} + {2, 3}'

    def test_single_container_add_consts(self):
        com = DiceletCalculation(DiceletContainer([5]), '+', DiceletContainer([2, 3]))
        assert len(com) == 2
        assert str(com) == '{5} + {2, 3}'
        res = com.to_result()
        assert res.value == (7, 8)
        assert str(res) == '{5} + {2, 3}'

    def test_single_container_add_single_container(self):
        com = DiceletCalculation(DiceletContainer([5]), '+', DiceletContainer([6]))
        assert len(com) == 1
        assert str(com) == '{5} + {6}'
        res = com.to_result()
        assert res.value == (11,)
        assert str(res) == '{5} + {6}'

    @patch('random.randint')
    def test_const_add_repeat(self, mocker):
        mocker.return_value = 19
        com = DiceletCalculation(ConstResult(5), '+', DiceletRepeat(3, Dice(1, 20)))
        assert len(com) == 3
        assert str(com) == '{5} + 3#1D20'
        res = com.to_result()
        assert res.value == (24, 24, 24)
        assert str(res) == '{5} + {3#1D20: 19, 19, 19}'

    def test_invalid_calculation_error(self):
        com = DiceletCalculation(DiceletContainer([2, 3]), '+', DiceletContainer([1, 2, 3]))
        with pytest.raises(error.DiceletSizeMismatchError):
            com.to_result()

    def test_zero_len(self):
        com = DiceletCalculation(DiceletContainer([]), '+', ConstResult(1))
        with pytest.raises(error.EmptyDiceletError):
            com.to_result()
