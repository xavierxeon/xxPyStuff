#!/usr/bin/env python3

from .clock_abstract import MidiClockAbstract

class MidiClockInternal(MidiClockAbstract):

   def __init__(self, beatsPerMinute: int):

      MidiClockAbstract.__init__(self)
