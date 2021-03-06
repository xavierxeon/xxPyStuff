#!/usr/bin/env python3

import math

from .console import Console

class UserInteraction:

   def __init__(self, title):

      self.title = title
      self.location = None
      self.choices = dict()
      self.content = list()

   def addChoice(self, key, text):

      self.choices[key] = text

class StatusIndicatorAbstract:
   
   def __init__(self):

      self._progressText = str()

   def setProgressText(self, text):

      self._progressText = text

   def message(self, text):

      raise NotImplementedError

   def busy(self):

      raise NotImplementedError

   def progress(self, count, maxCount):

      raise NotImplementedError

   def endProgress(self, trailer = None):

      raise NotImplementedError

   def askUser(self, userInteraction):

      raise NotImplementedError

class StatusIndicatorConsole(StatusIndicatorAbstract):

   class Wrapper:

      def __init__(self, indicator, message):

         if not indicator:
               self._indicator = StatusIndicatorConsole()
         else:
               self._indicator = indicator

         self._indicator.setProgressText(message)
         self._indicator.progress(0, 10)

      def __del__(self):

         self._indicator.endProgress(Console.green('done'))

      def progress(self, count, maxCount):

         self._indicator.progress(count, maxCount)

   def busy(self):

      self._indicator.busy()

   def __init__(self):

      StatusIndicatorAbstract.__init__(self)

      self._segments = 0
      self._lastTest = -1
   
   def message(self, text):

      print(text)

   def busy(self):

      front = ' ' * self._segments
      back = ' ' * (10 - (self._segments + 1))
      message = Console.white('[{0}#{1}]', True).format(front, back)

      self._segments += 1
      if self._segments >= 10:
         self._segments = 0

      message += Console.yellow(' ?.? %')

      if self._progressText:
         message += ' {0}'.format(self._progressText)

      print('\r' + message, end = '', flush = True)            

   def progress(self, count, maxCount):

      percent = 100 * count / maxCount
      if count >= maxCount:
         self._segments = 10
      else:
         self._segments = math.floor(percent / 10)
         test = int(percent * 10)
         if test == self._lastTest:
               return
         else:
               self._lastTest = test
      
      done = '#' * self._segments
      remain = '_' * (10 - self._segments)
      message = Console.white('[{0}{1}]', True).format(done, remain)
      message += Console.yellow(' {0:.1f} %').format(percent)
      if self._progressText:
         message += ' {0}'.format(self._progressText)

      print('\r' + message, end = '', flush = True)            

   def endProgress(self, trailer = None):

      self.progress(10, 10)

      self._progressText = None
      self._segments = 0
      self._lastTest = -1
      
      if trailer:
         print(' ' + trailer, flush = True)
      else:
         print('' , flush = True)

   def askUser(self, userInteraction):

      if userInteraction.location:
         print(Console.yellow(userInteraction.title) + ': ' + userInteraction.location)
      else:
         print(Console.yellow(userInteraction.title))
      
      for text in userInteraction.content:
         print('* ' + text)
   
      for key, text in userInteraction.choices.items():
         print('type "{0}": {1}'.format(Console.yellow(key), text))

      userInput = input('your choice: ')
      return userInput
