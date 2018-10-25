#!/usr/bin/env python3

import os
from pathlib import Path

from .webcomponent import WebComponent

class WebApplication(WebComponent):

    _contentTypes = {
        'html': 'text/html'
        , 'css': 'text/css'
        , 'jpeg': 'image/jpeg'
        , 'png': 'image/png'
        , 'json': 'application/json'
        , 'js': 'application/javascript'
        , 'xml': 'application/xml'
    }

    def __init__(self, rootPath, scriptName, startPage):

        WebComponent.__init__(self)

        self._rootPath = rootPath
        self._scriptName = scriptName
        self._startPage = startPage

        self._callPath = ''

    def __call__(self, env, responseFunction):

        if env['REQUEST_METHOD'] == 'POST':
            return self._handlePost(env, responseFunction)

        request = env["PATH_INFO"]
        print(self._callPath)
        print(request)
        if self._scriptName in request:
            self._compileCallPath(request)
            fileName = self._rootPath + '/' + self._startPage 
        else:
            if self._callPath + '/' in request:
                request = request.replace(self._callPath, '', 1)
            fileName = self._rootPath + request

        print(request)
        print(fileName)

        if not os.path.exists(fileName):
            return self._notFound(responseFunction)
        else:
            fileType = Path(fileName).suffix[1:]
        
        with open(fileName, 'r') as infile:
            content = infile.read()

        return self._response(responseFunction, fileType, content)

    def _compileCallPath(self, request):

        if self._callPath:
            return

        callPath = request.replace(self._scriptName, '')    
        if callPath.endswith('/'):
            callPath = callPath[ : -1]

        self._callPath = callPath

    def _handlePost(self, env, responseFunction):

        try:
            length = int(env.get('CONTENT_LENGTH', '0'))
        except ValueError: # CONTENT_LENGTH might not exist
            length = 0
                
        body = env['wsgi.input'].read(length).decode()
        request = env["PATH_INFO"]
        fileName = self._rootPath + request
                
        if not os.path.exists(fileName):
            return self._notFound(responseFunction)

        with open(fileName, 'r') as executable:
            exec(executable.read())
        
        if not 'application' in locals():
            return self._notFound(responseFunction)

        postApplication = locals()['application']
        if issubclass(type(postApplication), WebComponent):
            postArgs = dict()
            
            fields = body.split('&')
            for field in fields:
                content = field.split('=')
                if len(content) < 2:
                    continue 
                postArgs[content[0]] = content[1]

            postApplication._setPostArgs(postArgs)

        return postApplication(env, responseFunction)

