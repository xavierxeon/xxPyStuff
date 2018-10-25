#!/usr/bin/env python3

import os
from pathlib import Path

from .component import Component

class RootApplication(Component):

    def __init__(self, rootPath, startPage):

        Component.__init__(self)

        self._rootPath = rootPath
        self._startPage = startPage
        self._callbackDict = dict()

    def __call__(self, env, responseFunction):

        if env['REQUEST_METHOD'] == 'POST':
            return self._handlePost(env, responseFunction)

        request = env["PATH_INFO"]
        print("REQUEST IN: " + request)
        if '/' is request:
            fileName = self._rootPath + '/' + self._startPage 
        else:
            fileName = self._rootPath + request

        print('FILENAME: ' + fileName)

        if not os.path.exists(fileName) or not os.path.isfile(fileName):
            return self._notFound(responseFunction)
        else:
            fileType = Path(fileName).suffix[1:]
        
        with open(fileName, 'r') as infile:
            content = infile.read()

        return self._response(responseFunction, fileType, content)

    def registerPostCallback(self, name, function):

        self._callbackDict[name] = function

    def _handlePost(self, env, responseFunction):

        try:
            length = int(env.get('CONTENT_LENGTH', '0'))
        except ValueError: # CONTENT_LENGTH might not exist
            return self._notFound(responseFunction)
                
        body = env['wsgi.input'].read(length).decode()
        request = env["PATH_INFO"]
                
        postArgs = dict()
        
        fields = body.split('&')
        for field in fields:
            content = field.split('=')
            if len(content) < 2:
                continue 
            postArgs[content[0]] = content[1]

        return self._notFound(responseFunction)
