#!/usr/bin/env python3

from threading import Timer

from .clock_abstract import ClockAbstract

class ClockInternal(ClockAbstract):

   def __init__(self, beatsPerMinute: int):

      ClockAbstract.__init__(self)
      self.beatsPerMinute = beatsPerMinute

      self._timer = None

   def __del__(self):

      if self._timer:
         self._timer.cancel()

   def start(self):

      self._setState(ClockAbstract.State.Start)
      self._setSongPosition(1) 
      self._nextTimer()

   def stop(self):

      self._setState(ClockAbstract.State.Stop)
      if self._timer:
         self._timer.cancel()
         self._timer = None

   def reset(self):

      if self._timer:
         self._timer.cancel()
         self._timer = None

      self._setSongPosition(1)      

   def _nextTimer(self):

      if self.state != ClockAbstract.State.Start:
         return

      secondsPerTick = 2.5 / self.beatsPerMinute

      self._timer = Timer(secondsPerTick, self._timeout)
      self._timer.start()

   def _timeout(self):

      self._clockTick()
      self._nextTimer()
