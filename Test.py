import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from wblenderstylewidget import CheckBox

app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
window = QMainWindow()
check_box = CheckBox("This is a CheckBox!")
window.setStyleSheet("background-color: #303030; color: white;")
window.setCentralWidget(check_box)
window.show()
app.exec_()