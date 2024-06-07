import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget, QListWidgetItem, QFrame
from PyQt5.QtCore import Qt

from wblenderstylewidget.common.style_sheet import BlenderStyleSheet
# from .widget_base import WidgetBaseSetting

class ListWidget(QListWidget):
    """
    A custom QListWidget with additional styling and functionalities such as adding separators and removing selected items.

    Parameters
    ----------
    >>> parent : QWidget, optional

        The parent widget of this custom list widget. Default is None.

    Usage
    -----
    >>> list_widget = ListWidget()
    >>> list_widget.addSeparator()
    >>> list_widget.remove_selected_item()
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ListWidget")

        BlenderStyleSheet.LISTWIDGET.apply(self)

    def addSeparator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        item = QListWidgetItem()
        self.setItemWidget(item, separator)

    def remove_selected_item(self):
        for item in self.selectedItems():
            self.takeItem(self.row(item))