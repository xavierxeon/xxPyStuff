#!/usr/bin/env python3

from .clock_internal import ClockInternal
from .clockprinter import ClockPrinter
from .sequencer import Sequencer

import time

class Performance:

   def __init__(self, bpm, output, clock = None):

      self.masterClock = clock if clock else ClockInternal(bpm)
      ClockPrinter(self.masterClock)

      self.sequencer = Sequencer(self.masterClock, output)

      self._running = False
      self.sequencer.onFinished(self._finshed)

   def addNote(self, startTimeCode, note, channel):      

      self.sequencer.addNote(startTimeCode, note, channel)           

   def run(self):  

      self._running = True

      try:
         self.masterClock.start()
         while self._running:
            time.sleep(2)    # time here does not matter for clock timimg
      except KeyboardInterrupt:
         print()
         print('user interruption')
         self.sequencer._output.allNotesOff()
         pass
      finally:
         self.masterClock.stop()            

   def _finshed(self):

      self._running = False