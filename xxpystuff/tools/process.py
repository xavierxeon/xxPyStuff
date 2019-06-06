#!/usr/bin/env python3

import os
from subprocess import Popen, PIPE

class Process:

    def __init__(self, command):

        self.workDir = None
        self.outputFunction = None
        self.errorFunction = None

        self._command = command
        self._handle = None

    def start(self, *argList):

        current = os.getcwd()
        if self.workDir:
            os.chdir(self.workDir)

        content = [ self._command ]
        for arg in argList:
            content.append(str(arg))

        self._handle = Popen(content, stdout = PIPE, stderr = PIPE, stdin = PIPE, bufsize = 1, universal_newlines = True)
        while self._handle.poll() is None:
            self._capture(self._handle.stdout, self.outputFunction)
            self._capture(self._handle.stderr, self.errorFunction)
                    
        self._capture(self._handle.stdout, self.outputFunction)
        self._capture(self._handle.stderr, self.errorFunction)

        self.stop()
        os.chdir(current)

    def stop(self):

        if not self._handle:
            return

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
            output = pipe.readline().strip()
            if not output:
                return
            callBack(output)
