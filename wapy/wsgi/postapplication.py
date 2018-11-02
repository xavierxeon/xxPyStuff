#!/usr/bin/env python3

from .application import Application

class PostApplication(Application):

    def __init__(self):

        Application.__init__(self)
        self._postFunctionDict = dict()      

    def __call__(self, env, responseFunction):

        if env['REQUEST_METHOD'] != 'POST':
            print('PostApplication: not a post request, got ' + env['REQUEST_METHOD'])
            return self._notFound(responseFunction)

        try:
            length = int(env.get('CONTENT_LENGTH', '0'))
        except ValueError: # CONTENT_LENGTH might not exist
            length = 0
                
        body = env['wsgi.input'].read(length).decode()
        postArgs = dict()
        
        fields = body.split('&')
        for field in fields:
            content = field.split('=')
            if len(content) < 2:
                continue 
            postArgs[content[0]] = content[1]


        if 'function' in postArgs:
            functionName = postArgs['function']
            if functionName in self._postFunctionDict:
                return self._postFunctionDict[functionName](postArgs, responseFunction)
        else:
            print('no function in postArgs')
            if not postArgs:
                print(' * postArgs are empty')
            else:
                for key, value in postArgs.items():
                    print(' * {0}:{1}'.format(key, value))

        return self._notFound(responseFunction)     

    def _registerFunction(self, key, function):

        self._postFunctionDict[key] = function
