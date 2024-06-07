import os
from typing import Union, List

from functools import singledispatchmethod
from PyQt5.QtWidgets import QDialog, QPushButton, QWidget, QButtonGroup
from PyQt5.QtGui import QIcon, QMouseEvent, QColor
from PyQt5.QtCore import QSize, Qt

from wblenderstylewidget.common.style_sheet import BlenderStyleSheet
from .tooltip import Tooltip
from .widget_base import WidgetBaseSetting
from ..dialog.color_dialog import ColorDialog

class PushButton(QPushButton, WidgetBaseSetting):
    """
    A custom QPushButton with additional features such as configurable corner radius,
    hover and press states, and support for both text and icon.

    Parameters
    ----------
    >>> text : str, optional

        The text to be displayed on the button. Default is None.

    >>> icon : Union[QIcon, str], optional

        The icon to be displayed on the button. This can be a QIcon object or a string path to the icon image. Default is None.

    >>> parent : QWidget, optional

        The parent widget of the button. Default is None.

    **kwargs : dict

        Additional keyword arguments to pass to the QPushButton constructor.

    Usage
    -----
    >>> push_button = PushButton(text="Click Me", icon="path/to/icon.png")
    >>> push_button = PushButton(text="Click Me")
    """
    class TextAlign:
        LEFT = Qt.AlignmentFlag.AlignLeft
        CENTER = Qt.AlignmentFlag.AlignCenter
        RIGHT = Qt.AlignmentFlag.AlignRight

    class CornerRadiusAlign:
        LEFT_TOP = 1
        TOP = 2
        RIGHT_TOP = 3
        LEFT = 4
        CENTER = 5
        RIGHT = 6
        LEFT_BOTTOM = 7
        BOTTOM = 8
        RIGHT_BOTTOM = 9
        DEFAULT = 0

    def __init__(self, text: str = None, icon: Union[QIcon, str] = None, *args,
                 parent: QWidget = None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        self.initialized = False
        self.setObjectName('PushButton')
        self.setColor("#545454", "#656565", "#4772b3")
        self.setCornerRadius(self.CornerRadiusAlign.DEFAULT, 5)
        self.setTextAlign(self.TextAlign.CENTER)

        self.setIconSize(QSize(12, 12))
        self.setIcon(QIcon(icon) or None)
        self.setText(text or None)
        self.setFixedHeight(None)

        self.updateQss()
        self.initialized = True
        
    @singledispatchmethod
    def set_contents(self, *args, **kwargs):
        pass
        
    @set_contents.register
    def _(self, text: str, icon: Union[QIcon, str] = None, parent: QWidget = None):
        self.__init__(parent=parent)
        self.setText(text)
        self.setIcon(icon)

    @set_contents.register
    def _(self, icon: QIcon, text: str, parent: QWidget = None):
        self.__init__(text, parent, icon)
        self.setText(text)
        self.setIcon(icon)

    def update_Qss(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            if self.initialized:
                self.updateQss()
        return wrapper
        
    @update_Qss
    def setCornerRadius(self, button_radius_type:Union[int, CornerRadiusAlign, list[int]]=0, radius:int=5) -> list[str, str, str, str]:
        if isinstance(button_radius_type, int) or isinstance(button_radius_type, self.CornerRadiusAlign):
            left_top = radius if button_radius_type in [0, 1, 2, 4] else 0
            right_top = radius if button_radius_type in [0, 2, 3, 6] else 0
            left_bottom = radius if button_radius_type in [0, 4, 7, 8] else 0
            right_bottom = radius if button_radius_type in [0, 6, 8, 9] else 0
            self.corner_radius = [left_top, right_top, left_bottom, right_bottom]
        elif isinstance(button_radius_type, list) and len(button_radius_type) == 4:
            self.corner_radius = button_radius_type
        else:
            raise ValueError("corner_radius must be either an integer(or type CornerRadiusAlign) or a list of 4 integers.")
        return self.corner_radius

    @update_Qss
    def setTextAlign(self, align: TextAlign):
        self.text_align = align
        
    @update_Qss
    def setColor(self, background_color:str, hover_color:str, press_color:str):
        self.backGroundColor = background_color
        self.hoverColor = hover_color
        self.pressColor = press_color
    
    @update_Qss
    def setBackgroundColor(self, color:str):
        '''Set the button background color.'''
        self.backGroundColor = color

    @update_Qss
    def setHoverColor(self, color:str):
        '''Set the button hover color.'''
        self.hoverColor = color

    @update_Qss
    def setPressColor(self, color:str):
        '''Set the button press color.'''
        self.pressColor = color

    def updateQss(self):
        align_dict = {
            self.TextAlign.LEFT: 'left',
            self.TextAlign.CENTER: 'center',
            self.TextAlign.RIGHT: 'right'
        }
        qss = f"""
            QPushButton#PushButton {{
                background-color: {self.backGroundColor};
                border-top-left-radius: {self.corner_radius[0]}px;
                border-top-right-radius: {self.corner_radius[1]}px;
                border-bottom-left-radius: {self.corner_radius[2]}px;
                border-bottom-right-radius: {self.corner_radius[3]}px;
                color: white;
                font-family: Arial, Helvetica, sans-serif;
                font-size: 14px;
                padding-left: 3px;
                padding-right: 3px;
                text-align: {align_dict[self.text_align]};
            }}
            QPushButton#PushButton:hover {{
                background-color: {self.hoverColor};
            }}
            QPushButton#PushButton:pressed {{
                background-color: {self.pressColor};
            }}
        """
        self.setStyleSheet(qss)
        
    def mousePressEvent(self, event: QMouseEvent):
        self.isPressed = True
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

class ColorPicker(QPushButton, WidgetBaseSetting):
    """
    A custom QPushButton representing a color picker button with additional features such as hover and press states.

    Parameters
    ----------
    >>> show_text : bool, optional

        Determines whether to display the selected color name as text on the button. Default is False.

    >>> parent : QWidget, optional

        The parent widget of the button. Default is None.

    **kwargs : dict

        Additional keyword arguments to pass to the QPushButton constructor.

    Usage
    -----
    >>> color_picker_button = ColorPicker(show_text=True)
    >>> color_picker_button.pickColor()  # Auto opens a color picker dialog to select a color.
    """
    def __init__(self, show_text:bool = False, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.selected_color_name = kwargs.get("selected_color_name", "#545454")
        self.show_text = show_text

        self.BaseSetting()
        self.innerSetting()
        BlenderStyleSheet.COLORPICKER.apply(self)

    def innerSetting(self):
        self.setText(self.selected_color_name) if self.show_text else self.setText("")
        self.clicked.connect(self.pickColor)

    def mousePressEvent(self, event: QMouseEvent):
        self.isPressed = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.isPressed = False
        super().mouseReleaseEvent(event)

    def enterEvent(self, event: QMouseEvent):
        self.isHover = True
        self.update()

    def leaveEvent(self, event: QMouseEvent):
        self.isHover = False
        self.update()

    def pickColor(self):
        # 創建顏色選擇器對話框
        colorPickerDialog = ColorDialog()
        color = colorPickerDialog.exec_()
        
        if color == QDialog.Accepted:
            selected_color = colorPickerDialog.selectedColor()
            font_color = "black" if selected_color.lightnessF() > 0.5 else "white"
            button_style = f"background-color: {selected_color.name()}; border-radius: 3px; color: {font_color}; font-family: Arial, Helvetica, sans-serif ; letter-spacing: 0.8px;"
            self.setStyleSheet(button_style)
            self.selected_color_name = selected_color.name()
            if self.show_text: self.setText(selected_color.name())
            return selected_color
        return

class ToggleButton(PushButton):
    """
    A custom ToggleButton that extends PushButton to add toggle functionality.
    The button will change state (pressed or not pressed) when clicked.

    Parameters
    ----------
    *args : tuple

        Additional positional arguments to pass to the PushButton constructor.

    **kwargs : dict
    
        Additional keyword arguments to pass to the PushButton constructor.

    Usage
    -----
    >>> toggle_button = ToggleButton(text="Toggle Me")
    >>> toggle_button.setToggleColor("#4772b3", "#628bca", "#628bca")
    >>> toggle_button.setChecked(True)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggled = False
        self._backgraoundColor = self.backGroundColor
        self._pressColor = self.pressColor
        self._hoverColor = self.hoverColor
        self.setToggleColor("#4772b3", "#628bca", "#628bca")
        self.updateQss()

        self.initialized = True

    def update_Qss(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            if self.initialized:
                self.updateQss()
        return wrapper
    
    @update_Qss
    def setChecked(self, checked):
        self.toggled = checked
        self.getButtonColor(self.toggled)
        super().setChecked(checked)

    @update_Qss
    def setToggleColor(self, toggle_background_color:str, toggle_hover_color:str, toggle_press_color:str):
        self.setToggleBackgroundColor(toggle_background_color)
        self.setToggleHoverColor(toggle_hover_color)
        self.setTogglePressColor(toggle_press_color)

    @update_Qss
    def setToggleBackgroundColor(self, color:str):
        self.toggleBackgroundColor = color

    @update_Qss
    def setTogglePressColor(self, color:str):
        self.togglePressColor = color

    @update_Qss
    def setToggleHoverColor(self, color:str):
        self.toggleHoverColor = color

    @update_Qss
    def getButtonColor(self, toggled):
        if toggled:
            self.backGroundColor = self.toggleBackgroundColor
            self.pressColor = self.togglePressColor
            self.hoverColor = self.toggleHoverColor
        else: 
            self.backGroundColor = self._backgraoundColor
            self.pressColor = self._pressColor
            self.hoverColor = self._hoverColor

    def mousePressEvent(self, event: QMouseEvent):
        self.toggled = not self.toggled
        self.getButtonColor(self.toggled)
        super().mousePressEvent(event)

class RadioButton(ToggleButton):
    """
    A custom RadioButton that extends PushButton to add radio button functionality.
    The button will behave like a radio button, being part of a mutually exclusive group of buttons.

    Parameters
    ----------
    >>> group : QButtonGroup

        The button group to which this radio button belongs.

    *args : tuple

        Additional positional arguments to pass to the ToggleButton constructor.

    **kwargs : dict

        Additional keyword arguments to pass to the ToggleButton constructor.

    Usage
    -----
    >>> button_group = QButtonGroup()
    >>> radio_button1 = RadioButton(group=button_group, text="Option 1")
    >>> radio_button2 = RadioButton(group=button_group, text="Option 2")
    """

    def __init__(self, group: QButtonGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggled = False
        self.group = group
        self.group.addButton(self)
        self.updateQss()

    def mousePressEvent(self, event: QMouseEvent):
        if not self.toggled:
            self.toggled = True
            self.getButtonColor(self.toggled)
            for button in self.group.buttons():
                if button != self:
                    button.toggled = False
                    button.getButtonColor(button.toggled)