#!/usr/bin/env python3

from .clock_internal import ClockInternal
from .clockprinter import ClockPrinter
from .sequencer import Sequencer

import time

class Performance:

   def __init__(self, bpm, output, clock = None):

      self.masterClock = clock if clock else ClockInternal(bpm)
      self.sequencer = Sequencer(self.masterClock, output)

      self._running = False
      self._clockPrinter = None
      self.sequencer.onFinished(self._finshed)

   def addNote(self, startTimeCode, note, channel):      

      self.sequencer.addNote(startTimeCode, note, channel)       

   def printClock(self, resolution = ClockPrinter.Resolution.Quarter):

      if self._clockPrinter:
         del self._clockPrinter

      self._clockPrinter = ClockPrinter(self.masterClock, resolution)

   def run(self):  

      self._running = True

      try:
         self.masterClock.start()
         while self._running:
            time.sleep(2)    # time here does not matter for clock timimg
      except KeyboardInterrupt:
         print()
         print('user interruption')
         pass
      finally:
         self.masterClock.stop()            

   def _finshed(self):

      self._running = False