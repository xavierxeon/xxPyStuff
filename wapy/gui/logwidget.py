#!/usr/bin/env python3

import sys

# pylint: disable=E0611
from PySide2.QtWidgets import (
    QWidget
    , QLabel
    , QTextEdit
    , QVBoxLayout
    , QApplication
)  
from PySide2.QtGui import QTextCursor, QColor 
from PySide2.QtCore import QEventLoop 
# pylint: enable=E0611

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

        label = QLabel('Messages')

        textEdit = QTextEdit()
        sys.stdout = Logger(textEdit)
        sys.stderr = Logger(textEdit, QColor(255, 0, 0))

        masterLayout = QVBoxLayout(self)
        masterLayout.addWidget(label)
        masterLayout.addWidget(textEdit)

        self._edit = textEdit
        self.setLayout(masterLayout)
        
    def clear(self):

        self._edit.clear()
