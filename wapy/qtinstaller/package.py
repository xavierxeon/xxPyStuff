#!/usr/bin/env python3

import os

from fnmatch import fnmatch
from datetime import date

import xml.etree.ElementTree as xmlfile
from shutil import copy, rmtree

from ..tools import XMLTools, Process, Console, SimpleProgresIndicator

class Package:
    
    def __init__(self, installer, name, subKey, version = None):

        installer._packageList.append(self)
        self._installer = installer
        self.name = name 
        self._key = installer._key + '.' + subKey

        self._data = {
            'Name': self._key,
            'Version': version if version else '1.0',
            'Default': 'true',
            'ReleaseDate': str(date.today())
        }

        self._script = None

        self._metaDir = 'installer/packages/' + self._key + '/meta'
        self._dataDir = 'installer/packages/' + self._key + '/data'

    def copyFiles(self, targetDir):

        raise NotImplementedError()        

    @staticmethod
    def copyWildCard(sourceDir, targetDir, wildcard, progressBar = None, recursive = False):
        
        copyList = dict()
        
        def fillCoppyListRecursive(sourceDir, targetDir):
            os.makedirs(targetDir, exist_ok = True)
            for entry in os.scandir(sourceDir):
                if recursive and entry.is_dir():
                    fillCoppyListRecursive(entry.path, targetDir + '/' + entry.name)
                    continue
                if entry.is_file() and  fnmatch(entry.name, wildcard):
                    copyList[entry.path] = targetDir

        fillCoppyListRecursive(sourceDir, targetDir)

        count = len(copyList)
        index = 0

        for fileName, targetDir in copyList.items():
            index += 1
            if progressBar:
                progressBar(index, count)
            else:
                print(fileName, targetDir)           
            copy(fileName, targetDir)           

    def setDefault(self, default):

        self._data['Default'] = 'true' if default else 'false'

    def setDisplayName(self, name):

        self._data['DisplayName']  = name

    def getContentDirName(self):

        dirName = self.name.replace(' ', '')
        return dirName

    def _createMeta(self):

        os.makedirs(self._metaDir, exist_ok = True)

        root = xmlfile.Element('Package')

        for key, value in self._data.items():
            xmlfile.SubElement(root, key).text = value    

        if self._script:
             xmlfile.SubElement(root, 'Script').text = self._script.name    
             self._script.save(self._metaDir)

        XMLTools.indent(root)        
        with open(self._metaDir + '/package.xml', 'wb') as outfile:
            content = xmlfile.tostring(root, encoding='utf8')
            outfile.write(content)

    def _startCopyFiles(self):

        os.makedirs(self._dataDir + '/' + self.getContentDirName(), exist_ok = True)
        self.copyFiles(os.getcwd() + '/' + self._dataDir + '/' + self.getContentDirName())

    def _zipContent(self):

        p = SimpleProgresIndicator('compressing')            
        command = [self._installer.get7ZipExe(), 'a', 'Content.7z', self.getContentDirName() + '/*']
        output = Process.execute(command, self._dataDir)

        del p
        if output:
            print(Console.grey(output))

    def _cleanup(self):

        SimpleProgresIndicator('clean up')
        rmtree(self._dataDir + '/' + self.getContentDirName())
