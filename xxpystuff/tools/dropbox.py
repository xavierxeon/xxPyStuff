#!/usr/bin/env python3

import os, json, sys
import platform

from pathlib import Path

class Dropbox:

   @staticmethod
   def getPath():

      home = str(Path.home())
      infoPath = home + '/.dropbox/info.json'
      if platform.system() == 'Windows':
         infoPath = home + '/AppData/Local/Dropbox/info.json'
      if not os.path.exists(infoPath):
         print('no dropbox folder')
         sys.exit(1)

      with open(infoPath, 'r') as infile:
         dropbox = json.load(infile)

      if not 'personal' in dropbox:
         sys.exit(1)

      if not 'path' in dropbox['personal']:
         sys.exit(1)

      path = dropbox['personal']['path'] + '/'
      return path
