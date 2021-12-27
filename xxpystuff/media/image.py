#!/usr/bin/env python3

import numpy as np


class Image:

    @staticmethod
    def create(width, height, clearColor=None):

        blank_image = np.zeros((height, width, 3), np.uint8)
        if clearColor:
            blank_image[:, :] = tuple(clearColor)

        return blank_image

    @staticmethod
    def color(red, green, blue, alpha=None):

        if None != alpha:
            return (blue, green, red, alpha)
        else:
            return (blue, green, red)

    @staticmethod
    def gray(gray=0, alpha=None):

        if None != alpha:
            return (gray, gray, gray, alpha)
        else:
            return (gray, gray, gray)
