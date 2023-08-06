#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DiceParameterInvalidError(ValueError):
    pass


class InvalidOperatorError(ValueError):
    pass


class InvalidDiceletCalculationError(ValueError):
    pass


class DiceFaceTooBigError(DiceParameterInvalidError):
    def __init__(self, face: int):
        self.face = face


class DiceFaceTooSmallError(DiceParameterInvalidError):
    def __init__(self, face: int):
        self.face = face


class DiceCountTooBigError(DiceParameterInvalidError):
    def __init__(self, dice: int):
        self.dice = dice


class DiceCountTooSmallError(DiceParameterInvalidError):
    def __init__(self, dice: int):
        self.dice = dice


class DiceHighestTooBigError(DiceParameterInvalidError):
    def __init__(self, highest: int):
        self.highest = highest


class DiceHighestTooSmallError(DiceParameterInvalidError):
    def __init__(self, highest: int):
        self.highest = highest


class DiceLowestTooBigError(DiceParameterInvalidError):
    def __init__(self, lowest: int):
        self.lowest = lowest


class DiceLowestTooSmallError(DiceParameterInvalidError):
    def __init__(self, lowest: int):
        self.lowest = lowest


class EmptyDiceletError(InvalidDiceletCalculationError):
    def __init__(self):
        pass


class DiceletOverSizeError(InvalidDiceletCalculationError):
    def __init__(self, size: int):
        self.size = size


class DiceletSizeMismatchError(InvalidDiceletCalculationError):
    def __init__(self, size_a: int, size_b: int):
        self.size_a = size_a
        self.size_b = size_b
