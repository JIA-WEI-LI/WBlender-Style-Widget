from PyQt5.QtWidgets import QSizePolicy, QWidget
from PyQt5.QtGui import QFont, QMouseEvent

from wblenderstylewidget.common.style_sheet import BlenderStyleSheet

class WidgetBaseSetting(QWidget):
    TOP: int
    BUTTON: int
    LEFT: int
    RIGHT: int
    TOP_LEFT: int
    TOP_RIGHT: int
    BOTTOM_LEFT: int
    BOTTOM_RIGHT: int

    FONT = QFont("Arial", 11)

    class COLOR:
        COLOR_22 = "#222222"

    def BaseSetting(self):
        self.isPressed = False
        self.isHover = False

        self.setFont(self.FONT)
        self.setFixedHeight(None)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # if hasattr(BlenderStyleSheet, self.__class__.__name__.upper()):
        #     getattr(BlenderStyleSheet, self.__class__.__name__.upper()).apply(self)

    def setFixedHeight(self, height):
        default_height = 30
        new_height = height if height is not None else default_height
        super().setFixedHeight(new_height)