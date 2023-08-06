#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datum.base import Component, Result


def to_value(x):
    if isinstance(x, Component):
        return x.to_result().value
    elif isinstance(x, Result):
        return x.value
    else:
        return x


def to_result(x):
    if isinstance(x, Component):
        return x.to_result()
    else:
        return x
