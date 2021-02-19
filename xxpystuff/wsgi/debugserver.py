#!/usr/bin/env python3

import os
from pathlib import Path
from wsgiref.simple_server import make_server
import threading
import webbrowser

from .application import Application
from ..tools import Console

class DebugServer(Application):

    _port = 8080

    def __init__(self, rootDir = '', indexfFile = 'index.html'):

        self._rootDir = rootDir
        if rootDir.endswith('/'):
            self._rootDir = rootDir[ : -1]
        self.indexFile = indexfFile
        self._scriptAliasDirMap = dict()
        
    def __call__(self, env, responseFunction):

        request = env["PATH_INFO"]
        print(Console.yellow('REQUEST is {0}').format(request))

        scriptName = self._checkScript(request)
        if scriptName:
            return self._handleScript(scriptName, env, responseFunction)

        if env['REQUEST_METHOD'] == 'POST':
            print(Console.red('no POST application found'))
            return self._notFound(responseFunction)

        if '/' == request:
            fileName = self._rootDir + '/' + self.indexFile 
        else:
            fileName = self._rootDir + request

        if not os.path.exists(fileName) or not os.path.isfile(fileName):
            print(Console.red('GET: file not found {0}').format(fileName))
            return self._notFound(responseFunction)
        else:
            fileType = Path(fileName).suffix[1:]
            print(Console.green('GET: serve file {0} of type {1}').format(fileName, fileType))
        
        try:
            with open(fileName, 'r') as infile:
                content = infile.read()
            return self._response(responseFunction, fileType, content)
        except UnicodeDecodeError:
            with open(fileName, 'rb') as infile:
                content = infile.read()
            return self._responseBinary(responseFunction, fileType, content)            

        return self._notFound(responseFunction)


    def start(self, delayToOpenBorwser = 0.0):

        httpd = make_server('', self._port, self)
        print(Console.blue('Serving on port {0}...').format(self._port))

        if delayToOpenBorwser > 0.0:
            timer = threading.Timer(delayToOpenBorwser, self._openBrowser)
            timer.start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()
            print('Goodbye.')

    def addScriptAliasDir(self, htmlDir, localPath):

        if not htmlDir.startswith('/'):
            htmlDir = '/' + htmlDir
        if not htmlDir.endswith('/'):
            htmlDir = htmlDir + '/'

        if not localPath.endswith('/'):
            localPath = localPath + '/'

        print('add script alias {0} @ {1}'.format(htmlDir, localPath))

        self._scriptAliasDirMap[htmlDir] = localPath

    def _openBrowser(self):

        print(Console.grey('open browser'))
        webbrowser.open('http://localhost:{0}'.format(self._port))

    def _checkScript(self, request):

        for htmlDir, localPath in self._scriptAliasDirMap.items():
            if not htmlDir in request:
                continue
            
            scriptName = request.replace(htmlDir, localPath)
            if os.path.exists(scriptName):
                return scriptName

        return ''

    def _handleScript(self, scriptName, env, responseFunction):

        with open(scriptName, 'r') as scriptFile:
            exec(scriptFile.read())
        if 'application' in locals():
            scriptApplication = locals()['application']
            print(Console.cyan('execute script {0}').format(scriptName))
            return scriptApplication(env, responseFunction)

        print(Console.red('unable to execute wsgi applicaiton in script {0]').format(scriptName))            
        return self._notFound(responseFunction)


