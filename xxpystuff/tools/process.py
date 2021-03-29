#!/usr/bin/env python3

import os
from subprocess import Popen, PIPE, TimeoutExpired

# On modern Python versions you can do capture_output=True instead of stdout=subprocess.PIPE. – Boris Feb 18 at 23:27

class Process:

   def __init__(self, command, statusIndicator = None):

      self.workDir = None
      self.output = None
      self.error = None

      self._command = command
      self._statusIndicator = statusIndicator
      self._handle = None

   def startWithArguments(self, *arguments):

      content = [ self._command ]
      for arg in arguments:
         content.append(str(arg))

      return self._executeInternal(content)

   def start(self, argList = None):

      content = [ self._command ]
      if argList:
         for arg in argList:
               content.append(str(arg))

      return self._executeInternal(content)

   def stop(self):

      if not self._handle:
         return

      self._handle.kill()

      del self._handle
      self._handle = None

   def write(self, text):

      pass

   @staticmethod
   def execute(command, workDir = None, statusIndicator = None):

      current = os.getcwd()
      if workDir:
         os.chdir(workDir)

      output = None
      error = None

      if not statusIndicator:
         with Popen(command, stdout = PIPE, stderr = PIPE) as process:
            output, error = process.communicate()
      else:
         with Popen(command, stdout = PIPE, stderr = PIPE, stdin = PIPE, bufsize = 1, universal_newlines = True) as process:
            while True:
               try:
                  output, error = process.communicate(None, 0.2)
                  break 
               except TimeoutExpired:
                  statusIndicator.busy()

      os.chdir(current)

      if error:
         return error
      elif output:
         return output
      else:
         return None
         
   def _executeInternal(self, content):

      current = os.getcwd()
      if self.workDir:
         os.chdir(self.workDir)

      self._handle = Popen(content, stdout = PIPE, stderr = PIPE, stdin = PIPE, bufsize = 1, universal_newlines = True)
      success = False
      while True:
         try:
            self.output, self.error = self._handle.communicate(None, 0.2)
            success = True
            break 
         except TimeoutExpired:
            if self._statusIndicator:
               self._statusIndicator.busy()

      self.stop()
      os.chdir(current)

      return success
