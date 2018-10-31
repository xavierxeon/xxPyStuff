#!/usr/bin/env python3

import math
from .console import Console

class ProgressBar:    

    def __init__(self):

        self.text = None

        self._counter = 0
    
    def __call__(self, size, maxSize):

        if maxSize == 0:
            percent = 0
            self._counter += 1
            if self._counter == 10:
                self._counter = 0
        else:
            percent = 100 * size / maxSize
            if size >= maxSize:
                self._counter = 10
            else:
                self._counter = math.floor(percent / 10)
            
        done = '#' * self._counter
        remain = '_' * (10 - self._counter)
        message = Console.white('[{0}{1}]', True).format(done, remain)
        message += Console.yellow(' {0:.2f} %').format(percent)
        if self.text:
            message += ' {0}'.format(self.text)

        print('\r' + message, end = '', flush = True)
    
    def clear(self):

        self.text = None
        print('', flush = True)
