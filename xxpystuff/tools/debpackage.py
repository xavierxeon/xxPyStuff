#!/usr/bin/env python3

import os
from subprocess import Popen, PIPE

from .console import Console

class DebianPackage:

    def __init__(self, path, name, version):

        self._path = path
        self._name = name
        self._version = version

        self.section = 'main'
        self.priority = 'optional'
        self.architecture = 'amd64'
        self.maintainer = 'Ralf Waspe <raw@mmmi.sdu.dk>'

        self.description = None
        self._dependencies = list()
        self._size = None

    def addDependencyList(self, text):

        for entry in  text.split(" "):
            if not entry:
                continue
            self._dependencies.append(entry)

    def create(self):

        self._calculateSize()
        if not self._writeControl():
            return

        current = os.getcwd()
        rootPath = self._path + '/..'
        contentDirName = os.path.basename(self._path)
        os.chdir(rootPath)
        
        with Popen(['dpkg-deb', '--build' , contentDirName], stdout = PIPE, stderr = PIPE) as process:
            output, error = process.communicate()

        if error:
            os.chdir(current)
            error = error.decode()
            print(Console.red(error))
            return        
        
        output = output.decode('ascii')
        print(Console.yellow(output))
        os.rename(contentDirName + '.deb', self._name + '-' + self._version + '.deb')    
        os.chdir(current)

    def _calculateSize(self):

        os.chdir(self._path)

        with Popen(['du', '-sk' , '.'], stdout = PIPE, stderr = PIPE) as process:
            output, error = process.communicate()
            output = output.decode('ascii')
            output = output.replace('.', '').strip()
            self._size = int(output)

    def _writeControl(self):

        if not os.path.exists(self._path):
            print(Console.red('PATH DOES NOT EXIST: ') + self._path)
            return False

        os.makedirs(self._path + '/DEBIAN', exist_ok = True)
        fileName = self._path + '/DEBIAN/control'

        with open(fileName, 'w') as outfile:
            outfile.write('Package: ' + self._name + '\n')
            outfile.write('Version: ' + self._version + '\n')
            outfile.write('Section: ' + self.section + '\n')
            
            outfile.write('Priority: ' + self.priority + '\n')
            outfile.write('Architecture: ' + self.architecture + '\n')
            outfile.write('Maintainer: ' + self.maintainer + '\n')

            outfile.write('Provides: ' + self._name + '\n')
            outfile.write('Conflicts: ' + self._name + '\n')
            outfile.write('Replaces: ' + self._name + '\n')

            outfile.write('Installed-Size: ' + str(self._size) + '\n')

            if self._dependencies:
                dependencyText = ", ".join(self._dependencies)
                outfile.write('Depends: ' + dependencyText + '\n')

            if self.description:
                outfile.write('Description: ' + self.description + '\n')
                            
        return True
