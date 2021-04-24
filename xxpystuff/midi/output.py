#!/usr/bin/env python3

from rtmidi import MidiOut
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF

class MidiOutput:

   def __init__(self, name = None, port = None):

      self.midiout = MidiOut()
      if port:
         portNames = self.midiout.get_ports()
         if len(portNames) <= port:
            raise ValueError
         print('real output', port, portNames[port])
         self.midiout.open_port(port)
         if not self.midiout.is_port_open():
            print('not open')
      else:
         print('virtual output', name)
         self.midiout.open_virtual_port(name)         

   def __del__(self):

      print('close port')
      self.midiout.close_port()
      del self.midiout # to remove virtual port

   def noteOn(self, channel, pitch, velocity):

      pass

   def noteOff(self, channel, pitch):

      pass

   @staticmethod
   def available():

      return MidiOut().get_ports()