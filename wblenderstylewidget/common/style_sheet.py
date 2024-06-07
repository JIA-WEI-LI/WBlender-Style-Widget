# coding:utf-8
from enum import Enum
from typing import List, Union
import os

from PyQt5.QtWidgets import QWidget

class BaseStyleSheet:
    def path(self):
        raise NotImplementedError
    
    def apply(self, widget: QWidget):
        """ apply style sheet to widget """
        setStyleSheet(widget, self)

class BlenderStyleSheet(BaseStyleSheet, Enum):
    BUTTON = "button"
    CHECKBOX = "checkbox"
    COLORDIALOG = "colordialog"
    COLORPICKER = "colorpicker"
    EXPANDABLELAYOUT = "expandablelayout"
    LINEEDIT = "lineedit"
    LISTWIDGET = "listwidget"
    PROGRESSBAR = "progressbar"
    SCROLLAREA = "scrollarea"
    SPINBOX = "spinbox"
    SWITCHBUTTON = "switchbutton"
    TOOLTIP = "tooltip"
    
    def path(self):
        return f"wblenderstylewidget\\styles\\{self.value}.qss"
    
def setStyleSheet(widget: QWidget, stylesheet: 'BaseStyleSheet'):
    """ Helper function to set the style sheet to the widget """
    qss_path = stylesheet.path()
    if os.path.exists(qss_path):
        with open(qss_path, 'r', encoding='utf-8') as file:
            qss_text = file.read()
            widget.setStyleSheet(qss_text)
            return qss_text
    else:
        raise FileNotFoundError(f"QSS file not found: {qss_path}")