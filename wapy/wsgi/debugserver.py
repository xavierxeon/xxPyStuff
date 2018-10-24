#!/usr/bin/env python3

import os


class DebugServer:

    _port = 8080

    def __init__(self, rootApp):

        self._rootApp = rootApp

    def start(self, delayToOpenBorwser = 0.0):

        from wsgiref.simple_server import make_server
        import threading

        httpd = make_server('', self._port, self._rootApp)
        print('Serving on port {0}...'.format(self._port))

        if delayToOpenBorwser > 0.0:
            timer = threading.Timer(delayToOpenBorwser, self._openBrowser)
            timer.start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()
            print('Goodbye.')

    def _openBrowser(self):

        import webbrowser
        webbrowser.open('http://localhost:{0}'.format(self._port))
