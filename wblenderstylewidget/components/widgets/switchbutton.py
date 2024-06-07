from PyQt5.QtWidgets import QHBoxLayout, QLabel, QToolButton, QWidget
from PyQt5.QtGui import QColor, QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtProperty

from wblenderstylewidget.common.style_sheet import BlenderStyleSheet
from .widget_base import WidgetBaseSetting
  
class Indicator(QToolButton, WidgetBaseSetting):

    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setCheckable(True)
        super().setChecked(False)
        self.resize(30, 15)
        self.__sliderOnColor = QColor("#000000")
        self.__sliderOffColor = QColor("#FFFF55")
        self.__sliderDisabledColor = QColor("#FFFFFF")
        self.timer = QTimer(self)
        self.padding = self.height()//4
        self.sliderX = self.padding
        self.sliderRadius = (self.height() -2*self.padding)//2
        self.sliderEndX = self.width()-2*self.sliderRadius
        self.sliderStep = self.width()/50
        self.timer.timeout.connect(self.__updateSliderPos)

    def __updateSliderPos(self):
        if self.isChecked():
            if self.sliderX+self.sliderStep < self.sliderEndX:
                self.sliderX += self.sliderStep
            else:
                self.sliderX = self.sliderEndX
                self.timer.stop()
        else:
            if self.sliderX-self.sliderStep > self.sliderEndX:
                self.sliderX -= self.sliderStep
            else:
                self.sliderX = self.sliderEndX
                self.timer.stop()

        self.style().polish(self)

    def setChecked(self, isChecked: bool):
        if isChecked == self.isChecked():
            return
        super().setChecked(isChecked)
        self.sliderEndX = self.width()-2*self.sliderRadius - \
            self.padding if self.isChecked() else self.padding
        self.timer.start(5)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.sliderEndX = self.width()-2*self.sliderRadius - \
            self.padding if self.isChecked() else self.padding
        self.timer.start(5)
        self.checkedChanged.emit(self.isChecked())

    def resizeEvent(self, e):
        self.padding = self.height()//4
        self.sliderRadius = (self.height()-2*self.padding)//2
        self.sliderStep = self.width()/50
        self.sliderEndX = self.width()-2*self.sliderRadius - \
            self.padding if self.isChecked() else self.padding
        self.update()

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        if self.isEnabled():
            color = self.sliderOnColor if self.isChecked() else self.sliderOffColor
        else:
            color = self.sliderDisabledColor
        painter.setBrush(color)
        painter.drawEllipse(round(self.sliderX), self.padding, self.sliderRadius*2, self.sliderRadius*2)

    def getSliderOnColor(self):
        return self.__sliderOnColor

    def setSliderOnColor(self, color: QColor):
        self.__sliderOnColor = color
        self.update()

    def getSliderOffColor(self):
        return self.__sliderOffColor

    def setSliderOffColor(self, color: QColor):
        self.__sliderOffColor = color
        self.update()

    def getSliderDisabledColor(self):
        return self.__sliderDisabledColor

    def setSliderDisabledColor(self, color: QColor):
        self.__sliderDisabledColor = color
        self.update()

    sliderOnColor = pyqtProperty(QColor, getSliderOnColor, setSliderOnColor)
    sliderOffColor = pyqtProperty(QColor, getSliderOffColor, setSliderOffColor)
    sliderDisabledColor = pyqtProperty(QColor, getSliderDisabledColor, setSliderDisabledColor)

class SwitchButton(QWidget):

    checkedChanged = pyqtSignal(bool)

    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)
        self.text = text
        self.__spacing = 0
        self.hBoxLayout = QHBoxLayout(self)
        self.indicator = Indicator(self)
        self.label = QLabel(text, self)
        self.label.setFont(QFont("Arial", 12))
        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(30)
        self.hBoxLayout.addWidget(self.indicator)
        self.hBoxLayout.addWidget(self.label)
        self.hBoxLayout.setSpacing(self.__spacing)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.indicator.checkedChanged.connect(self.checkedChanged)

        BlenderStyleSheet.SWITCHBUTTON.apply(self)

    def isChecked(self):
        return self.indicator.isChecked()

    def setChecked(self, isChecked: bool):
        self.indicator.setChecked(isChecked)

    def toggleChecked(self):
        self.indicator.setChecked(not self.indicator.isChecked())

    def setText(self, text: str):
        self.text = text
        self.label.setText(text)
        self.adjustsSize()

    def getSpacing(self):
        return self.__spacing

    def setSpacing(self, spacing: int):
        self.__spacing = spacing
        self.hBoxLayout.setSpacing(spacing)
        self.update()

    spacing = pyqtProperty(int, getSpacing, setSpacing)