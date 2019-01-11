#!/usr/bin/env python3

import os, sys

import xml.etree.ElementTree as xmlfile
from shutil import copy

from ..tools import XMLTools, JSONSettings, Process, Console, SimpleProgresIndicator
from .package import OnlineDummyPackage

class Installer(JSONSettings):

    _template = {
        'executables': {
            'qt_installer': '',
            'repogen': '', 
            '7zip': ''
        }
    }
    _fileName = 'config.json'

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
        self._name = name

        # config data
        self._configData = { 
            'Name': name,
            'Version': version if version else '1.0'
        }
        self._remoteRepoList = list()

    def create(self):

        for package in self._packageList:
            print(Console.blue('Package: ') + package.name)
            package.create()
            if self._remoteRepoList:
                package.updateRepository()

        self._createConfig()   
        self._createInstaller()

    def setTitle(self, title):

        self._configData['Title'] = title

    def setPublisher(self, publisher):

        self._configData['Publisher'] = publisher

    def setStartMenuDir(self, name):

        self._configData['StartMenuDir'] = name

    def setMaintenanceToolName(self, name):

        self._configData['MaintenanceToolName'] = name

    def setHomeDirTarget(self, relLocation):

        self._configData['TargetDir'] = '@HomeDir@/' + relLocation

    def setInstallerApplicationIcon(self, iconFile):

        os.makedirs('installer/config', exist_ok = True)
        copy(iconFile, 'installer/config')
        
        suffix = os.path.splitext(iconFile)[1]
        name = os.path.basename(iconFile).replace(suffix, '')
        
        self._configData['InstallerApplicationIcon'] = name

    def addRemoteRepository(self, url):

        if not self._remoteRepoList:
            OnlineDummyPackage(self)

        self._remoteRepoList.append(url)

    def get7ZipExe(self):

        return self.data['executables']['7zip']

    def _createConfig(self):

        os.makedirs('installer/config', exist_ok = True)

        root = xmlfile.Element('Installer')

        for key, value in self._configData.items():
            xmlfile.SubElement(root, key).text = value     

        if self._remoteRepoList:
            repos = xmlfile.SubElement(root, 'RemoteRepositories')
            for repoUrl in self._remoteRepoList:
                repo = xmlfile.SubElement(repos, 'Repository')
                xmlfile.SubElement(repo, 'Url').text = repoUrl               
                xmlfile.SubElement(repo, 'Enabled').text = '1'

        XMLTools.indent(root)        
        with open('installer/config/config.xml', 'wb') as outfile:
            content = xmlfile.tostring(root, encoding='utf8')
            outfile.write(content)

    def _createInstaller(self):

        name = self._name
        if 'MaintenanceToolName' in self._configData:
            name = self._configData['MaintenanceToolName']

        if self._remoteRepoList:
            p = SimpleProgresIndicator('create online installer')
            command = [self.data['executables']['qt_installer'], '-c', 'config/config.xml', '-p', 'packages', '-n', name + '.exe']
        else:
            p = SimpleProgresIndicator('create offline installer')
            command = [self.data['executables']['qt_installer'], '--offline-only', '-c', 'config/config.xml', '-p', 'packages', name + '.exe']
            
        output =  Process.execute(command, 'installer')

        del p
        if output:
            print(Console.grey(output))

