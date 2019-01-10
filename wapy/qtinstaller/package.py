#!/usr/bin/env python3

import os

import xml.etree.ElementTree as xmlfile

from .lib import Settings
from ..tools import XMLTools

class Package:
    
    def __init__(self, installer, name, subKey, version = None):

        installer._packageList.append(self)
        self._key = installer._key + '.' + subKey

        self._data = {
            'DisplayName': name,
            'Name': self._key,
            'Version': version if version else '1.0',
            'Default': 'true'
        }

        self._metaDir = 'installer/packages/' + self._key + '/meta'
        self._dataDir = 'installer/packages/' + self._key + '/data'

    def copyFiles(self, targetDir):

        raise NotImplementedError()        

    def setDefault(self, default):

        self._data['Default'] = 'true' if default else 'false'

    def _createMeta(self):

        os.makedirs(self._metaDir, exist_ok = True)

        root = xmlfile.Element('Package')

        for key, value in self._data.items():
            xmlfile.SubElement(root, key).text = value     

        XMLTools.indent(root)        
        with open(self._metaDir + '/package.xml', 'wb') as outfile:
            content = xmlfile.tostring(root, encoding='utf8')
            outfile.write(content)

    def _startCopyFiles(self):

        os.makedirs(self._dataDir + '/content', exist_ok = True)
        self.copyFiles(os.getcwd() + '/' + self._dataDir + '/content')

    def _zipAndRemoveContent(self):

        pass
