#!/usr/bin/env python3

class Color:

    def __init__(self, red = 0, green = 0, blue = 0):

        self._red = red
        self._green = green
        self._blue = blue

    def __len__(self):
        return 3

    def __iter__(self): 
        #get opencv friendly tuple
        yield self._blue
        yield self._green
        yield self._red
