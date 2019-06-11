#!/usr/bin/env python3

import os
from subprocess import Popen, PIPE, TimeoutExpired

class Process:

    def __init__(self, command, statusIndicator = None):

        self.workDir = None
        self.outputFunction = None
        self.errorFunction = None

        self._command = command
        self._statusIndicator = statusIndicator
        self._handle = None

    def start(self, *argList):

        current = os.getcwd()
        if self.workDir:
            os.chdir(self.workDir)

        content = [ self._command ]
        for arg in argList:
            content.append(str(arg))

        self._handle = Popen(content, stdout = PIPE, stderr = PIPE, stdin = PIPE, bufsize = 1, universal_newlines = True)
        success = False
        while True:
            try:
                output, error = self._handle.communicate(None, 0.2)

                # timeout not reached, therefore process is finished
                if output and self.outputFunction:
                    self.outputFunction(output)
                if error and self.errorFunction:
                    self.errorFunction(error)
                if not error:
                    success = True
                break 
            except TimeoutExpired:
                if self._statusIndicator:
                    self._statusIndicator.busy()

        self.stop()
        os.chdir(current)

        return success

    def stop(self):

        if not self._handle:
            return

        self._handle.kill()

        del self._handle
        self._handle = None

    def write(self, text):

        pass

    @staticmethod
    def execute(command, workDir = None):

        current = os.getcwd()
        if workDir:
            os.chdir(workDir)

        with Popen(command, stdout = PIPE, stderr = PIPE) as process:
            output, error = process.communicate()

        os.chdir(current)

        if error:
            return error.decode('ascii')
        else:
            return output.decode('ascii')
            
    def _capture(self, pipe, callBack):
        
        if not callBack:
            return

        while True:
            output = pipe.read()
            if not output:
                return
            callBack(output)
