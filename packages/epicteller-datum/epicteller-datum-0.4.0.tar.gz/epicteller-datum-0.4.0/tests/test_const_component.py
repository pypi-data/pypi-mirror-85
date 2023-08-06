#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from unittest.mock import patch

from datum.component import *
from datum import error


@patch('random.randint')
class TestDice:
    def test_single_simple(self, mocker):
        mocker.return_value = 3
        dice = Dice(1, 6)
        assert str(dice) == '1D6'
        mocker.assert_not_called()

        res = dice.to_result()
        mocker.assert_called_once_with(1, 6)
        assert res.value == 3
        assert str(res) == '[1D6: 3]'

    def test_dice_with_injected_generator(self, mocker):
        dice = Dice(1, 20)
        dice.set_dice_generator(lambda x: 21)
        res = dice.to_result()
        mocker.assert_not_called()
        assert res.value == 21
        assert str(res) == '[1D20: 21]'

    def test_multiple_simple(self, mocker):
        mocker.return_value = 13
        dice = Dice(4, 20)
        assert str(dice) == '4D20'
        mocker.assert_not_called()

        res = dice.to_result()
        assert mocker.call_count == 4
        assert res.value == 52
        assert str(res) == '[4D20: 13 + 13 + 13 + 13 = 52]'

    def test_highest(self, mocker):
        mocker.side_effect = lambda _, __: mocker.call_count
        dice = Dice(8, 6, highest=3)
        assert str(dice) == '8D6H3'

        res = dice.to_result()
        assert mocker.call_count == 8
        assert res.value == 21
        assert res.dices == (1, 2, 3, 4, 5, 6, 7, 8)
        assert res.selected == (6, 7, 8)
        assert str(res) == '[8D6H3: 1* + 2* + 3* + 4* + 5* + 6 + 7 + 8 = 21]'

    def test_lowest(self, mocker):
        mocker.side_effect = lambda _, __: mocker.call_count
        dice = Dice(8, 6, lowest=3)
        assert str(dice) == '8D6L3'

        res = dice.to_result()
        assert mocker.call_count == 8
        assert res.value == 6
        assert res.dices == (1, 2, 3, 4, 5, 6, 7, 8)
        assert res.selected == (1, 2, 3)
        assert str(res) == '[8D6L3: 1 + 2 + 3 + 4* + 5* + 6* + 7* + 8* = 6]'

    def test_invalid_dices(self, _):
        with pytest.raises(error.DiceCountTooSmallError):
            Dice(0, 2).to_result()
        with pytest.raises(error.DiceFaceTooSmallError):
            Dice(1, 0).to_result()
        with pytest.raises(error.DiceLowestTooSmallError):
            Dice(30, 20, lowest=-2).to_result()
        with pytest.raises(error.DiceHighestTooBigError):
            Dice(30, 20, highest=10000).to_result()


class TestConstBracket:
    def test_const(self):
        com = ConstBracket(ConstResult(3))
        assert str(com) == '(3)'
        res = com.to_result()
        assert res.value == 3
        assert str(res) == '(3)'

    def test_neg(self):
        com = ConstBracket(ConstNeg(ConstResult(4)))
        assert str(com) == '(-4)'
        res = com.to_result()
        assert res.value == -4
        assert str(res) == '(-4)'


class TestConstNeg:
    def test_const(self):
        com = ConstNeg(ConstResult(5))
        assert str(com) == '-5'
        res = com.to_result()
        assert res.value == -5
        assert str(res) == '-5'

    def test_float(self):
        com = ConstNeg(ConstResult(3.1415))
        assert str(com) == '-3.1415'
        res = com.to_result()
        assert res.value == -3.1415
        assert str(res) == '-3.1415'

    def test_bracket(self):
        com = ConstNeg(ConstBracket(4))
        assert str(com) == '-(4)'
        res = com.to_result()
        assert res.value == -4
        assert str(res) == '-(4)'


class TestConstCalculation:
    def test_const_add_const(self):
        com = ConstCalculation(ConstResult(1919), '+', ConstResult(810))
        assert str(com) == '1919 + 810'
        res = com.to_result()
        assert res.value == 2729
        assert str(res) == '1919 + 810'

    def test_const_add_bracketed_neg(self):
        com = ConstCalculation(ConstResult(1919), '+', ConstBracket(ConstNeg(ConstResult(810))))
        assert str(com) == '1919 + (-810)'
        res = com.to_result()
        assert res.value == 1109
        assert str(res) == '1919 + (-810)'

    def test_const_mul_const(self):
        com = ConstCalculation(ConstResult(1919), '*', ConstResult(0))
        assert str(com) == '1919 * 0'
        res = com.to_result()
        assert res.value == 0
        assert str(res) == '1919 * 0'

    @patch('random.randint')
    def test_const_add_dice(self, mocker):
        mocker.return_value = 15
        com = ConstCalculation(ConstResult(1919), '+', Dice(1, 20))
        assert str(com) == '1919 + 1D20'
        res = com.to_result()
        assert res.value == 1934
        assert str(res) == '1919 + [1D20: 15]'

    def test_zero_division_error(self):
        com = ConstCalculation(ConstResult(1), '/', ConstBracket(ConstCalculation(1, '-', 1)))
        assert str(com) == '1 / (1 - 1)'
        with pytest.raises(ZeroDivisionError):
            com.to_result()

    def test_invalid_operator_error(self):
        com = ConstCalculation(ConstResult(1), '?', ConstResult(1))
        assert str(com) == '1 ? 1'
        with pytest.raises(error.InvalidOperatorError):
            com.to_result()
