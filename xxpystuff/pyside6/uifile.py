#!/usr/bin/env python3

import sys, os, subprocess, platform
from pathlib import Path

class UiFile:

    @staticmethod
    def makePythonFile(uiFile, pythonFile):

        def findUiExe():

            if 'Windows' == platform.system():
                for path in sys.path:
                    if not 'site-packages' in path: 
                        continue
                    path = path.replace('site-packages', 'Scripts')
                    if not os.path.exists(path):
                        continue
                    return path + '\\pyside6-uic.exe'
            else:
                return str(Path.home()) + '/.local/bin/pyside6-uic'

            return None

        uiExe = findUiExe()
        if not uiExe or not os.path.exists(uiExe):
            print('can not find file ui exe:', uiExe)
            return

        if os.path.exists(pythonFile):
            os.remove(pythonFile)

        command = (uiExe, uiFile , '-o' , pythonFile)
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                output, error = process.communicate()
        
        if output:
            print('OUTPUT')
            for line in output.decode().split('\n'):
                print(line)

        if error:
            print('ERROR')
            for line in error.decode().split('\n'):
                print(line)    

