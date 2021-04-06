#!/usr/bin/env python3

import sys

def printHelpToFile(cls, fileName):

   store_stdout = sys.stdout
   with open(fileName, 'w') as helpfile:
      sys.stdout = helpfile
      help(cls)
      sys.stdout = store_stdout
