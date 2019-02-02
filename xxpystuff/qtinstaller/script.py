#!/usr/bin/env python3

import os, random, string

class Script:

    class Shurtcut:

        def __init__(self, target, name):

            self.args = None
            self.workinDirectory = '@TargetDir@'
            self.desription = None

            self._target = '@TargetDir@/' + target
            self._link = '@StartMenuDir@/' + name + '.lnk'

        def createOpertaion(self):

            operation = '"CreateShortcut"'
            operation += ', "' + self._target+ '"'
            operation += ', "' + self._link + '"'
            if self.args:
                operation += ', "' + self.args + '"'
            operation += ', "workingDirectory=' + self.workinDirectory+ '"'
            if self.desription:
                operation += ', "description=' + self.desription + '"'
            return operation

    def __init__(self, package):

        package._script = self
        self.name = package._key.replace('.', '_') + '_installscript.qs'
        self._shortcutList = list()

    def addShortcut(self, target, name):

        shortcut = Script.Shurtcut(target, name)
        self._shortcutList.append(shortcut)
        return shortcut

    def save(self, targetDir):

        newLine = '\n'
        content = 'function Component() { }' + newLine + newLine
        content += 'Component.prototype.createOperations = function()' + newLine
        content += '{' + newLine
        content += '    component.createOperations();' + newLine
        content += '    if (systemInfo.productType === "windows")' + newLine
        content += '    {' + newLine

        for shortcut in self._shortcutList:
            content += '        component.addOperation(' + shortcut.createOpertaion() + ');' + newLine
        
        content += '    }' + newLine
        content += '}' + newLine

        fileName = targetDir + '/' + self.name
        with open(fileName, 'w') as scriptfile:
            scriptfile.write(content)
