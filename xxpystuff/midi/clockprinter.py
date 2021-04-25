#!/usr/bin/env python3

from .clock_abstract import ClockAbstract
from .timecode import TimeCode

class ClockPrinter:

   def __init__(self, clock):

      clock.onStateChange(self.stateChange)
      clock.onPositionChange(self.songPostion)

      self._lastBar = 0
      self._lastQuarter = 0
   
   def stateChange(self, state: ClockAbstract.State):

      print(ClockAbstract.State.names[state])

   def songPostion(self, position):

      timeCode = TimeCode.fromPosition(position)
      if timeCode.quarter != self._lastQuarter:
         print(timeCode)
         self._lastQuarter = timeCode.quarter