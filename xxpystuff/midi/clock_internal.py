#!/usr/bin/env python3

from threading import Timer

from .clock_abstract import MidiClockAbstract

class MidiClockInternal(MidiClockAbstract):

   def __init__(self, beatsPerMinute: int):

      MidiClockAbstract.__init__(self)
      self.beatsPerMinute = beatsPerMinute

      self._timer = None

   def __del__(self):

      if self._timer:
         self._timer.cancel()

   def start(self):

      self._setState(MidiClockAbstract.State.Start)
      self._nextTimer()

   def stop(self):

      self._setState(MidiClockAbstract.State.Stop)
      if self._timer:
         self._timer.cancel()
         self._timer = None

   def reset(self):

      if self._timer:
         self._timer.cancel()
         self._timer = None

      self._setSongPosition(1)      

   def _nextTimer(self):

      secondsPerTick = 2.5 / self.beatsPerMinute

      self._timer = Timer(secondsPerTick, self._timeout)
      self._timer.start()

   def _timeout(self):

      self._clockTick()
      self._nextTimer()
