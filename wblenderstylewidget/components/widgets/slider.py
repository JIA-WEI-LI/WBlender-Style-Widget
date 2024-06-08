from typing import Union
from PyQt5.QtWidgets import QApplication, QProgressBar, QSizePolicy, QStyle, QStyleOption, QStyleOptionProgressBar, QWidget
from PyQt5.QtGui import QColor, QCursor, QFont, QMouseEvent, QPainter
from PyQt5.QtCore import QEvent, QPointF, Qt

from common.style_sheet import BlenderStyleSheet
from .widget_base import WidgetBaseSetting

class ProgressBarSliderStyle(QStyle):
    def drawControl(self, element: QStyle.ControlElement, option: QStyleOption, painter: QPainter, widget: QWidget = None, *args,
                    color:str):
        self.widget = widget
        if element == QStyle.ControlElement.CE_ProgressBar:
            if isinstance(option, QStyleOptionProgressBar):
                self.drawProgressBar(option, painter, color)

    def drawProgressBar(self, option: QStyleOptionProgressBar, painter: QPainter, color:str):
        background_rect = option.rect
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 隨滑鼠動作改變顏色
        if self.widget.isEnter and self.widget.isDragging:
            painter.setBrush(QColor('#000000'))
        elif self.widget.isEnter and not self.widget.isDragging:
            painter.setBrush(QColor('#656565'))
        else:
            painter.setBrush(QColor('#545454'))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(background_rect, 5, 5)
        
        # Draw Progressbar
        progress_rect = background_rect.adjusted(0, 0, 0, 0)
        progress_width = int(progress_rect.width() * (option.progress / 100.0))
        progress_rect.setWidth(progress_width)

        # 繪製帶有圓角效果的進度條
        painter.setBrush(QColor(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(progress_rect, 5, 5)

class ProgressBarSlider(QProgressBar, WidgetBaseSetting):
    """
    This is a custom QProgressBar that behaves like a QSlider, allowing users to drag and set values.

    Parameters
    ----------
    text : str, optional
        The text to be displayed on the progress bar. Default is "Value".

    minimum : int, optional
        The minimum value of the progress bar. Default is 0.

    maximum : int, optional
        The maximum value of the progress bar. Default is 100.

    initial_value : Union[float, int], optional
        The initial value of the progress bar. Can be a float representing a percentage
        (e.g., 0.5 for 50%) or an integer representing an absolute value. Default is 0.5.

    color : str, optional
        The color of the progress bar. Default is "#4772b3".

    decimal_places : int, optional
        The number of decimal places to display for the progress value. Default is 2.

    parent : QWidget, optional
        The parent widget of the progress bar. Default is None.

    **kwargs : dict
        Additional keyword arguments to pass to the QProgressBar constructor.

    Examples
    --------

    .. code-block:: python

        from PyQt5.QtWidgets import QApplication, QMainWindow
        from customwidgets import ProgressBarSlider

        app = QApplication([])
        window = QMainWindow()
        progress_bar_slider = ProgressBarSlider()
        window.setCentralWidget(progress_bar_slider)
        window.show()
        app.exec_()

    """
    def __init__(self, text="Value", minimum:int=0, maximum:int=100 , initial_value: Union[float, int]=0.5, parent=None, *args,
                color:str="#4772b3", decimal_places:int=2, **kwargs):
        super().__init__(parent)
        self.text = text
        self.minimum = minimum
        self.maximum = maximum
        self.color = color
        self.initial_value = initial_value
        self.decimal_places = decimal_places
        self.apply_style = False
        self.isEnter = False
        self.isDragging = False

        self.BaseSetting()
        self.innerSetting()

    def innerSetting(self):
        self.setRange(self.minimum, self.maximum)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self._setInitialValue(self.initial_value)

    def setRange(self, minimum: int, maximum: int):
        """
        This method sets the minimum and maximum values for the progress bar,
        defining the range of values it can represent. 

        Parameters
        ----------
        minimum : int
            The minimum value of the progress bar.
        maximum : int
            The maximum value of the progress bar.
        """
        self.min_value = minimum
        self.max_value = maximum

    def setBackgroundColor(self, color:str):
        """Sets the background color of the progress bar."""
        self.backgroundColor = color

    def setProgressColor(self, color:str):
        """Sets the color of the progress indicator of the progress bar."""
        self.progressColor = color

    def getValue(self):
        """Returns the current value of the progress bar."""
        return self.value()

    def _setInitialValue(self, initial_value: Union[float, int]):
        '''Set the initial value of the progress bar based on the input.

        The initial value can be provided as either a float representing a percentage
        (e.g., 0.5 for 50%) or an integer representing an absolute value.
        '''
        if isinstance(initial_value, float) and 0 <= initial_value <= 1:
            self.setValue(int(initial_value * 100))
        elif isinstance(initial_value, int) or isinstance(initial_value, float):
            self.setValue(initial_value)
        else: raise TypeError("initial_value must be a float or an integer")

    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.isDragging = True
            self.update()
            self.updateProgress(event)
            QApplication.setOverrideCursor(QCursor(Qt.CursorShape.BlankCursor))

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        return super().mouseDoubleClickEvent(event)
    
    def mouseMoveEvent(self, event):
        if hasattr(self, 'isDragging') and self.isDragging:
            self.updateProgress(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if hasattr(self, 'isDragging') and self.isDragging:
            self.isDragging = False
            QApplication.restoreOverrideCursor()
            self.update()
        else:
            super().mouseReleaseEvent(event)

    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.isEnter = True
        self.update()

    def leaveEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.isEnter = False
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        style = ProgressBarSliderStyle()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        opt = QStyleOptionProgressBar()
        self.initStyleOption(opt)
        opt.rect = self.rect().adjusted(1, 1, -1, -1)
        opt.textVisible = self.isTextVisible()

        style.drawControl(QStyle.ControlElement.CE_ProgressBar, opt, painter, self, color=self.color)

        painter.setBackgroundMode(Qt.BGMode.TransparentMode)
        painter.setPen(QColor(Qt.GlobalColor.white))
        painter.drawText(QPointF(10, self.height() / 2 + 5), self.text)

        # 繪製數值
        progress = self.value() * (self.maximum - self.minimum) / 100 + self.minimum
        text = f"{progress:.{self.decimal_places}f}"
        text_rect = painter.boundingRect(self.rect(), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)
        text_rect.adjust(-5, 0, -5, 0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)

    def updateProgress(self, event):
        mouse_x = event.x()
        total_width = self.width()

        progress_percent = mouse_x / total_width
        if progress_percent < 0:
            self.setValue(0)
            return
        if progress_percent > 1:
            self.setValue(100)
            return
        self.setValue(int(progress_percent * 100))