#!/usr/bin/env python3

import os, json, sys
import platform

from pathlib import Path
from subprocess import Popen, PIPE

class Dropbox:

   @staticmethod
   def getPath():

      on_wsl = platform.system() == 'Linux' and 'microsoft' in platform.uname().release
      on_windows = platform.system() == 'Windows'

      home = str(Path.home())
      infoPath = home + '/.dropbox/info.json'

      if on_wsl:
         command = ['cmd.exe', '/c' , 'echo',  '%USERNAME%']
         with Popen(command, stdout = PIPE, stderr = PIPE) as process:
            output, _ = process.communicate()      
            user = output.decode().strip()    
         home = '/mnt/c/Users/' + user 
         infoPath = home + '/AppData/Local/Dropbox/info.json'

      if on_windows:
         infoPath = home + '/AppData/Local/Dropbox/info.json'

      #print(home)

      if not os.path.exists(infoPath):
         print('no dropbox folder')
         sys.exit(1)

      with open(infoPath, 'r') as infile:
         dropbox = json.load(infile)

      if not 'personal' in dropbox:
         sys.exit(1)

      if not 'path' in dropbox['personal']:
         sys.exit(1)

      path = dropbox['personal']['path']

      if on_wsl:
         path = path.replace('\\', '/')
         command = ['wslpath', '-a', path]
         with Popen(command, stdout = PIPE, stderr = PIPE) as process:
            output, _ = process.communicate()      
            path = output.decode().strip()    

      path = path + '/'
      return path

if __name__ == '__main__':

   path = Dropbox.getPath()
   print(path)
