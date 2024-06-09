from decimal import Decimal, ROUND_HALF_UP
from typing import Union
from PyQt5.QtWidgets import QApplication, QStyleOptionSpinBox, QStyle, QStyleOption, QWidget, QSpinBox, QHBoxLayout, QDoubleSpinBox, QAbstractSpinBox
from PyQt5.QtGui import QCursor, QMouseEvent, QPainter, QColor
from PyQt5.QtCore import Qt, QEvent, QPointF

from common.icon import BlenderStyleIcon
from common.style_sheet import BlenderStyleSheet
from .button import PushButton
from .widget_base import WidgetBaseSetting

class SpinBoxStyle(QStyle):
    def __init__(self):
        super().__init__()
        self.cornerRadius = [5, 5]

    def drawControl(self, option: QStyleOption, painter: QPainter, widget: QWidget = None):
        self.widget = widget
        if isinstance(option, QStyleOptionSpinBox):
            self.drawSpinBox(option, painter)

    def drawSpinBox(self, option: QStyleOptionSpinBox, painter: QPainter):
        background_rect = option.rect
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 根據滑鼠動作改變顏色
        if self.widget.isEnter and self.widget.isDragging:
            painter.setBrush(QColor('#222222'))
        elif self.widget.isEnter and not self.widget.isDragging:
            painter.setBrush(QColor('#656565'))
        else:
            painter.setBrush(QColor('#545454'))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(background_rect, self.cornerRadius[0], self.cornerRadius[1])

    def setRoundRect(self, xRadius:float=5, yRadius:float=5):
        self.cornerRadius[0] = xRadius
        self.cornerRadius[1] = yRadius

class BaseSpinBox(WidgetBaseSetting):
    def __init__(self, text:str=None, parent=None, *args,
                minimum:Union[int, float]=-1000000, 
                maximum:Union[int, float]=1000000, **kwargs):
        super().__init__(parent)
        self.minimum = minimum
        self.maximum = maximum
        self.value = 0
        self.text = text

        self.isEnter = False
        self.isDragging = False
        self.isEditing = False
        self.isLineEditActive = False
        self.cornerRadius = [5, 5]

        self.BaseSetting()
        self.innerSetting()
        self.installEventFilter(self)
        BlenderStyleSheet.SPINBOX.apply(self)

    def innerSetting(self):
        self.setRange(self.minimum, self.maximum)
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)
        
        self.line_edit = self.lineEdit()
        self.line_edit.installEventFilter(self)
        self.line_edit.setVisible(False)
        self.line_edit.setDisabled(True)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.line_edit.setGeometry(self.rect())

    def setRange(self, minimum: Union[int, float], maximum: Union[int, float]):
        '''Override the setRange method to add custom behavior.'''
        if not (isinstance(minimum, Union[int, float]) and isinstance(maximum, Union[int, float])):
            raise TypeError("Minimum and maximum values must be integers")
        if minimum > maximum:
            raise ValueError("Minimum value cannot be greater than maximum value")
        
        self.minimum = minimum
        self.maximum = maximum
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        if not self.checkRange(self.value, self.minimum, self.maximum): 
            self.value = self.minimum
        else:
            self._setInitialValue(self.value)
        self.update()

    def setCornerRaduis(self, xRadius:int=3, yRadius:int=3):
        self.cornerRadius[0] = xRadius
        self.cornerRadius[1] = yRadius

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.line_edit.setGeometry(self.rect())

    def _setInitialValue(self, initial_value: Union[int, float]):
        '''Set the initial value of the progress bar based on the input.

        The initial value can be provided as either a float representing a percentage
        (e.g., 0.5 for 50%) or an integer representing an absolute value.
        '''
        if isinstance(initial_value, int) or isinstance(initial_value, float):
            self.setValue(initial_value)
        else: raise TypeError("initial_value must be an integer or float")

    def mousePressEvent(self, event: QMouseEvent):
        '''滑鼠點擊時更新進度'''
        if event.buttons() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.isDragging = True
            self.isEditing = True
            self.last_mouse_x = event.x()
            self.update()
            self.updateValue(event)
            QApplication.setOverrideCursor(QCursor(Qt.CursorShape.SizeHorCursor))

    def mouseMoveEvent(self, event: QMouseEvent):
        '''滑鼠移動時，如果正在拖動，更新進度'''
        if hasattr(self, 'isDragging') and self.isDragging:
            self.isEditing = False
            self.updateValue(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        '''釋放滑鼠後，停止拖動'''
        if hasattr(self, 'isEditing') and self.isEditing:
            QApplication.restoreOverrideCursor()
            self.isLineEditActive = True
            self.line_edit.setVisible(True)
            self.line_edit.setDisabled(False)
            
            self.update()
        elif hasattr(self, 'isDragging') and self.isDragging:
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

    def eventFilter(self, obj, event:QEvent):
        if event.type() == QEvent.Type.KeyPress and obj == self and self.isEditing:
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Escape:
                self.closeLineEdit()
                return True
        return super().eventFilter(obj, event)

    def closeLineEdit(self):
        self.line_edit = self.lineEdit()
        try:
            if '.' in self.line_edit.text():
                self.value = float(self.line_edit.text())
            else:
                self.value = int(self.line_edit.text())
        except ValueError as e:
            print("Invalid input:", self.line_edit.text())
        self.line_edit.setVisible(False)
        self.line_edit.setDisabled(True)
        self.line_edit.hide()
        self.isDragging = False     # HACK:保持輸入數值後滑鼠處於懸浮狀態
        self.isEditing = False
        self.isLineEditActive = False
        self.setFocus()

    def checkRange(self, value:int, min:int, max:int):
        return min <= value <= max

    def paintEvent(self, event):
        if self.isLineEditActive:
            return
        painter = QPainter(self)
        style = SpinBoxStyle()  # 使用您定義的SpinBoxStyle
        style.setRoundRect(self.cornerRadius[0], self.cornerRadius[1])
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        opt = QStyleOptionSpinBox()
        self.initStyleOption(opt)
        opt.rect = self.rect().adjusted(0, 0, 0 ,0)
        style.drawControl(opt, painter, self)

        painter.setBackgroundMode(Qt.BGMode.TransparentMode)
        painter.setPen(QColor(Qt.GlobalColor.white))

        value = f"{self.value}"

        if self.text is not None: 
            painter.drawText(QPointF(10, self.height() / 2 + 5), self.text)
            text_rect = painter.boundingRect(self.rect(), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, value)
            text_rect.adjust(-10, 0, -10, 0)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, value)
        else:
            text_rect = painter.boundingRect(self.rect(), Qt.AlignmentFlag.AlignCenter, value)
            text_rect.adjust(-5, 0, -5, 0)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, value)

    def updateValue(self, event):
        mouse_x = event.x()
        speed = 2 if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ControlModifier else 1
        # 計算實際進度值
        self.value += int((mouse_x - self.last_mouse_x) / speed)
        self.last_mouse_x = event.x()
        if self.value < self.minimum:
            self.value = self.minimum
        if self.value > self.maximum: 
            self.value = self.maximum
        # 設置SpinBox的值
        self.setValue(self.value) if isinstance(self.value, int) else float(self.value)

class PlainSpinBox(QSpinBox, BaseSpinBox):
    """
    A custom SpinBox with additional features such as configurable range, hover and press states, and support for editing values.

    Parameters
    -----------
    text : str, optional

        The text to be displayed on the SpinBox. Default is None.

    parent : QWidget, optional

        The parent widget of the SpinBox. Default is None.

    **kwargs : dict

        Additional keyword arguments to pass to the QAbstractSpinBox constructor.
 
    Note
    ~~~~
    In the default state where text is entered, the PlainSpinBox will center the numbers within the component.

    Examples
    --------

    .. code-block:: python

        from PyQt5.QtWidgets import QApplication, QMainWindow
        from customwidgets import PlainSpinBox

        app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
        window = QMainWindow()
        spin_box = PlainSpinBox()
        window.setStyleSheet("background-color: #303030; color: white;")
        window.setCentralWidget(spin_box)
        window.show()
        app.exec_()

    Note
    ~~~~
    When text is entered as a parameter, the PlainSpinBox will align the input text to the left and the numbers to the right.

    Examples
    --------

    .. code-block:: python

        from PyQt5.QtWidgets import QApplication, QMainWindow
        from customwidgets import PlainSpinBox

        app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
        window = QMainWindow()
        spin_box = PlainSpinBox("PlainSpinBox with text")
        window.setStyleSheet("background-color: #303030; color: white;")
        window.setCentralWidget(spin_box)
        window.show()
        app.exec_()
    """
    def __init__(self, text: str = None, parent=None, *args,
                minimum:int=-1000000, 
                maximum:int=1000000,**kwargs):
        QSpinBox.__init__(self, parent)
        BaseSpinBox.__init__(self, text, parent, *args, minimum=minimum, maximum=maximum, **kwargs)

    def setRange(self, minimum: int, maximum: int):
        """
        This method sets the minimum and maximum values for the spin box,
        defining the range of values it can represent. 

        Parameters
        ----------
        minimum : int
            The minimum value of the spin box.
        maximum : int
            The maximum value of the spin box.
        """
        super().setRange(minimum, maximum)
        if not (isinstance(minimum, int) and isinstance(maximum, int)):
            raise TypeError("Minimum and maximum values must be integers")
        if minimum > maximum:
            raise ValueError("Minimum value cannot be greater than maximum value")
        
        self.minimum = minimum
        self.maximum = maximum
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        if not self.checkRange(self.value, self.minimum, self.maximum): 
            self.value = self.minimum
            self.update()

    def setValue(self, value: int):
        super().setValue(value)
        QSpinBox.setValue(self, value)

class PlainDoubleSpinBox(QDoubleSpinBox, BaseSpinBox):
    """
    A custom DoubleSpinBox with additional features such as configurable range, hover and press states, and support for editing values.

    Parameters
    -----------
    text : str, optional

        The text to be displayed on the DoubleSpinBox. Default is None.

    parent : QWidget, optional

        The parent widget of the DoubleSpinBox. Default is None.

    **kwargs : dict

        Additional keyword arguments to pass to the QAbstractSpinBox constructor.
 
    Note
    ~~~~
    In the default state where text is entered, the PlainDoubleSpinBox will center the numbers within the component.

    Examples
    --------

    .. code-block:: python

        from PyQt5.QtWidgets import QApplication, QMainWindow
        from customwidgets import PlainDoubleSpinBox

        app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
        window = QMainWindow()
        spin_box = PlainDoubleSpinBox()
        window.setStyleSheet("background-color: #303030; color: white;")
        window.setCentralWidget(spin_box)
        window.show()
        app.exec_()

    Note
    ~~~~
    When text is entered as a parameter, the PlainDoubleSpinBox will align the input text to the left and the numbers to the right.

    Examples
    --------

    .. code-block:: python

        from PyQt5.QtWidgets import QApplication, QMainWindow
        from customwidgets import PlainDoubleSpinBox

        app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
        window = QMainWindow()
        spin_box = PlainDoubleSpinBox("PlainSpinBox with text")
        window.setStyleSheet("background-color: #303030; color: white;")
        window.setCentralWidget(spin_box)
        window.show()
        app.exec_()
    """
    # FIXME 無法即時更新數值
    def __init__(self, text: str = None, parent=None, *args,
                 minimum:int=-1000000, 
                 maximum:int=1000000,
                 decimal_places:int=2, **kwargs):
        QDoubleSpinBox.__init__(self, parent)
        BaseSpinBox.__init__(self, text, parent, *args, minimum, maximum, **kwargs)
        self.setRange(-100.0, 100.0)
        self.setDecimals(decimal_places)
        
    def setRange(self, minimum: float, maximum: float):
        '''Override the setRange method to add custom behavior.'''
        if not (isinstance(minimum, float) and isinstance(maximum, float)):
            minimum = float(minimum)
            maximum = float(maximum)
        if minimum > maximum:
            raise ValueError("Minimum value cannot be greater than maximum value")
        
        self.minimum = minimum
        self.maximum = maximum
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        if not self.checkRange(self.value, self.minimum, self.maximum): 
            self.value = self.minimum
            self.setValue(self.minimum)
            self.update()

        super().setRange(minimum, maximum)

    def setValue(self, value: float):
        super().setValue(value)

class ButtonSpinBox(QWidget):
    """
    A custom widget combining a spin box with up and down buttons.

    Parameters
    -----------
    text : str, optional

        The text to be displayed on the SpinBox. Default is None.
        
    value : int, optional

        The initial value of the spin box. Default is 1.

    step : int, optional

        The step size for increasing or decreasing the value. Default is 1.

    parent : QWidget, optional

        The parent widget of the ButtonSpinBox. Default is None.

    **kwargs : dict

        Additional keyword arguments to pass to the PlainSpinBox constructor.

    Parameters
    -----------
    text : str, optional

        The text to be displayed on the DoubleSpinBox. Default is None.

    parent : QWidget, optional

        The parent widget of the DoubleSpinBox. Default is None.

    **kwargs : dict

        Additional keyword arguments to pass to the QAbstractSpinBox constructor.
 
    Note
    ~~~~
    In the default state where text is entered, the ButtonSpinBox will center the numbers within the component.

    Examples
    --------

    .. code-block:: python

        from PyQt5.QtWidgets import QApplication, QMainWindow
        from customwidgets import ButtonSpinBox

        app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
        window = QMainWindow()
        spin_box = ButtonSpinBox()
        window.setStyleSheet("background-color: #303030; color: white;")
        window.setCentralWidget(spin_box)
        window.show()
        app.exec_()

    Note
    ~~~~
    When text is entered as a parameter, the ButtonSpinBox will align the input text to the left and the numbers to the right.

    Examples
    --------

    .. code-block:: python

        from PyQt5.QtWidgets import QApplication, QMainWindow
        from customwidgets import ButtonSpinBox

        app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
        window = QMainWindow()
        spin_box = ButtonSpinBox("PlainSpinBox with text")
        window.setStyleSheet("background-color: #303030; color: white;")
        window.setCentralWidget(spin_box)
        window.show()
        app.exec_()
    """
    def __init__(self, text: str = None, value:int=1, step:int=1, parent=None, **kwargs):
        super().__init__(parent)
        self.value = value
        self.step = step

        self.hBoxLayout = QHBoxLayout()
        self.downButton = PushButton(icon=BlenderStyleIcon.LEFTARROWHEAD)
        self.downButton.setCornerRadius(PushButton.CornerRadiusAlign.LEFT)
        self.downButton.setPressColor("#222222")
        self.spinBox = PlainSpinBox(text=text, value=self.value, **kwargs)
        self.upButton = PushButton(icon=BlenderStyleIcon.RIGHTARROWHEAD)
        self.upButton.setCornerRadius(PushButton.CornerRadiusAlign.RIGHT)
        self.upButton.setPressColor("#222222")

        self.minimum = self.spinBox.minimum
        self.maximum = self.spinBox.maximum

        self.initWidget()
        self.initLayout()
        self.innerButtonSetting()

    def initWidget(self):
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSpacing(0)
        self.downButton.setFixedWidth(self.downButton.height())
        self.upButton.setFixedWidth(self.upButton.height())
        self.spinBox.setFixedHeight(self.downButton.height())
        self.spinBox.cornerRadius = [0, 0]
        self.spinBox.setValue(self.spinBox.value)

    def initLayout(self):
        self.hBoxLayout.addWidget(self.downButton)
        self.hBoxLayout.addWidget(self.spinBox, stretch=1)
        self.hBoxLayout.addWidget(self.upButton)
        self.setLayout(self.hBoxLayout)

    def innerButtonSetting(self):
        self.downButton.clicked.connect(lambda: self._decreaseValue())
        self.upButton.clicked.connect(lambda: self._increaseValue())

    def setRange(self, minimum: int, maximum: int) -> None:
        """
        This method sets the minimum and maximum values for the spin box,
        defining the range of values it can represent. 

        Parameters
        ----------
        minimum : int
            The minimum value of the spin box.
        maximum : int
            The maximum value of the spin box.
        """
        # super().setRange(minimum, maximum)
        self.spinBox.setRange(minimum, maximum)

    def _decreaseValue(self):
        if not self.spinBox.checkRange(self.spinBox.value, self.spinBox.minimum, self.spinBox.maximum):
            self.spinBox.value = self.spinBox.minimum
            self.spinBox.update()
        elif self.spinBox.value > self.spinBox.minimum:
            current_value = self.spinBox.value
            new_value = current_value - self.step
            self.spinBox.value = new_value
            self.spinBox.update()

    def _increaseValue(self):
        if not self.spinBox.checkRange(self.spinBox.value, self.spinBox.minimum, self.spinBox.maximum):
            self.spinBox.value = self.spinBox.maximum
            self.spinBox.update()
        elif self.spinBox.value < self.spinBox.maximum:
            current_value = self.spinBox.value
            new_value = current_value + self.step
            self.spinBox.value = new_value
        self.spinBox.update()