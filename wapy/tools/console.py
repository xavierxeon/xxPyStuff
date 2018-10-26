#!/usr/bin/env python3

class Console:
    
    @staticmethod
    def _write(message, bold, color):
        if bold:
            return '\033[1m' + color + message + '\033[0m'    
        else:
            return color + message + '\033[0m'    

    @staticmethod
    def grey(message, bold = False):
        return Console._write(message, bold, '\033[90m')

    @staticmethod
    def red(message, bold = False):
        return Console._write(message, bold, '\033[91m')

    @staticmethod
    def green(message, bold = False):
        return Console._write(message, bold, '\033[92m')        

    @staticmethod
    def yellow(message, bold = False):
        return Console._write(message, bold, '\033[93m')

    @staticmethod
    def blue(message, bold = False):
        return Console._write(message, bold, '\033[94m')
            
    @staticmethod
    def magenta(message, bold = False):
        return Console._write(message, bold, '\033[95m')

    @staticmethod
    def cyan(message, bold = False):
        return Console._write(message, bold, '\033[96m')

    @staticmethod
    def white(message, bold = False):
        return Console._write(message, bold, '\033[97m')  

