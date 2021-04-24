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

         orderList = list(self._noteOnMap.keys())
         orderList.sort()
         return orderList

      startPosition = startTimeCode.position()
      self._noteOnPositions = addEvent(startPosition, self._noteOnMap)

      endPosition = startPosition + note.duration
      self._noteOffPositions = addEvent(endPosition, self._noteOffMap)      

   def onFinished(self, callback):

      self._finsihedCallbackList.append(callback) 

   def _songPostion(self, position):

      if position > self._noteOnPositions[-1] and position > self._noteOffPositions[-1]:
         for callback in self._finsihedCallbackList:
            callback()
         return
      
      if position in self._noteOffMap:
         for entry in self._noteOffMap[position]:
            print('off', entry[0], entry[1])

      if position in self._noteOnMap:
         for entry in self._noteOnMap[position]:
            print('on', entry[0], entry[1])
