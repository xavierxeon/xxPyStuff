#!/usr/bin/env python3

class Style:

    class FgColor:
        Default = 'default'
        Black = 'black'
        Blue = 'light blue'
        Brown = 'brown'
        Cyan = 'light cyan'
        Gray = 'light gray'
        Green = 'light green'
        Magenta = 'light magenta'
        Red = 'light red'                
        White = 'white'
        Yellow = 'yellow'        
        DarkBlue = 'dark blue'
        DarkCyan = 'dark cyan'
        DarkGray = 'dark gray'
        DarkGreen ='dark green'
        DarkRed = 'dark red'
        DarkMagenta = 'dark magenta'
        
    class BgColor:      
        Default = 'default'
        Black = 'black'
        Brown = 'brown'
        Gray = 'light gray'
        DarkBlue = 'dark blue'
        DarkCyan = 'dark cyan'
        DarkGreen = 'dark green'
        DarkMagenta = 'dark magenta'
        DarkRed = 'dark red'

    class Emphasis:
        Default = ''
        Blink = 'blink'
        Bold = 'bold'
        Italics = 'italics'
        Standout = 'standout'
        StrikeThrough = 'strikethrough'
        UnderLine = 'underline'

    _counter = 0
            
    def __init__(self, foregroundColor, backgroundColor = BgColor.Default, emphasis = Emphasis.Default):

        Style._counter += 1
        self.name = 'palette_style_{0}'.format(Style._counter)
        self.foregroundColor = foregroundColor
        self.backgroundColor = backgroundColor
        self.emphasis = emphasis

    def toTuple(self):

        data = list()
        data.append(self.name)
        data.append(self.foregroundColor)
        data.append(self.backgroundColor)
        data.append(self.emphasis)
        return tuple(data)
