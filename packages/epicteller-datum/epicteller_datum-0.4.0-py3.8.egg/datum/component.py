#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from abc import ABC, abstractmethod
from collections.abc import Iterable, Sized

from datum import error
from datum.const import MAX_DICE_FACE, MAX_DICE_COUNT, MAX_HIGHEST_COUNT, MAX_LOWEST_COUNT, MAX_DICELET_SIZE
from datum.base import Component
from datum.result import ConstResult, ConstCalculationResult, DiceResult, DiceletResult, DiceletNegResult, \
    DiceletBracketResult, ConstNegResult, ConstBracketResult, DiceletCalculationResult, DiceletRepeatResult, \
    DiceletContainerResult
from datum.util import to_value, to_result


class ConstComponent(Component):
    def to_result(self) -> ConstResult:
        raise NotImplementedError  # pragma: no cover


class Const(Component):
    def __init__(self, value):
        super().__init__()
        self._value = value

    def to_result(self) -> ConstResult:
        try:
            value = int(self._value)
        except ValueError:
            value = float(self._value)
        return ConstResult(value)

    def __str__(self):
        return str(self._value)


class Percent(Component):
    def __init__(self, value):
        super().__init__()
        self._value = value

    def to_result(self) -> ConstResult:
        return ConstResult(float(self._value) / 100)


class ConstNeg(ConstComponent):
    def __init__(self, origin):
        super().__init__()
        self._origin = origin

    def to_result(self) -> ConstResult:
        result = to_result(self._origin)
        value = -to_value(result)
        return ConstNegResult(result, value)

    def __str__(self):
        return '-{!s}'.format(self._origin)


class ConstBracket(ConstComponent):
    def __init__(self, origin):
        super().__init__()
        self._origin = origin

    def to_result(self) -> ConstResult:
        return ConstBracketResult(to_result(self._origin))

    def __str__(self):
        return '({!s})'.format(self._origin)


class ConstCalculation(ConstComponent):
    def __init__(self, a, operator, b):
        super().__init__()
        self._a = a
        self._operator = operator
        self._b = b

    def to_result(self) -> ConstResult:
        res_a = to_result(self._a)
        res_b = to_result(self._b)
        value_a = to_value(res_a)
        value_b = to_value(res_b)
        oper = self._operator
        if oper == '+':
            value = value_a + value_b
        elif oper == '-':
            value = value_a - value_b
        elif oper in ('*', 'x', 'X'):
            value = value_a * value_b
        elif oper == '/':
            value = value_a / value_b
        else:
            raise error.InvalidOperatorError
        return ConstCalculationResult(res_a, self._operator, res_b, value)

    def __str__(self):
        return '{!s} {} {!s}'.format(self._a, self._operator, self._b)


class Dice(ConstComponent):
    def __init__(self, dice, face, *, highest=None, lowest=None):
        super().__init__()
        self._dice = dice
        self._face = face
        self._highest = highest or None
        self._lowest = lowest or None

    def to_result(self) -> DiceResult:
        dice = int(to_value(self._dice))
        face = int(to_value(self._face))
        highest = int(to_value(self._highest)) if self._highest is not None else None
        lowest = int(to_value(self._lowest)) if self._lowest is not None else None
        self._validate(dice, face, highest, lowest)
        dices = [self._generator(face) for _ in range(dice)]
        return DiceResult(dice, face, dices, highest=highest, lowest=lowest)

    @staticmethod
    def _validate(dice, face, highest, lowest):
        if dice < 1:
            raise error.DiceCountTooSmallError(dice)
        if dice > MAX_DICE_COUNT:
            raise error.DiceCountTooBigError(dice)
        if face < 1:
            raise error.DiceFaceTooSmallError(face)
        if face > MAX_DICE_FACE:
            raise error.DiceFaceTooBigError(face)
        if highest is not None:
            if highest < 1:
                raise error.DiceHighestTooSmallError(highest)
            if highest > MAX_HIGHEST_COUNT:
                raise error.DiceHighestTooBigError(highest)
        if lowest is not None:
            if lowest < 1:
                raise error.DiceLowestTooSmallError(lowest)
            if lowest > MAX_LOWEST_COUNT:
                raise error.DiceLowestTooBigError(lowest)

    def __str__(self):
        pure = '{!s}D{!s}'.format(self._dice, self._face)
        if self._highest:
            return '{}H{!s}'.format(pure, self._highest)
        elif self._lowest:
            return '{}L{!s}'.format(pure, self._lowest)
        return pure


class DiceletComponent(ABC, Sized, Component):
    @abstractmethod
    def to_result(self) -> DiceletResult:
        raise NotImplementedError  # pragma: no cover


class DiceletContainer(Iterable, DiceletComponent):
    @staticmethod
    def _calc_len(origin):
        _len = 0
        for i in origin:
            if isinstance(i, Sized):
                _len += len(i)
            else:
                _len += 1
        return _len

    @staticmethod
    def _to_list(origin):
        if not isinstance(origin, Iterable):
            return [origin]
        return list(origin)

    def __init__(self, origin):
        super().__init__()
        self._container = self._to_list(origin)
        self._len = self._calc_len(self._container)

    def __iadd__(self, other):
        other = self._to_list(other)
        self._container += other
        self._len += self._calc_len(other)
        return self

    def __iter__(self):
        for i in self._container:
            yield i

    def __len__(self):
        return self._len

    def __getitem__(self, item):
        return self._container[item]

    def to_result(self) -> DiceletContainerResult:
        if self._len < 1:
            raise error.EmptyDiceletError()
        if self._len > MAX_DICELET_SIZE:
            raise error.DiceletOverSizeError(self._len)
        return DiceletContainerResult(to_result(i) for i in self._container)

    def __str__(self):
        pure = ', '.join(str(i) for i in self._container)
        return '{{{}}}'.format(pure)


class DiceletBracket(DiceletComponent):
    def __init__(self, origin: DiceletComponent):
        super().__init__()
        self._origin = origin

    def to_result(self):
        return DiceletBracketResult(self._origin.to_result())

    def __len__(self):
        return len(self._origin)

    def __str__(self):
        return '({!s})'.format(self._origin)


class DiceletNeg(DiceletComponent):
    def __init__(self, origin: DiceletComponent):
        super().__init__()
        self._origin = origin

    def to_result(self):
        results = self._origin.to_result()
        values = [-value for value in to_value(results)]
        return DiceletNegResult(results, values)

    def __len__(self):
        return len(self._origin)

    def __str__(self):
        return '-{!s}'.format(self._origin)


class DiceletRepeat(DiceletComponent):
    def __init__(self, times, expr):
        super().__init__()
        self._times = int(to_value(times))
        self._expr = expr

    def __len__(self):
        return self._times

    def to_result(self):
        if self._times < 1:
            raise error.EmptyDiceletError()
        if self._times > MAX_DICELET_SIZE:
            raise error.DiceletOverSizeError(self._times)
        return DiceletRepeatResult(str(self), [to_value(self._expr) for _ in range(self._times)])

    def __str__(self):
        return '{}#{!s}'.format(self._times, self._expr)


class DiceletCalculation(DiceletComponent):
    @staticmethod
    def _to_container(origin):
        if isinstance(origin, DiceletComponent):
            return origin
        return DiceletContainer(origin)

    def __init__(self, a, operator, b):
        super().__init__()
        self._a = self._to_container(a)
        self._operator = operator
        self._b = self._to_container(b)

    def _validate(self):
        if len(self._a) == 0 or len(self._b) == 0:
            raise error.EmptyDiceletError()

    def _calc(self):
        self._validate()
        oper = self._operator
        res_a = self._a.to_result()
        res_b = self._b.to_result()
        if len(res_a) == len(res_b):
            value_a = to_value(res_a)
            value_b = to_value(res_b)
            return DiceletCalculationResult(
                res_a, oper, res_b, (
                    to_value(ConstCalculation(i, oper, j))
                    for i, j in zip(value_a, value_b)
                )
            )
        elif len(res_a) == 1:
            value_a = to_value(res_a)[0]
            value_b = to_value(res_b)
            return DiceletCalculationResult(
                res_a, oper, res_b, (
                    to_value(ConstCalculation(value_a, oper, i))
                    for i in value_b
                )
            )
        elif len(res_b) == 1:
            value_a = to_value(res_a)
            value_b = to_value(res_b)[0]
            return DiceletCalculationResult(
                res_a, oper, res_b, (
                    to_value(ConstCalculation(i, oper, value_b))
                    for i in value_a
                )
            )
        else:
            raise error.DiceletSizeMismatchError(len(res_a), len(res_b))

    def to_result(self) -> DiceletCalculationResult:
        return self._calc()

    def __len__(self):
        return max(len(self._a), len(self._b))

    def __str__(self):
        return '{!s} {} {!s}'.format(self._a, self._operator, self._b)
