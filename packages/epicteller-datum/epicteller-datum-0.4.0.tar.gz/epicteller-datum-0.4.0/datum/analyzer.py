#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lark import Transformer, v_args

from datum.base import Component
from datum.component import DiceletBracket, DiceletComponent, ConstBracket, ConstCalculation, ConstNeg, \
    Dice, DiceletContainer, DiceletRepeat, DiceletCalculation, DiceletNeg, Const, Percent
from datum.result import DiceletResult


class Analyzer(Transformer):
    @v_args(inline=True)
    def number(self, value) -> Const:
        return Const(value)

    @v_args(inline=True)
    def percent(self, num) -> Percent:
        return Percent(num)

    @v_args(inline=True)
    def bracket(self, a) -> Component:
        if isinstance(a, (DiceletComponent, DiceletResult)):
            return DiceletBracket(a)
        else:
            return ConstBracket(a)

    @v_args(inline=True)
    def const_calc(self, num_a, operator, num_b) -> ConstCalculation:
        return ConstCalculation(num_a, operator, num_b)

    @v_args(inline=True)
    def const_neg(self, a):
        return ConstNeg(a)

    rand_calc = const_calc

    rand_neg = const_neg

    def simple_rand(self, params) -> Dice:
        if len(params) == 1:
            dice = 1
            face = params[0]
        else:
            dice = params[0]
            face = params[1]
        return Dice(dice, face)

    @v_args(inline=True)
    def highest_rand(self, dice, face, highest) -> Dice:
        return Dice(dice, face, highest=highest)

    @v_args(inline=True)
    def lowest_rand(self, dice, face, lowest) -> Dice:
        return Dice(dice, face, lowest=lowest)

    @v_args(inline=True)
    def dicelet_concat(self, a, b):
        if isinstance(a, DiceletContainer):
            a += b
            return a
        return DiceletContainer([a, b])

    @v_args(inline=True)
    def dicelet_const(self, times, expr):
        return DiceletRepeat(times, expr)

    dicelet_rand = dicelet_const

    @v_args(inline=True)
    def dicelet_calc(self, a, operator, b) -> DiceletCalculation:
        return DiceletCalculation(a, operator, b)

    @v_args(inline=True)
    def dicelet_neg(self, a: DiceletComponent) -> DiceletNeg:
        return DiceletNeg(a)
