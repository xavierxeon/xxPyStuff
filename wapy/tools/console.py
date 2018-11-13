﻿#!/usr/bin/env python3

class Console:

    class _ColorBash:
        Clear = '\033[0m'
        Bold = '\033[1m'
        Grey = '\033[90m'
        Red = '\033[91m'
        Green = '\033[92m'
        Yellow = '\033[93m'
        Blue = '\033[94m'
        Magenta = '\033[95m'
        Cyan = '\033[96m'
        White = '\033[97m'

    Color = None

    @staticmethod
    def _write(message, bold, color):
        if not Console.Color:
            Console.Color = Console._ColorBash
            
        if bold:
            return Console.Color.Bold + color + message + Console.Color.Clear    
        else:
            return color + message + Console.Color.Clear    

    @staticmethod
    def grey(message, bold = False):
        return Console._write(message, bold, Console.Color.Grey)

    @staticmethod
    def red(message, bold = False):
        return Console._write(message, bold, Console.Color.Red)

    @staticmethod
    def green(message, bold = False):
        return Console._write(message, bold, Console.Color.Green)        

    @staticmethod
    def yellow(message, bold = False):
        return Console._write(message, bold, Console.Color.Yellow)

    @staticmethod
    def blue(message, bold = False):
        return Console._write(message, bold, Console.Color.Blue)
            
    @staticmethod
    def magenta(message, bold = False):
        return Console._write(message, bold, Console.Color.Magenta)

    @staticmethod
    def cyan(message, bold = False):
        return Console._write(message, bold, Console.Color.Cyan)

    @staticmethod
    def white(message, bold = False):
        return Console._write(message, bold, Console.Color.White)  
