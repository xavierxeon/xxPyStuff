#!/usr/bin/env python3

import sys

try:
   import todoist 
except ModuleNotFoundError:
   print('pip3 install --user  todoist-python')
   sys.exit()

from .settings import Settings

class Todoist(Settings, todoist.TodoistAPI):

   def __init__(self):

      Settings.__init__(self)
      todoist.TodoistAPI.__init__(self, self.getApiKey())
      self.sync()

   def save(self):

      try:
         self.commit()
      except todoist.SyncError as message:
         print(str(message))

   def getFullName(self):

      return self.state['user']['full_name']

   def getProjectId(self, projectName):

      if not projectName:
         return None

      # iterate over todoist.models.Project
      for project in self.state['projects']:
         if project['name'] == projectName:
               return project['id']

      return None

   def getSectionId(self, sectionName, projectId = None):

      for section in self.state['sections']:
         if section['name'] != sectionName:
            continue
         if projectId and section['project_id'] != projectId:
            continue
         return section['id']

      return None

   def iterProjectItems(self, projectId, sectionId = None):

      for item in self.state['items']:
         if item['project_id'] != projectId:
            continue
         if sectionId and item['section_id'] != sectionId:
            continue

         yield item
         
      return None

   def createProject(self, projectName):

      if not projectName:
         return None

      project = self.projects.add(projectName)
      return project['id']

   def createItem(self, text, projectId = None):

      item = self.items.add(text, project_id = projectId)
      return item

   def setItemDate(self, item, dateString):

      if not item or not dateString:
         return

      item['date_string'] = dateString
