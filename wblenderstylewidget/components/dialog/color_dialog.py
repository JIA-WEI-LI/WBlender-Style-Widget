from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PyQt5.QtWidgets import QPushButton, QColorDialog, QLabel, QSpinBox, QLineEdit, QGraphicsOpacityEffect

from common.style_sheet import BlenderStyleSheet

class ColorDialog(QColorDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        BlenderStyleSheet.COLORDIALOG.apply(self)

    def showEvent(self, event):
        super().showEvent(event)
        self.setStyleSheet("background-color: #222;")

        labels = self.findChildren(QLabel)
        for label in labels:
            label.setFixedHeight(23)

        buttons = self.findChildren(QPushButton)
        for button in buttons:
            button.setFixedHeight(23)
            button.setMinimumWidth(60)

        spinBoxs = self.findChildren(QSpinBox)
        for spinBox in spinBoxs:
            spinBox.setFixedHeight(23)

        lineEdits = self.findChildren(QLineEdit)
        for lineEdit in lineEdits:
            lineEdit.setFixedHeight(23)

        BlenderStyleSheet.COLORDIALOG.apply(self)