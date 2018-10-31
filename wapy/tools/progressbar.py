#!/usr/bin/env python3

import math
from .console import Console

class ProgressBar:    

    def __init__(self):

        self.text = None

        self._segments = 0
    
    def __call__(self, count, maxCount):

        if maxCount == 0:
            percent = 0
            self._segments += 1
            if self._segments == 10:
                self._segments = 0
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
    
    def clear(self, trailer):

        self.text = None
        if trailer:
            print(' ' + trailer, flush = True)
        else:
            print('', flush = True)
