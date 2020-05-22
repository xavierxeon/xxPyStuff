#!/usr/bin/env python3

import numpy as np

class Image:

    def __init__(self, width, height):

        self._width = width
        self._height = height

    def create(self, clearColor = None):
        
        blank_image = np.zeros((self._height, self._width, 3), np.uint8)
        if clearColor:
            blank_image[:,:] = tuple(clearColor)
            
        return blank_image
