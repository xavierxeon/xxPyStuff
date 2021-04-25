#!usr/bin/env python3

from .timecode import TimeCode
from .note import Note

class Sequencer:

   def __init__(self, clock, output):

      clock.onPositionChange(self._songPostion)

      self._output = output

      self._noteOnMap = dict()
      self._noteOnPositions = list()
      self._noteOffMap = dict()
      self._noteOffPositions = list()

      self._finsihedCallbackList = list()

   def addNote(self, startTimeCode, note, channel):
      
      def addEvent(position, eventMap):
         if not position in eventMap:
            eventMap[position] = list()

         eventList = eventMap[position]
         eventList.append( [note, channel] )

         orderList = list(eventMap.keys())
         orderList.sort()
         return orderList

      startPosition = startTimeCode.position()
      self._noteOnPositions = addEvent(startPosition, self._noteOnMap)

      endPosition = startPosition + note.duration
      self._noteOffPositions = addEvent(endPosition, self._noteOffMap)      

   def onFinished(self, callback):

      self._finsihedCallbackList.append(callback) 

   def _songPostion(self, position):

      lastOn = 0 if not self._noteOnPositions else self._noteOnPositions[-1] 
      lastOff = 0 if not self._noteOffPositions else self._noteOffPositions[-1]

      if position > lastOn and position > lastOff:
         for callback in self._finsihedCallbackList:
            callback()
         return
      
      if position in self._noteOffMap:
         for entry in self._noteOffMap[position]:
            self._output.noteOff(entry[1], entry[0].pitch)

      if position in self._noteOnMap:
         for entry in self._noteOnMap[position]:
            self._output.noteOn(entry[1], entry[0].pitch, entry[0].velocity)
