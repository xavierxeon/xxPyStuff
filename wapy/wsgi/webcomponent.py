#!/usr/bin/env python3

class WebComponent:

    _contentTypes = {
        'html': 'text/html'
        , 'css': 'text/css'
        , 'jpeg': 'image/jpeg'
        , 'png': 'image/png'
        , 'json': 'application/json'
        , 'js': 'application/javascript'
        , 'xml': 'application/xml'
    }

    def __init__(self):

        self._postArgs = dict()

    def __call__(self, env, responseFunction):

        return self._notFound(responseFunction)


    def _notFound(self, responseFunction):

        responseFunction('404 Not Found', [('content-type','text/plain')])
        return [b'']

    def _response(self, responseFunction, fileType, content):

        contentType = 'text/plain'
        if fileType in self._contentTypes:
            contentType = self._contentTypes[fileType]

        responseFunction('200 OK', [('Content-type', contentType)])
        return [content.encode()]

    def _setPostArgs(self, postArgs):

        self._postArgs = postArgs
