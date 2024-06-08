import os
import sys
from typing import Union
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QMainWindow, QStatusBar, QLabel
from PyQt5.QtCore import Qt

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, grandparent_dir)

from common.icon import *
from components.layout import *
from components.widgets import *
from components.widgets.expandablelayout import ExpandableLayout
from wblenderstylewidget import __version__

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Blender Style Widgets Demo")
        self.setGeometry(100, 100, 500, 600)
        self.setStyleSheet("background-color: #303030; color: white; font-family: Arial, Helvetica, sans-serif;")
        self.setupCentralWidget()
        self.setupStatusBar()

    def setupCentralWidget(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        central_widget.setLayout(layout)
        self.setupScrollArea(layout)

    def setupScrollArea(self, layout: Union[QVBoxLayout, QHBoxLayout]):
        scroll_area = ScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_layout.setSpacing(0)
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        self.setupExpandableLayout(scroll_layout)
        scroll_area.setStyleSheet("border: none;")

    def setupExpandableLayout(self, scroll_layout: Union[QVBoxLayout, QHBoxLayout]):
        button_demo = ExpandableLayout(title="Buttons")
        button_demo.addWidget(PushButton())
        button_demo.addWidget(PushButton("PushButton"))
        button_demo.addWidget(PushButton("PushButton ( with icon )", BlenderStyleIcon.CHECK))
        button_demo.addWidget(ToggleButton("ToggleButton"))
        button_demo.addWidget(RadioButtonGroup(["RadioButton 1", "RadioButton 2", "RadioButton 3"]))
        scroll_layout.addWidget(button_demo)
        
        checkBox_demo = ExpandableLayout(title="CheckBoxs")
        checkBox_demo.addWidget(CheckBox())
        checkBox_demo.addWidget(CheckBox("CheckBox"))
        scroll_layout.addWidget(checkBox_demo)

        colorPicker_demo = ExpandableLayout(title="Color Pickers")
        colorPicker_demo.addWidget(ColorPicker())
        colorPicker_demo.addWidget(ColorPicker(True))
        scroll_layout.addWidget(colorPicker_demo)

        lineEdit_demo = ExpandableLayout(title="LineEdits")
        lineEdit_demo.addWidget(LineEdit())
        lineEdit_demo.addWidget(SearchLineEdit())
        scroll_layout.addWidget(lineEdit_demo)

        listWidget_demo = ExpandableLayout(title="List Widgets")
        list_widget = ListWidget()
        list_widget.addItems(["List 1", "List 2", "List 3"])
        list_widget.addSeparator()
        list_widget.addItems(["List 1", "List 2", "List 3"])
        listWidget_demo.addWidget(list_widget)
        scroll_layout.addWidget(listWidget_demo)

        slider_demo = ExpandableLayout(title="ProgressBar Sliders")
        slider_demo.addWidget(ProgressBarSlider(decimal_places=0))
        slider_demo.addWidget(ProgressBarSlider(minimum=-0.1, maximum=0.1, decimal_places=3))
        scroll_layout.addWidget(slider_demo)

        spinBox_demo = ExpandableLayout(title="SpinBoxs")
        spinBox_demo.addWidget(PlainSpinBox())
        spinBox_demo.addWidget(PlainSpinBox("PlainSpinBox", minimum=-1000, maximum=1000))
        spinBox_demo.addWidget(ButtonSpinBox())
        spinBox_demo.addWidget(ButtonSpinBox("ButtonSpinBox"))
        scroll_layout.addWidget(spinBox_demo)

        switchButton_demo = ExpandableLayout(title="SwitchButtons")
        switchButton_demo.addWidget(SwitchButton())
        switchButton_demo.addWidget(SwitchButton("SwitchButton"))
        scroll_layout.addWidget(switchButton_demo)

    def setupStatusBar(self):
        status_bar = QStatusBar()
        status_bar.setStyleSheet("background-color: #232323; color: white;")
        self.setStatusBar(status_bar)
        
        version_label = QLabel(f"{__version__}")
        status_bar.insertPermanentWidget(0, version_label)
        status_bar.showMessage("Already")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
    
    