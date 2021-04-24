#!usr/bin/env python3

from rtmidi import MidiIn
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF, SYSTEM_EXCLUSIVE

class Input:

   def __init__(self, name = None, port = None):

      self.midiin = MidiIn()
      if port:
         portNames = self.midiin.get_ports()
         if len(portNames) <= port:
            raise ValueError
         print('real input', port, portNames[port])
         self.midiin.open_port(port)
         if not self.midiin.is_port_open():
            print('not open')
      else:
         print('virtual input', name)
         self.midiin.open_virtual_port(name)         

      self.midiin.set_callback(self._callback)

   def __del__(self):

      self.midiin.close_port()

   @staticmethod
   def available():

      return MidiIn().get_ports()

   def _callback(self, event, data):

      message,_ = event
      midiEvent = message[0] & SYSTEM_EXCLUSIVE
      if midiEvent == NOTE_ON:
         status, note, velocity = message
         channel = (status & 0x0F) + 1
         print('note on', channel, note, velocity)
      elif midiEvent == NOTE_OFF:
         status, note, velocity = message
         channel = (status & 0x0F) + 1
         print('note off', channel, note, velocity)
