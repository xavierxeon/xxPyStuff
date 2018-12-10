#!/usr/bin/env python3

import math
from .console import Console

class ProgressBar:    

    _symbols = [Console.green('-'), Console.green('/'), Console.green('|'), Console.green('\\')]

    def __init__(self):

        self.text = None
        self._segments = 0
    
    def __call__(self, count, maxCount = None):

        if not maxCount:
            symbol = ProgressBar._symbols[self._segments]
            self._segments += 1
            if self._segments >= len(ProgressBar._symbols):
                self._segments = 0

            if self.text:
                message = '{0} {1}'.format(self.text, symbol) 
            else:
                message = '{0}'.format(symbol)
        else:
            percent = 100 * count / maxCount
            if count >= maxCount:
                self._segments = 10
            else:
                self._segments = math.floor(percent / 10)
            
            done = '#' * self._segments
            remain = '_' * (10 - self._segments)
            message = Console.white('[{0}{1}]', True).format(done, remain)
            message += Console.yellow(' {0:.2f} %').format(percent)
            if self.text:
                message += ' {0}'.format(self.text)

        print('\r' + message, end = '', flush = True)

    def setText(self, text):

        self.text = text
    
    def clear(self, trailer):

        self.text = None
        self._segments = 0
        
        if trailer:
            print(' ' + trailer, flush = True)
        else:
            print('', flush = True)
