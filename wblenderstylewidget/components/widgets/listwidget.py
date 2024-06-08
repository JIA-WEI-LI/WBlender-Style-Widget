import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget, QListWidgetItem, QFrame
from PyQt5.QtCore import Qt

from common.style_sheet import BlenderStyleSheet

class ListWidget(QListWidget):
    """
    A custom QListWidget with additional styling and functionalities such as adding separators and removing selected items.

    Parameters
    ----------
    parent : QWidget, optional

        The parent widget of this custom list widget. Default is None.

    Examples
    --------
    
    .. code-block:: python

        from PyQt5.QtWidgets import QApplication, QMainWindow
        from wblenderstylewidget import ListWidget

        app = QApplication([])
        window = QMainWindow()
        list_widget = ListWidget()
        list_widget.addItems(["List 1", "List 2", "List 3"])
        window.setCentralWidget(list_widget)
        window.show()
        app.exec_()
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ListWidget")

        BlenderStyleSheet.LISTWIDGET.apply(self)

    def addSeparator(self):
        """
        Adds a visual separator to the list widget.

        This method creates a horizontal line (separator) and adds it as an item
        to the list widget. The separator is implemented as a `QFrame` with a
        `HLine` shape and `Sunken` shadow to visually distinguish sections of the
        list. This can be useful for organizing items within the list.
        
        Note
        ----
        The separator is purely visual and does not affect the functionality of the
        list items around it.
        """
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        item = QListWidgetItem()
        self.setItemWidget(item, separator)

    def remove_selected_item(self):
        """
        Removes the currently selected item(s) from the list widget.

        This method iterates over all selected items in the list widget and removes
        them. It is useful for allowing users to delete items from the list
        interactively.

        Note
        ----
        If multiple items are selected, all selected items will be removed. The
        method checks for selection before attempting to remove items to ensure
        safe operation.
        """
        for item in self.selectedItems():
            self.takeItem(self.row(item))