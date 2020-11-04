#!/usr/bin/env pythin3

import os, json

from .console import Console

class JSONSettings:

    class SettingsError(Exception):

        pass

    def __init__(self, fileName, template, removeUnknownKeys = True):

        self._fileName = fileName
        self._template = template
        self._removeUnknownKeys = removeUnknownKeys
        self.data = dict()

    def load(self, abortIfFileNotExist = True):

        if not os.path.exists(self._fileName):
            with open(self._fileName, 'w') as output:
                json.dump(self._template, output, indent = 4)
                self.data = self._template
            if abortIfFileNotExist:
                self._abort('please edit the values')
        else:
            with open(self._fileName, 'r') as infile:
                self.data = json.load(infile)

            if self._sanityCheck(self._template, self.data):
                self.save()

    def save(self):

        with open(self._fileName, 'w') as outfile:
            json.dump(self.data, outfile, indent = 4)

    def _abort(self, message):

        message = Console.red('{0} in settings file ').format(message) + Console.magenta('{0}').format(self._fileName)
        raise JSONSettings.SettingsError(message) 

    def _sanityCheck(self, source, target):

        madeChanges = False

        #remove extra entries
        if self._removeUnknownKeys:
            removeKeys = list()
            for key in target.keys():
                if not key in source:
                    removeKeys.append(key)

            for key in removeKeys:
                del target[key]
                madeChanges = True

        # add missing entries
        for key, value in source.items():
            if not key in target:
                target[key] = value
                madeChanges = True
            #recurse into sub dictionaries
            if isinstance(value, dict):
                if self._sanityCheck(source[key], target[key]):
                    madeChanges = True
            
        return madeChanges
                       