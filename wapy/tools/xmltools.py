#!/usr/bin/env python3

#import xml.etree.ElementTree as xmlfile

class XMLTools:

    @staticmethod
    def indent(elem, tabwidth = 4, level = 0):
        tab = tabwidth * " "
        i = "\n" + (level * tab)
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + tab
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                XMLTools.indent(elem, tabwidth, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i    