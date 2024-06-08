from PyQt5.QtWidgets import QApplication, QMainWindow
from wblenderstylewidget import RadioButtonGroup

app = QApplication([])
window = QMainWindow()
button_list = ["List 1", "List 2", "List 3"]
button_group = RadioButtonGroup(lists=button_list)
window.setCentralWidget(button_group)
window.show()
app.exec_()