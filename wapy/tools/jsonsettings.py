#!/usr/bin/env pythin3

import os, json

from .console import Console

class JSONSettings:

    class SettingsError(Exception):

        pass

    def __init__(self, fileName, template):

        self._fileName = fileName
        self._template = template
        self._data = dict()

    def load(self, abortIfFileNotExist = True):

        if not os.path.exists(self._fileName):
            with open(self._fileName, 'w') as output:
                json.dump(self._template, output, indent = 4)
            if abortIfFileNotExist:
                self._abort('please edit the values')

        with open(self._fileName, 'r') as infile:
            self._data = json.load(infile)

        self._sanityCheck()  

    def save(self):

        with open(self._fileName, 'w') as outfile:
            json.dump(self._data, outfile)

    def _abort(self, message):

        message = Console.red('{0} in settings file ').format(message) + Console.magenta('{0}').format(self._fileName)
        raise JSONSettings.SettingsError(message) 

    def _sanityCheck(self):

        def compileKeyList(dictionary):

            keyList = list()
            for key, value in dictionary.items():
                keyList.append(key)
                if isinstance(value, dict):
                    for subKey in compileKeyList(value):
                        keyList.append(key + '/' + subKey)
            return keyList

        templateKeyList = compileKeyList(self._template)
        dataKeyList = compileKeyList(self._data)

        missingList = list()

        for key in templateKeyList:
            if not key in dataKeyList:
                missingList.append(key)

        if missingList:
            if len(missingList) is 1:
                missing = missingList[0]
            elif len(missingList) > 1:
                missing = '", "'.join(missingList)
            self._abort('entry "{0}" is missing'.format(missing))
            
                       