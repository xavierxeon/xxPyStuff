#!/usr/bin/env python3

from rtmidi.midiconstants import SONG_POSITION_POINTER, TIMING_CLOCK, SONG_START, SONG_CONTINUE, SONG_STOP, SYSTEM_EXCLUSIVE

from .clock_abstract import MidiClockAbstract
from .intput import MidiInput

class MidiClockExternal(MidiClockAbstract, MidiInput):

   def __init__(self, name = None, port = None):

      MidiClockAbstract.__init__(self)
      print('clock')
      MidiInput.__init__(self, name, port)
      self.midiin.ignore_types(timing = False)
      
   def _callback(self, event, data):

      message,_ = event
      midiEvent = message[0] 
      if midiEvent == SONG_POSITION_POINTER:
         front = message[1]
         back = message[2]
         position = 1 + front + (128 * back)
         self._setSongPosition(position)
      elif midiEvent == TIMING_CLOCK:
         self._clockTick() 
      elif midiEvent == SONG_START:
         self._setState(MidiClockAbstract.State.Start)
      elif midiEvent == SONG_CONTINUE:
         self._setState(MidiClockAbstract.State.Continue)
      elif midiEvent == SONG_STOP:
         self._setState(MidiClockAbstract.State.Stop)

