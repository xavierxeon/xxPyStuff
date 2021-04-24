#!/usr/bin/env python3

class ClockAbstract:

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

      self.stateCallbackList = list()
      self.state = ClockAbstract.State.Stop

      self.positionCallbackList = list()      
      self.position = 1

      self._tickCounter = 0

   def addStateCallBack(self, callback):

      self.stateCallbackList.append(callback)

   def addPositionCallBack(self, callback):

      self.positionCallbackList.append(callback)

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
      for callback in self.stateCallbackList:
         callback(state)

   def _clockTick(self):

      self._tickCounter += 1

      if self._tickCounter >= 6:
         self._setSongPosition(self.position + 1)

   def _setSongPosition(self, position):

      self.position = position
      self._tickCounter = 0

      for callback in self.positionCallbackList:
         callback(position)      
