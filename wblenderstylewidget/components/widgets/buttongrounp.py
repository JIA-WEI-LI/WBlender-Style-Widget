from PyQt5.QtWidgets import QWidget, QHBoxLayout, QButtonGroup

from .button import PushButton, RadioButton

class RadioButtonGroup(QWidget):
    """
    A custom QWidget that creates a group of radio buttons arranged horizontally. Each button can have configurable corner radius and initial selection.

    Parameters
    ----------
    lists : list of str, optional

        A list of strings representing the labels for each radio button. Default is [""].

    initial_selection : int, optional

        The index of the button that should be initially selected. Default is 0.

    parent : QWidget, optional

        The parent widget of the button group. Default is None.

    Examples
    --------
    
    .. code-block:: python

        from PyQt5.QtWidgets import QApplication, QMainWindow
        from wblenderstylewidget import RadioButtonGroup

        app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
        window = QMainWindow()
        button_list = ["List 1", "List 2", "List 3"]
        button_group = RadioButtonGroup(lists=button_list)
        window.setStyleSheet("background-color: #303030; color: white;")
        window.setCentralWidget(button_group)
        window.show()
        app.exec_()
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

    def setRatioButtonCornerRadius(self, index:int, total:int):
        """
        Sets the corner radius for the radio buttons based on their position in the group.

        Parameters
        ----------
        index : int

            The index of the current radio button.

        total : int

            The total number of radio buttons in the group.

        Returns
        -------
        int
            The corner radius alignment for the current radio button.
        """
        if index == 0:
            return PushButton.CornerRadiusAlign.LEFT
        elif index == total - 1:
            return PushButton.CornerRadiusAlign.RIGHT
        else: return PushButton.CornerRadiusAlign.CENTER  
