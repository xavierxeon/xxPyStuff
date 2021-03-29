#!/usr/bin/env python3

import platform

class Console:

   class Color:
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

   __initilized = False

   @staticmethod
   def _init():
      
      if Console.__initilized:
         return

      # make output look nice in windows cmd window 
      if platform.platform() == 'Windows':
         from colorama import init
         init()
      Console.__initilized = True

   @staticmethod
   def _write(message, bold, color):
      Console._init()
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

   @staticmethod
   def qtFriendly(message):
      message = message.replace(Console.Color.Clear, '</font>')
      message = message.replace(Console.Color.Bold, '')
      message = message.replace(Console.Color.Grey, '<font style="color:Grey">')
      message = message.replace(Console.Color.Red, '<font style="color:Red">')
      message = message.replace(Console.Color.Green, '<font style="color:Green">')
      message = message.replace(Console.Color.Yellow, '<font style="color:Yellow">')
      message = message.replace(Console.Color.Blue, '<font style="color:Blue">')
      message = message.replace(Console.Color.Magenta, '<font style="color:Magenta">')
      message = message.replace(Console.Color.Cyan, '<font style="color:Cyan">')
      message = message.replace(Console.Color.White, '<font style="color:White">')

      return message
