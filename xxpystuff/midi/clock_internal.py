#!/usr/bin/env python3

from .clock_abstract import ClockAbstract

class ClockInternal(ClockAbstract):

   def __init__(self, beatsPerMinute: int):

      ClockAbstract.__init__(self)
