from PyQt5.QtWidgets import QDialog, QPushButton
from PyQt5.QtGui import QMouseEvent

from common.style_sheet import BlenderStyleSheet
from .widget_base import WidgetBaseSetting
from ..dialog.color_dialog import ColorDialog

class ColorPicker(QPushButton, WidgetBaseSetting):
    """
    A custom QPushButton representing a color picker button with additional features such as hover and press states.

    Parameters
    ----------
    show_text : bool, optional

        Determines whether to display the selected color name as text on the button. Default is False.

    parent : QWidget, optional

        The parent widget of the button. Default is None.

    **kwargs : dict

        Additional keyword arguments to pass to the QPushButton constructor.

    Examples
    --------
    
    .. code-block:: python

        from PyQt5.QtWidgets import QApplication, QMainWindow
        from wblenderstylewidget import ColorPicker

        app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
        window = QMainWindow()
        color_picker = ColorPicker(show_text=True)
        window.setStyleSheet("background-color: #303030; color: white;")
        window.setCentralWidget(color_picker)
        window.show()
        app.exec_()
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
        """
        Open a color picker dialog and set the button's background color based on the user's selection.

        This method creates a color picker dialog using the `ColorDialog` class. If the user selects a
        color and accepts the dialog, the button's background color is updated to the selected color,
        and the text color is set to either black or white based on the lightness of the selected color.
        The selected color's name is also stored in the `selected_color_name` attribute, and if
        `show_text` is `True`, the button's text is updated to display the selected color's name.

        Returns
        -------
        QColor or None
            The selected QColor object if the user accepts the dialog, otherwise None.

        Examples
        --------
        .. code-block:: python

            button = PushButton(text="Select Color")
            selected_color = button.pickColor()
            if selected_color:
                print(f"Selected color: {selected_color.name()}")

        Notes
        -----
        - The `ColorDialog` class must be properly defined and imported.
        - The method assumes that the `selectedColor` method of `ColorDialog` returns a `QColor` object.
        - The `show_text` attribute determines whether the button's text is updated with the selected color's name.
        """
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