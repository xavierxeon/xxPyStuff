#!/usr/bin/env python3

from .application import Application

class PostApplication(Application):

    def __init__(self):

        Application.__init__(self)
        self._postFunctionDict = dict()        

    def _handlePost(self, env, responseFunction):

        try:
            length = int(env.get('CONTENT_LENGTH', '0'))
        except ValueError: # CONTENT_LENGTH might not exist
            length = 0
                
        body = env['wsgi.input'].read(length).decode()
        request = env["PATH_INFO"]
                
        postArgs = dict()
        
        fields = body.split('&')
        for field in fields:
            content = field.split('=')
            if len(content) < 2:
                continue 
            postArgs[content[0]] = content[1]

        if not postArgs:
            print(' => no argumets')
        else:
            print(' => {0} argumets'.format(len(postArgs)))
            for key, value in postArgs.items():
                print(' * {0} = {1}'.format(key, value))

        if 'function' in postArgs:
            functionName = postArgs['function']
            print('execute function {0}'.format(functionName))

        return self._notFound(responseFunction)        