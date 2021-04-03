#!/usr/bin/env python3

import os, sys, json

from pathlib import Path
from xxpystuff.tools import JSONSettings, Console

class Settings(JSONSettings):

   _fileName = str(Path.home()) + '/.todoist_cli.json'
   _template = { 'apikey': ''}

   def __init__(self):

      JSONSettings.__init__(self, Settings._fileName, Settings._template)
      try:
         self.load()
      except JSONSettings.SettingsError as message:
         print('get api token from todoist app -> settings -> integration -> api token ')
         print(str(message))
         sys.exit(1)

   def getApiKey(self):

      return self.data['apikey']

   def getCurrentDirectoryProjectName(self):

      path = os.getcwd()
      
      while True:
         fileName = path + '/todoist.project.json'
         if os.path.exists(fileName):
               break
         newpath = os.path.realpath(path + '/..')
         if newpath == path:
               return None
         path = newpath
         
      with open(fileName, 'r') as infile:
         content = json.load(infile)
               
      if not 'project' in content:
         return None

      return content['project']
