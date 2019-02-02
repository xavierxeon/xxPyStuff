#!/usr/bin/env python3

from .style import Style

class Palette:

    def __init__(self):

        self.styleList = list()
        self._iterCounter = 0

    def addStyle(self, style):

        self.styleList.append(style.toTuple())

    def __iter__(self):

        self._iterCounter = 0
        return self

    def __next__(self):

        if self._iterCounter < len(self.styleList):
            val = self.styleList[self._iterCounter]
            self._iterCounter += 1
            return val
        else:
            raise StopIteration
