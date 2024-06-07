from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QMouseEvent, QKeyEvent
from PyQt5.QtWidgets import QLineEdit, QWidget, QHBoxLayout

from common.icon import BlenderStyleIcon
from common.style_sheet import BlenderStyleSheet
from .button import PushButton
from .widget_base import WidgetBaseSetting

class LineEdit(QLineEdit, WidgetBaseSetting):
    """
    This is a custom QLineEdit with additional features such as focus policies, hover and press states, 
    and custom key press handling.

    Parameters:
    -----------
    >>> parent : QWidget, optional

        The parent widget of the line edit. Default is None.

    >>> **kwargs : dict

        Additional keyword arguments to pass to the QLineEdit constructor.

    Usage:
    ------
    >>> line_edit = LineEdit(parent=some_parent_widget)
    >>> line_edit.setText("Edit me")
    """
    def __init__(self, parent=None, **kwargs):
        super(LineEdit, self).__init__(parent=parent)
        self.setObjectName("LineEdit")
        self.BaseSetting()
        self.innerSetting()
        BlenderStyleSheet.LINEEDIT.apply(self)
        
    def innerSetting(self):
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)
        self.installEventFilter(self)

    def mousePressEvent(self, event: QMouseEvent):
        self.isPressed = True
        self.editing = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.isPressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event: QMouseEvent):
        self.isHover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event: QMouseEvent):
        self.isHover = False
        self.update()
        super().leaveEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if self.editing:
            if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Escape):
                self.clearFocus()
        super().keyPressEvent(event)

class SearchLineEdit(QWidget):
    """
    A custom QWidget that combines a search button, a line edit, and a delete button into a single widget.
    This widget is styled for a search functionality with clear and focus events handling.

    Parameters
    ----------
    >>> parent : QWidget, optional

        The parent widget of this custom widget. Default is None.

    **kwargs : dict

        Additional keyword arguments to pass to the QWidget constructor.

    Usage
    -----
    >>> search_widget = SearchLineEdit()
    """
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.hBoxLayout = QHBoxLayout()
        self.search_button = PushButton(icon=BlenderStyleIcon.SEARCH)
        self.search_button.setCornerRadius(PushButton.CornerRadiusAlign.LEFT)
        self.search_button.setBackgroundColor("#1d1d1d")
        self.search_button.setHoverColor("#222222")
        self.search_button.setPressColor("#1d1d1d")
        self.search_linEdit = LineEdit()
        self.deleted_button = PushButton(icon=BlenderStyleIcon.CLOSE)
        self.deleted_button.setCornerRadius(PushButton.CornerRadiusAlign.RIGHT)
        self.deleted_button.setBackgroundColor("#1d1d1d")
        self.deleted_button.setHoverColor("#222222")
        self.deleted_button.setPressColor("#1d1d1d")

        self.initWidget()
        self.initLayout()

        BlenderStyleSheet.LINEEDIT.apply(self)

    def initWidget(self):
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSpacing(0)

        self.search_button.setMinimumWidth(self.search_button.height())

        self.search_linEdit.setObjectName("SearchLineEdit")
        self.search_linEdit.setPlaceholderText("Search")

        self.deleted_button.setMinimumWidth(self.deleted_button.height())
        self.deleted_button.clicked.connect(self.clearLineEdit)

    def initLayout(self):
        self.hBoxLayout.addWidget(self.search_button)
        self.hBoxLayout.addWidget(self.search_linEdit)
        self.hBoxLayout.addWidget(self.deleted_button)
        self.setLayout(self.hBoxLayout)

    def focusInEvent(self, event):
        if not self.search_linEdit.text():
            self.search_linEdit.setPlaceholderText("")
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        if not self.search_linEdit.text():
            self.search_linEdit.setPlaceholderText("Search")
        super().focusOutEvent(event)

    def clearLineEdit(self):
        self.search_linEdit.clear()