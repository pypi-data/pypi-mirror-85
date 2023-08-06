#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from lark import Lark

from datum.analyzer import Analyzer
from datum.base import Component

__path__ = os.path.dirname(__file__)


class Parser(Lark):
    def __init__(self):
        self._analyzer = Analyzer()
        with open(os.path.join(__path__, 'dice.lark'), 'r') as f:
            super(Parser, self).__init__(f, parser='earley')

    def parse(self, text) -> Component:
        tree = super(Parser, self).parse(text)
        component = self._analyzer.transform(tree)
        return component
