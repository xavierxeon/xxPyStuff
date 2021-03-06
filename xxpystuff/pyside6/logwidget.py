#!/usr/bin/env python3

import sys

from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QApplication
from PySide6.QtGui import QTextCursor, QColor 
from PySide6.QtCore import QEventLoop 

class Logger:

    def __init__(self, edit, color = None):

        self._edit = edit
        self._color = color

    def write(self, message):

        if self._color:
            orgColor = self._edit.textColor()
            self._edit.setTextColor(self._color)

        self._edit.moveCursor(QTextCursor.End)
        self._edit.insertPlainText(message)

        if self._color:
            self._edit.setTextColor(orgColor)

        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

    def flush(self):

        pass


class LogWidget(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        textEdit = QTextEdit()
        sys.stdout = Logger(textEdit)
        sys.stderr = Logger(textEdit, QColor(255, 0, 0))

        masterLayout = QVBoxLayout(self)
        masterLayout.addWidget(textEdit)

        self._edit = textEdit
        self.setLayout(masterLayout)
        
    def clear(self):

        self._edit.clear()
