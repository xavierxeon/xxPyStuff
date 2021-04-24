#!/usr/bin/env python3

class MidiClockAbstract:

   class State:

      Stop = 0
      Start = 1
      Continue = 2    

      names = {
         Stop: 'Stop',
         Start: 'Start',
         Continue: 'Continue'
      }

   def __init__(self):

      self.state = MidiClockAbstract.State.Stop
      self.position = 1

      self._stateCallbackList = list()
      self._positionCallbackList = list()      
      self._tickCounter = 0

      self._last_time = None

   def onStateChange(self, callback):

      self._stateCallbackList.append(callback)

   def onPositionChange(self, callback):

      self._positionCallbackList.append(callback)

   @staticmethod
   def timeCode(position):

      if position <= 0:
         return None

      position -= 1

      back = position % 4   
      mid = ((position - back) / 4) % 4
      front = (((position - back) / 4) - mid) / 4

      return [int(front) + 1, int(mid) + 1, int(back) + 1]

   def _setState(self, state):

      self.state = state
      for callback in self._stateCallbackList:
         callback(state)

   def _clockTick(self):

      self._tickCounter += 1

      if self._tickCounter >= 6:
         self._setSongPosition(self.position + 1)

   def _setSongPosition(self, position):

      self.position = position
      self._tickCounter = 0

      for callback in self._positionCallbackList:
         callback(position)      
