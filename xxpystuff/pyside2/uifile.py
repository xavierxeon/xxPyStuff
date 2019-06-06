#!/usr/bin/env python3

import os, subprocess, platform
from pathlib import Path

class UiFile:

    @staticmethod
    def makePythonFile(uiFile, pythonFile):

        import PySide2.QtCore
        path = os.path.dirname(PySide2.QtCore.__file__)
        if 'Windows' == platform.system():
            uiExe = path + '\\pyside2-uic.exe'
        else:
            uiExe = str(Path.home()) + '/.local/bin/pyside2-uic'

        if not os.path.exists(uiExe):
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

