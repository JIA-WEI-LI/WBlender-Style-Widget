from PyQt5.QtWidgets import QWidget, QHBoxLayout, QButtonGroup

from .button import PushButton, RadioButton

class RatioButtonGroup(QWidget):
    """
    This is a custom QPushButton representing a color picker button with additional features such as hover and press states.

    Parameters:
    -----------
    show_text : bool, optional
        Determines whether to display the selected color name as text on the button. Default is False.
    parent : QWidget, optional
        The parent widget of the button. Default is None.
    **kwargs : dict
        Additional keyword arguments to pass to the QPushButton constructor.

    Usage:
    ------
    >>> ratio_button_group = RatioButtonGroup(show_text=True)
    """
    def __init__(self, lists: list[str] = [""], initial_selection: int = 0, parent=None):
        super().__init__(parent)
        
        self.button_group = QButtonGroup(self)
        self.setLayout(self.setup_layout(lists, initial_selection))

    def setup_layout(self, lists, initial_selection):
        hBoxLayout = QHBoxLayout()
        hBoxLayout.setSpacing(1)
        hBoxLayout.setContentsMargins(0, 0, 0, 0)

        for index, item in enumerate(lists):
            radioButton = RadioButton(self.button_group, text=item)
            radioButton.setCornerRadius(self.setRatioButtonCornerRadius(index, len(lists)))
            self.button_group.addButton(radioButton, index)
            hBoxLayout.addWidget(radioButton)
            if index == initial_selection:
                radioButton.setChecked(True)

        return hBoxLayout

    def setRatioButtonCornerRadius(self, index:int, total:int, radius:int=5):
        if index == 0:
            return PushButton.CornerRadiusAlign.LEFT
        elif index == total - 1:
            return PushButton.CornerRadiusAlign.RIGHT
        else: return PushButton.CornerRadiusAlign.CENTER  
