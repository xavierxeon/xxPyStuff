#!/usr/bin/env python3

# \b got back one character
# \r go back to start of line

from .console import Console

class Progress:

    _symbols = ['-', '/', '|', '\\']

    def __init__(self):

        self._counter = 0
        self._prevLength  = 0
        self._leader = ''
        self._trailer = ''

    def setLeader(self, leader):

        self._leader = leader

    def advance(self, trailer = ''):

        self._trailer = trailer
        message = self._compileMesssage()

        print('\r' + message, end = '', flush = True)
    
    def clear(self, useNewLine = False):

        self._trailer = ''
        self._counter = 0

        print('\r' + ' ' * self._prevLength, end = '')
        self._prevLength = 0

        if useNewLine:
            print('\r' + self._leader)
        else:
            print('\r' + self._leader, end = '')

    def _compileMesssage(self):

        message = ''
        if self._leader:
            message += self._leader + ' '
        
        message += Console.green(self._symbols[self._counter])

        self._counter += 1
        if self._counter >= len(self._symbols):
            self._counter = 0

        if self._trailer:
            message += ' ' + self._trailer

        length = len(message)

        diff = self._prevLength - length
        if diff > 0:
            message += ' ' * diff
        
        self._prevLength = length

        return message
