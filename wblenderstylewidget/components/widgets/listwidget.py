import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget, QListWidgetItem, QFrame
from PyQt5.QtCore import Qt

from wblenderstylewidget.common.style_sheet import BlenderStyleSheet
# from .widget_base import WidgetBaseSetting

class ListWidget(QListWidget):
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom QListWidget Example")

        self.list_widget = ListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.list_widget.addItem("Custom Item 1")
        self.list_widget.addItem("Custom Item 2")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
