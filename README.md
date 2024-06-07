# Blender Style PyQt5 Components

This project consists of custom PyQt5 components inspired by the internal components of Blender. These components have been redesigned and restyled to mimic Blender's unique appearance and functionality.

## Features

- **Blender-style design**: The components are styled to resemble Blender's internal UI elements.
- **Custom components**: Various custom components have been created, including buttons, switches, and line edits, each with enhanced functionality.
- **PyQt5 based**: Built using PyQt5, ensuring compatibility with PyQt5 applications.

## Components

### PushButton

A custom QPushButton with additional features such as configurable corner radius, hover and press states, and support for both text and icon.

### ToggleButton

Extends PushButton to add toggle functionality. The button will change state (pressed or not pressed) when clicked.

### RadioButton

Extends PushButton to add radio button functionality. The button will behave like a radio button, being part of a mutually exclusive group of buttons.

### RatioButtonGroup

A custom QWidget that creates a group of radio buttons arranged horizontally. Each button can have configurable corner radius and initial selection.

### SearchLineEdit

A custom QWidget that combines a search button, a line edit, and a delete button into a single widget. This widget is styled for search functionality with clear and focus events handling.

### ListWidget

A custom QListWidget with additional styling and functionalities such as adding separators and removing selected items.

### SwitchButton

A custom switch button widget that includes an indicator and a label with text. The button can toggle its state between checked and unchecked.

## Installation

To install and use these custom components in your project, you need to have PyQt5 installed. You can install PyQt5 using pip:

Clone this repository to your local machine:

```git
git clone https://github.com/JIA-WEI-LI/WBlender-Style-Widget.git
```

## Usage

Below is an example of how to use the PushButton component in a PyQt5 application:
```python
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from wblenderstylewidget import *

app = QApplication([])

window = QWidget()
layout = QVBoxLayout()

push_button = PushButton(text="Click Me", icon="path/to/icon.png", corner_radius=5)
layout.addWidget(push_button)

window.setLayout(layout)
window.show()

app.exec_()
```

### Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome all contributions!

### License

This project is licensed under the MIT License. See the LICENSE file for more information.

### Acknowledgements

* Blender for the inspiration behind the UI design.
* The PyQt5 library for providing the tools to create these custom components.
  
---

Feel free to modify this README.md template to better fit your project. If you have any questions or need further assistance, please don't hesitate to ask.