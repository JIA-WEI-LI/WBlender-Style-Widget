from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import QPoint

from common.icon import BlenderStyleIcon
from common.style_sheet import BlenderStyleSheet
from .button import PushButton

class ExpandableLayout(QWidget):
    def __init__(self, title=None, parent=None):
        super().__init__(parent)

        self._is_collapsed = True
        self._title_frame = None
        self._content = None
        self._content_layout = None
        self.setObjectName("expandable_layout")

        self._main_v_layout = QVBoxLayout(self)
        self._main_v_layout.setSpacing(0)
        self._main_v_layout.addWidget(self.initTitleFrame(title))
        self._main_v_layout.addWidget(self.initContent(self._is_collapsed))

        BlenderStyleSheet.EXPANDABLELAYOUT.apply(self)

    def initTitleFrame(self, title):
        self._title_frame = PushButton(text=title, icon=BlenderStyleIcon.RIGHTARROWHEAD)
        self._title_frame.setTextAlign(PushButton.TextAlign.LEFT)
        self._title_frame.setObjectName("title_frame")
        self._title_frame.mousePressEvent = self.toggleCollapsed
        return self._title_frame

    def initContent(self, collapsed):
        self._content = QWidget()
        self._content_layout = QVBoxLayout(self._content)

        self._content.setObjectName("content_layout")
        self._content.setVisible(not collapsed)

        return self._content

    def addWidget(self, widget):
        self._content_layout.addWidget(widget)

    def toggleCollapsed(self, event):
        self._content.setVisible(self._is_collapsed)
        self._is_collapsed = not self._is_collapsed
