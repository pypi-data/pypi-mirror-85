#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from unittest.mock import patch

from datum import Parser, error
from datum.base import Component
from datum.error import DiceParameterInvalidError

parser = Parser()


def parse(expr) -> Component:
    return parser.parse(expr)


class TestConstUnit:
    def test_number(self):
        res = parse('2').to_result()
        assert res.value == 2

    def test_percent(self):
        res = parse('1134%').to_result()
        assert res.value == 11.34

    def test_bracket(self):
        res = parse('(3)').to_result()
        assert res.value == 3
        assert str(res) == '(3)'

    def test_const_unit_mul_const_unit(self):
        res = parse('2*3').to_result()
        assert res.value == 6
        assert str(res) == '2 * 3'

    def test_neg_const_expr_mul(self):
        res = parse('-6*9').to_result()
        assert res.value == -54
        assert str(res) == '-6 * 9'

    def test_const_add_const_expr_mul(self):
        res = parse('6+8*9').to_result()
        assert res.value == 78
        assert str(res) == '6 + 8 * 9'

    @patch('random.randint')
    def test_const_single_simple_dice(self, mocker):
        mocker.return_value = 3
        res = parse('d20').to_result()
        assert res.value == 3
        assert str(res) == '[1D20: 3]'

    @patch('random.randint')
    def test_const_simple_dice(self, mocker):
        mocker.return_value = 6
        res = parse('6d20').to_result()
        assert res.value == 36
        assert str(res) == '[6D20: 6 + 6 + 6 + 6 + 6 + 6 = 36]'

    @patch('random.randint')
    def test_highest_dice(self, mocker):
        mocker.side_effect = lambda _, __: mocker.call_count
        res = parse('8d20h6').to_result()
        assert res.value == 33
        assert str(res) == '[8D20H6: 1* + 2* + 3 + 4 + 5 + 6 + 7 + 8 = 33]'

    @patch('random.randint')
    def test_lowest_dice(self, mocker):
        mocker.side_effect = lambda _, __: mocker.call_count
        res = parse('8D20l6').to_result()
        assert res.value == 21
        assert str(res) == '[8D20L6: 1 + 2 + 3 + 4 + 5 + 6 + 7* + 8* = 21]'

    @patch('random.randint')
    def test_lowest_dice_selected_overflow(self, mocker):
        mocker.return_value = 20
        res = parse('8D20L8').to_result()
        assert res.value == 160
        assert str(res) == '[8D20: 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 = 160]'

    @patch('random.randint')
    def test_dice_bracket(self, mocker):
        mocker.return_value = 1
        res = parse('(d20)').to_result()
        assert res.value == 1
        assert str(res) == '([1D20: 1])'

    @patch('random.randint')
    def test_const_mul_mul_dice(self, mocker):
        mocker.return_value = 2
        res = parse('5*8*2d20').to_result()
        assert res.value == 160
        assert str(res) == '5 * 8 * [2D20: 2 + 2 = 4]'

    @patch('random.randint')
    def test_dice_mul_mul_const(self, mocker):
        mocker.return_value = 3
        res = parse('2d20*4*2').to_result()
        assert res.value == 48
        assert str(res) == '[2D20: 3 + 3 = 6] * 4 * 2'

    @patch('random.randint')
    def test_dice_mul_dice(self, mocker):
        mocker.return_value = 4
        res = parse('2d20*2d20').to_result()
        assert res.value == 64
        assert str(res) == '[2D20: 4 + 4 = 8] * [2D20: 4 + 4 = 8]'

    @patch('random.randint')
    def test_neg_dice_mul(self, mocker):
        mocker.return_value = 5
        res = parse('-2*d20').to_result()
        assert res.value == -10
        assert str(res) == '-2 * [1D20: 5]'

    @patch('random.randint')
    def test_const_add_dice_mul(self, mocker):
        mocker.return_value = 6
        res = parse('5-1+3*d20').to_result()
        assert res.value == 22
        assert str(res) == '5 - 1 + 3 * [1D20: 6]'

    @patch('random.randint')
    def test_dice_mul_add_const(self, mocker):
        mocker.return_value = 7
        res = parse('3.5/d20+5+6').to_result()
        assert res.value == 11.5
        assert str(res) == '3.5 / [1D20: 7] + 5 + 6'

    @patch('random.randint')
    def test_dice_add_dice_mul(self, mocker):
        mocker.side_effect = lambda _, __: mocker.call_count + 6
        res = parse('d20+3*d20').to_result()
        assert res.value == 31
        assert str(res) == '[1D20: 7] + 3 * [1D20: 8]'

    def test_dicelet_concat_const(self):
        res = parse('{3,(114514/2)}').to_result()
        assert res.value == (3, 57257.0)
        assert str(res) == '{3, (114514 / 2)}'

    @patch('random.randint')
    def test_dicelet_concat_dice(self, mocker):
        mocker.side_effect = lambda _, __: mocker.call_count
        res = parse('{810, 3d20}').to_result()
        assert res.value == (810, 6)
        assert str(res) == '{810, [3D20: 1 + 2 + 3 = 6]}'

    def test_dicelet_concat_repeat(self):
        res = parse('{1919, 3#810}').to_result()
        assert res.value == (1919, 810, 810, 810)
        assert str(res) == '{1919, {3#810: 810, 810, 810}}'

    def test_dicelet_repeat_const(self):
        res = parse('10#3').to_result()
        assert res.value == (3, 3, 3, 3, 3, 3, 3, 3, 3, 3)
        assert str(res) == '{10#3: 3, 3, 3, 3, 3, 3, 3, 3, 3, 3}'

    @patch('random.randint')
    def test_dicelet_repeat_dice(self, mocker):
        mocker.side_effect = lambda _, __: mocker.call_count
        res = parse('5#3d20').to_result()
        assert res.value == (6, 15, 24, 33, 42)
        assert str(res) == '{5#3D20: 6, 15, 24, 33, 42}'

    def test_dicelet_bracket(self):
        res = parse('({1, 2, 3})').to_result()
        assert res.value == (1, 2, 3)
        assert str(res) == '({1, 2, 3})'

    def test_const_mul_mul_dicelet(self):
        res = parse('5/2 * {1, 2, 3, 4}').to_result()
        assert res.value == (2.5, 5, 7.5, 10)
        assert str(res) == '{5 / 2} * {1, 2, 3, 4}'

    @patch('random.randint')
    def test_dice_mul_mul_dicelet(self, mocker):
        mocker.return_value = 1
        res = parse('2*2d20 * {1, 2, 3}').to_result()
        assert res.value == (4, 8, 12)
        assert str(res) == '{2 * [2D20: 1 + 1 = 2]} * {1, 2, 3}'

    def test_dicelet_mul_const_mul(self):
        res = parse('{1, 2, 3} / (1 / 2)').to_result()
        assert res.value == (2.0, 4.0, 6.0)
        assert str(res) == '{1, 2, 3} / {(1 / 2)}'

    @patch('random.randint')
    def test_dicelet_mul_dice_mul(self, mocker):
        mocker.return_value = 1
        res = parse('{1,2,3}*3d20/2').to_result()
        assert res.value == (1.5, 3.0, 4.5)
        assert str(res) == '{1, 2, 3} * {[3D20: 1 + 1 + 1 = 3]} / {2}'

    def test_dicelet_mul_dicelet(self):
        res = parse('{1,2,3}*{2,4,6}').to_result()
        assert res.value == (2, 8, 18)
        assert str(res) == '{1, 2, 3} * {2, 4, 6}'

    def test_neg_dicelet_mul(self):
        res = parse('-{1,2,3}*{1,2,3}').to_result()
        assert res.value == (-1, -4, -9)
        assert str(res) == '-{1, 2, 3} * {1, 2, 3}'

    def test_const_add_dicelet_mul(self):
        res = parse('5 + {1,2}*1.2').to_result()
        assert res.value == (6.2, 7.4)
        assert str(res) == '{5} + {1, 2} * {1.2}'

    @patch('random.randint')
    def test_dice_add_dicelet_mul(self, mocker):
        mocker.return_value = 3
        res = parse('d20+3#4').to_result()
        assert res.value == (7, 7, 7)
        assert str(res) == '{[1D20: 3]} + {3#4: 4, 4, 4}'

    def test_division_zero_error(self):
        with pytest.raises(ZeroDivisionError):
            parse('2/((5*6)-30)').to_result()

    def test_dice_parameter_invalid_error(self):
        with pytest.raises(error.DiceCountTooSmallError) as e:
            parse('(-2)d20').to_result()
        assert e.value.dice == -2

        with pytest.raises(error.DiceFaceTooSmallError) as e:
            parse('d0').to_result()
        assert e.value.face == 0
