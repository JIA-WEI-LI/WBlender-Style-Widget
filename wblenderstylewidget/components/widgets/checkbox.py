from enum import Enum
from functools import singledispatchmethod
from PyQt5.QtWidgets import QCheckBox, QWidget, QSizePolicy
from PyQt5.QtGui import QMouseEvent, QFont

from common.style_sheet import BlenderStyleSheet
from .widget_base import WidgetBaseSetting

class CheckBoxState(Enum):
    CHECKED = 0
    CHECKED_DISABLED = 1
    CHECKED_HOVER = 2
    CHECKED_PRESSED = 3
    DISABLED = 4
    HOVER = 5
    NORMAL = 6
    PRESSED = 7

class CheckBox(QCheckBox, WidgetBaseSetting):
    """
    This is a custom QCheckBox with additional features such as hover and press states.

    Parameters
    ----------
    parent : QWidget, optional
        
        The parent widget of the button. Default is None.

    Examples
    --------
    
    .. code-block:: python

        from PyQt5.QtWidgets import QApplication, QMainWindow
        from wblenderstylewidget import CheckBox

        app = QApplication([])
        window = QMainWindow()
        check_box = CheckBox()
        window.setCentralWidget(check_box)
        window.show()
        app.exec_()
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.isPressed = False
        self.isHover = False

        self.BaseSetting()
        BlenderStyleSheet.CHECKBOX.apply(self)
        
        self._states = {}

    @singledispatchmethod
    def set_contents(self, *args, **kwargs):
        pass
    
    @set_contents.register
    def _(self, text: str, parent: QWidget = None):
        if parent:
            self.setParent(parent)
        self.setText(text)
        
    def _state(self):
        if not self.isEnabled():
            return CheckBoxState.CHECKED_DISABLED if self.isChecked() else CheckBoxState.DISABLED

        if self.isChecked():
            if self.isPressed: return CheckBoxState.CHECKED_PRESSED
            if self.isHover: return CheckBoxState.CHECKED_HOVER
            return CheckBoxState.CHECKED
        else:
            if self.isPressed: return CheckBoxState.PRESSED
            if self.isHover: return CheckBoxState.HOVER
            return CheckBoxState.NORMAL