#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections.abc import Sized
from typing import List, Tuple, Union, Iterable

from datum.base import Result
from datum.util import to_value

Number = Union[int, float]


class ConstResult(Result):
    def __init__(self, value: Number):
        assert isinstance(value, (int, float))
        self._value = value

    @property
    def value(self) -> Number:
        return self._value

    def __str__(self):
        return str(self._value)

    def __int__(self):
        return int(self._value)

    def __float__(self):
        return float(self._value)


class ConstNegResult(ConstResult):
    def __init__(self, r, value):
        super(ConstNegResult, self).__init__(value)
        self._origin = r

    def __str__(self):
        return '-{}'.format(str(self._origin))


class ConstBracketResult(ConstResult):
    def __init__(self, r: Result):
        super(ConstBracketResult, self).__init__(to_value(r))
        self._origin = r

    def __str__(self):
        return '({})'.format(str(self._origin))


class ConstCalculationResult(ConstResult):
    def __init__(self, a, oper, b, value: Number):
        super(ConstCalculationResult, self).__init__(value)
        self._a = a
        self._oper = oper
        self._b = b

    def __str__(self):
        return '{} {} {}'.format(str(self._a), self._oper, str(self._b))


class DiceResult(ConstResult):
    SIMPLE = 0
    HIGHEST = 1
    LOWEST = 2

    def __init__(self, dice: Number, face: Number,
                 dices: Iterable[int], *,
                 highest: Number = None, lowest: Number = None):
        self._dice = int(dice)
        self._face = int(face)
        if highest is not None and highest < dice:
            highest = int(highest)
            self._size = highest
            self._highest = highest
            self._mode = self.HIGHEST
        elif lowest is not None and lowest < dice:
            lowest = int(lowest)
            self._size = lowest
            self._lowest = lowest
            self._mode = self.LOWEST
        else:
            self._size = self._dice
            self._mode = self.SIMPLE
        self._dices: List[int] = list(dices)
        self._selected: List[int] = []
        self._selected_index: List[bool] = [False for _ in self._dices]
        self._fill_dices()
        super(DiceResult, self).__init__(sum(self._selected))

    @property
    def dice(self) -> int:
        return self._dice

    @property
    def face(self) -> int:
        return self._face

    @property
    def highest(self) -> int:
        if hasattr(self, '_highest'):
            return self._highest

    @property
    def lowest(self) -> int:
        if hasattr(self, '_lowest'):
            return self._lowest

    @property
    def mode(self) -> int:
        return self._mode

    @property
    def dices(self) -> Tuple[int]:
        return tuple(self._dices)

    @property
    def selected(self) -> Tuple[int]:
        return tuple(self._selected)

    def _fill_dices(self):
        # keep mode is disabled
        if self._mode == self.SIMPLE:
            self._selected_index = [True for _ in self._dices]
            self._selected = self._dices
            return

        sorted_index = sorted(list(range(len(self._dices))), key=lambda i: self._dices[i])
        if self._mode == self.HIGHEST:
            target_index = sorted_index[-int(self._highest):]
        else:  # mode must be LOWEST
            target_index = sorted_index[:int(self._lowest)]

        for index in target_index:
            self._selected_index[index] = True
        self._selected = [dice for is_selected, dice
                          in zip(self._selected_index, self._dices)
                          if is_selected]

    def __str__(self):
        dice_name = '{}D{}'.format(self._dice, self._face)
        if self._mode != self.SIMPLE:
            dice_name = '{}{}{}'.format(dice_name,
                                        'H' if self._mode == self.HIGHEST else 'L',
                                        self._highest if self._mode == self.HIGHEST else self._lowest)
        dice_list = ' + '.join(
            str(self._dices[index])
            if self._selected_index[index]
            else '{}*'.format(self._dices[index])
            for index in range(len(self.dices)))
        if len(self._dices) == 1:
            dice_content = '{}'.format(dice_list)
        else:
            dice_content = '{} = {}'.format(dice_list, self.value)
        return '[{}: {}]'.format(dice_name, dice_content)


class DiceletResult(Iterable, Sized, Result):
    @staticmethod
    def _flatten(values):
        res = []
        for value in values:
            if isinstance(value, Iterable):
                res += value
            else:
                res.append(value)
        return res

    def __init__(self, args: Iterable[Union[Result, Number]], values: Iterable[Number] = None):
        self._items = list(args)
        if values:
            self._value = values
        else:
            self._value = self._flatten([to_value(i) for i in self._items])

    @property
    def value(self) -> Tuple[Number]:
        return tuple(self._value)

    @property
    def items(self) -> Tuple[Union[Result, Number]]:
        return tuple(self._items)

    def __len__(self):
        return len(self._value)

    def __str__(self):
        return ', '.join([str(i) for i in self._items])

    def __iter__(self):
        for item in self._items:
            yield item


class DiceletContainerResult(DiceletResult):
    def __str__(self):
        return '{{{}}}'.format(super(DiceletContainerResult, self).__str__())


class DiceletNegResult(DiceletResult):
    def __init__(self, r: DiceletResult, values: Iterable[Number]):
        super(DiceletNegResult, self).__init__([r], values)

    def __str__(self):
        return '-{}'.format(super(DiceletNegResult, self).__str__())


class DiceletBracketResult(DiceletResult):
    def __init__(self, r: DiceletResult):
        super(DiceletBracketResult, self).__init__([r])

    def __str__(self):
        return '({})'.format(super(DiceletBracketResult, self).__str__())


class DiceletRepeatResult(DiceletResult):
    def __init__(self, expr: str, values: Iterable[Number]):
        self._expr = expr
        super(DiceletRepeatResult, self).__init__(values)

    def __str__(self):
        inner = ', '.join([str(i) for i in self._items])
        return '{{{}: {}}}'.format(self._expr, inner)


class DiceletCalculationResult(DiceletResult):
    def __init__(self, a: DiceletResult, oper, b: DiceletResult, value: Iterable[Number]):
        super(DiceletCalculationResult, self).__init__(value)
        self._a = a
        self._oper = oper
        self._b = b

    def __str__(self):
        return '{!s} {} {!s}'.format(self._a, self._oper, self._b)
