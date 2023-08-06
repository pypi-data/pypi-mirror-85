#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from typing import Callable


class Result:
    @property
    def value(self):
        raise NotImplementedError  # pragma: no cover


class Component:
    def __init__(self):
        self._generator = self._generator

    def to_result(self) -> Result:
        raise NotImplementedError  # pragma: no cover

    def set_dice_generator(self, generator: Callable[[int], int]) -> None:
        self._generator = generator

    @staticmethod
    def _generator(face: int) -> int:
        return random.randint(1, face)
