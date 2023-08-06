#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from datum.result import *


class TestConstResult:
    def test_int(self):
        r = ConstResult(114514)
        assert r.value == 114514
        assert int(r) == 114514
        assert float(r) == 114514.0
        assert str(r) == '114514'

    def test_float(self):
        r = ConstResult(3.1415)
        assert r.value == 3.1415
        assert int(r) == 3
        assert float(r) == 3.1415
        assert str(r) == '3.1415'

    def test_wtf_types(self):
        with pytest.raises(AssertionError):
            ConstResult('wtf')


class TestDiceResult:
    def test_single_simple_dice(self):
        # D20
        res = DiceResult(1, 20, [3])
        assert res.value == 3
        assert res.dice == 1
        assert res.face == 20
        assert res.highest is None
        assert res.lowest is None
        assert res.mode == res.SIMPLE
        assert res.dices == (3,)
        assert res.selected == (3,)
        assert str(res) == '[1D20: 3]'

    def test_multiple_simple_dice(self):
        # 6D8
        res = DiceResult(6, 8, [4, 7, 4, 6, 3, 4])
        assert res.value == 28
        assert res.dice == 6
        assert res.face == 8
        assert res.highest is None
        assert res.lowest is None
        assert res.mode == res.SIMPLE
        assert res.dices == (4, 7, 4, 6, 3, 4)
        assert res.selected == (4, 7, 4, 6, 3, 4)
        assert str(res) == '[6D8: 4 + 7 + 4 + 6 + 3 + 4 = 28]'

    def test_highest_dice(self):
        # 8D6H3
        res = DiceResult(8, 6, [2, 5, 3, 5, 1, 3, 2, 4], highest=3)
        assert res.value == 14
        assert res.dice == 8
        assert res.face == 6
        assert res.highest == 3
        assert res.lowest is None
        assert res.mode == res.HIGHEST
        assert res.dices == (2, 5, 3, 5, 1, 3, 2, 4)
        assert res.selected == (5, 5, 4)
        assert str(res) == '[8D6H3: 2* + 5 + 3* + 5 + 1* + 3* + 2* + 4 = 14]'

    def test_lowest_dice(self):
        # 8D6L3
        res = DiceResult(8, 6, [2, 5, 3, 5, 1, 3, 2, 4], lowest=3)
        assert res.value == 5
        assert res.dice == 8
        assert res.face == 6
        assert res.highest is None
        assert res.lowest == 3
        assert res.mode == res.LOWEST
        assert res.dices == (2, 5, 3, 5, 1, 3, 2, 4)
        assert res.selected == (2, 1, 2)
        assert str(res) == '[8D6L3: 2 + 5* + 3* + 5* + 1 + 3* + 2 + 4* = 5]'

    def test_selected_dices_overflow(self):
        # 8D6L9
        res = DiceResult(8, 6, [2, 5, 3, 5, 1, 3, 2, 4], lowest=9)
        assert res.value == 25
        assert res.dice == 8
        assert res.face == 6
        assert res.highest is None
        assert res.lowest is None
        assert res.mode == res.SIMPLE
        assert res.dices == (2, 5, 3, 5, 1, 3, 2, 4)
        assert res.selected == (2, 5, 3, 5, 1, 3, 2, 4)
        assert str(res) == '[8D6: 2 + 5 + 3 + 5 + 1 + 3 + 2 + 4 = 25]'


class TestConstCalculationResult:
    def test_const_add_const(self):
        res = ConstCalculationResult(ConstResult(2), '+', ConstResult(5), 7)
        assert res.value == 7
        assert str(res) == '2 + 5'

    def test_const_add_dice(self):
        res = ConstCalculationResult(ConstResult(2), '+', DiceResult(6, 8, [4, 7, 4, 6, 3, 4]), 30)
        assert res.value == 30
        assert str(res) == '2 + [6D8: 4 + 7 + 4 + 6 + 3 + 4 = 28]'

    def test_const_sub_bracketed_dice(self):
        res = ConstCalculationResult(ConstResult(4.1), '-',
                                     ConstNegResult(ConstBracketResult(DiceResult(6, 8, [4, 7, 4, 6, 3, 4])), -28),
                                     32.1)
        assert res.value == 32.1
        assert str(res) == '4.1 - -([6D8: 4 + 7 + 4 + 6 + 3 + 4 = 28])'


class TestConstNegResult:
    def test_const_result_int(self):
        res = ConstNegResult(ConstResult(12), -12)
        assert res.value == -12
        assert str(res) == '-12'

    def test_const_result_float(self):
        res = ConstNegResult(ConstResult(4.5), -4.5)
        assert res.value == -4.5
        assert str(res) == '-4.5'

    def test_dice_result(self):
        res = ConstNegResult(DiceResult(1, 20, [16]), -16)
        assert res.value == -16
        assert str(res) == '-[1D20: 16]'

    def test_const_bracket_result(self):
        res = ConstNegResult(ConstBracketResult(ConstResult(5.0)), -5.0)
        assert res.value == -5.0
        assert str(res) == '-(5.0)'


class TestConstBracketResult:
    def test_const_result(self):
        res = ConstBracketResult(ConstResult(2))
        assert res.value == 2
        assert str(res) == '(2)'

    def test_dice_result(self):
        res = ConstBracketResult(DiceResult(1, 20, [16]))
        assert res.value == 16
        assert str(res) == '([1D20: 16])'

    def test_const_neg_result(self):
        res = ConstBracketResult(ConstNegResult(ConstResult(4.5), -4.5))
        assert res.value == -4.5
        assert str(res) == '(-4.5)'

    def test_const_calculation_result(self):
        res = ConstBracketResult(ConstCalculationResult(ConstResult(5), '+', ConstResult(4.3), 9.3))
        assert res.value == 9.3
        assert str(res) == '(5 + 4.3)'
