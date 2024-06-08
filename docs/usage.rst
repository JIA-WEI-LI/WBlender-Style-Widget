Usage
=====

Here are some examples of how to use the WBlender-Style-Widget components:

Basic Example
-------------

.. code-block:: python

    from PyQt5.QtWidgets import QApplication, QMainWindow
    from wblenderstylewidget.components.layout.scrollarea import ScrollArea

    app = QApplication([])
    window = QMainWindow()
    scroll_area = ScrollArea()
    window.setCentralWidget(scroll_area)
    window.show()
    app.exec_()

Advanced Example
----------------

.. code-block:: python

    # Add your advanced usage examples here