#!/usr/bin/env python3

import os, sys

import xml.etree.ElementTree as xmlfile

from ..tools import XMLTools, JSONSettings

class Installer(JSONSettings):

    _template = {
        'executables': {
            'qt_installer': '',
            'repogen': '', 
            '7zip': ''
        }
    }
    _fileName = 'config.qtinstaller.json'

    def __init__(self, name, key, version = None):

        JSONSettings.__init__(self, Installer._fileName, Installer._template)
        try:
            self.load()
        except JSONSettings.SettingsError as message:
            print(message)
            sys.exit(1)

        # general data
        self._packageList = list()
        self._key = key

        # config data
        self._data = { 
            'Name': name,
            'Version': version if version else '1.0'
        }
        self._remoteRepoList = list()

    def create(self):

        self._createConfig()
        for package in self._packageList:
            package._createMeta()
            package._startCopyFiles()
            package._zipAndRemoveContent()

    def setTitle(self, title):

        self._data['Title'] = title

    def setPublisher(self, publisher):

        self._data['Publisher'] = publisher

    def setStartMenuDir(self, name):

        self._data['StartMenuDir'] = name

    def setMaintenanceToolName(self, name):

        self._data['MaintenanceToolName'] = name

    def setHomeDirTarget(self, relLocation):

        self._data['TargetDir'] = '@HomeDir@/' + relLocation

    def addRemoteRepository(self, url):

        self._remoteRepoList.append(url)

    def get7ZipExe(self):

        return self.data['executables']['7zip']

    def _createConfig(self):

        os.makedirs('installer/config', exist_ok = True)

        root = xmlfile.Element('Installer')

        for key, value in self._data.items():
            xmlfile.SubElement(root, key).text = value     

        if self._remoteRepoList:
            repos = xmlfile.SubElement(root, 'RemoteRepositories');
            for repoUrl in self._remoteRepoList:
                repo = xmlfile.SubElement(repos, 'Repository')
                xmlfile.SubElement(repo, 'Url').text = repoUrl               
                xmlfile.SubElement(repo, 'Enabled').text = '1'

        XMLTools.indent(root)        
        with open('installer/config/config.xml', 'wb') as outfile:
            content = xmlfile.tostring(root, encoding='utf8')
            outfile.write(content)
