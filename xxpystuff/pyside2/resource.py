#!/Usr/bin/env python3

import os, subprocess, platform
import xml.etree.ElementTree as xmlfile

from ..tools import XMLTools


class Resource(list):

    def __init__(self):

        list.__init__(self)

    def createRCFile(self, name):

        if 0 == len(self):
            return

        root = xmlfile.Element('RCC')
        resource = xmlfile.SubElement(root, 'qresource')
        resource.attrib['version'] = '1.0'

        for fileName in self:        
            f = xmlfile.SubElement(resource, 'file')
            f.text = fileName

        XMLTools.indent(root)            

        content = xmlfile.tostring(root, method ='xml')
        with open(name, 'w') as outfile:
            outfile.write('<!DOCTYPE RCC>\n')
            outfile.write(content.decode() + '\n')

    def makePythonFile(self, rcFile, pythonFile):

        import PySide2.QtCore
        path = os.path.dirname(PySide2.QtCore.__file__)
        if 'Windows' == platform.system():
            rccExe = path + '\\pyside2-rcc.exe'
        else:
            rccExe = path + '/pyside2-rcc'

        if not os.path.exists(rccExe):
            return

        if os.path.exists(pythonFile):
            os.remove(pythonFile)

        command = (rccExe, rcFile , '-o' , pythonFile)
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                output, error = process.communicate()
        
        if output:
            print('OUTPUT')
            for line in output.decode().split('\n'):
                print(line)

        if error:
            print('ERROR')
            for line in error.decode().split('\n'):
                print(line)    

