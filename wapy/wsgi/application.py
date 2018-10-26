#!/usr/bin/env python3

class Application:

    _contentTypes = {
        'html': 'text/html'
        , 'css': 'text/css'
        , 'jpeg': 'image/jpeg'
        , 'png': 'image/png'
        , 'svg': 'image/svg+xml'
        , 'json': 'application/json'
        , 'js': 'application/javascript'
        , 'xml': 'application/xml'
        , 'ico': 'image/x-icon'
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

    def _responseBinary(self, responseFunction, fileType, content):

        contentType = 'application/octet-stream'
        if fileType in self._contentTypes:
            contentType = self._contentTypes[fileType]

        responseFunction('200 OK', [('Content-type', contentType)])
        return [content]

    def _setPostArgs(self, postArgs):

        self._postArgs = postArgs
