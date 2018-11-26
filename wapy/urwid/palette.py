#!/usr/bin/env python3

from .style import Style

class Palette(list):

    def __init__(self):

        list.__init__(self)

    def addStyle(self, style):

        self.append(style.toTuple())

    
    