import sys
from typing import Union
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QToolTip
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import QTimer, Qt

from wblenderstylewidget.common.style_sheet import BlenderStyleSheet

class Tooltip(QWidget):
    def __init__(self, title: str = "", content: str = "", icon: Union[QIcon, str] = None):
        super().__init__()
        self.setGeometry(100, 100, 300, 150)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)  # 隱藏標題列
        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)

        content_label = QLabel(content)
        content_label.setObjectName("contentLabel")
        layout.addWidget(content_label)

        # Icon
        if icon:
            icon_label = QLabel()
            pixmap = QPixmap(icon)
            icon_label.setPixmap(pixmap)
            layout.addWidget(icon_label)

        self.setLayout(layout)
        BlenderStyleSheet.TOOLTIP.apply(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTooltip)

    @staticmethod
    def setToolTip(widget, title="", content="", icon=None, delay=1000):
        widget.setToolTip("")  # 清空原生的 ToolTip

        def startTimer():
            widget.timer.start(delay)

        def stopTimer(event):  # 不接受任何參數
            widget.timer.stop()

        def showTooltip():
            tooltip = Tooltip(title, content, icon)
            tooltip.move(widget.mapToGlobal(widget.rect().bottomLeft()))  # 在底部左側顯示
            tooltip.show()

        widget.enterEvent = startTimer
        widget.leaveEvent = stopTimer
        widget.showEvent = stopTimer
        widget.hideEvent = stopTimer
        widget.showTooltip = showTooltip