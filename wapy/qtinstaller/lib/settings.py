#!/usr/bin/env python3

import sys

from ...tools import JSONSettings

class Settings(JSONSettings):

    _template = {
        'executables': {
            'qt_installer': '',
            'repogen': '', 
            '7zip': ''
        }
    }
    _fileName = 'config.qtinstaller.json'

    def __init__(self):

        JSONSettings.__init__(self, Settings._fileName, Settings._template)
        try:
            self.load()
        except JSONSettings.SettingsError as message:
            print(message)
            sys.exit(1)
