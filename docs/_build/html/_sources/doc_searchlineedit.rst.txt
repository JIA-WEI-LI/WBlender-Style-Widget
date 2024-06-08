SearchLineEdit
===========================

.. automodule:: wblenderstylewidget.components.widgets.lineedit
   :members: SearchLineEdit
   :exclude-members: initWidget, initLayout
   :undoc-members: initWidget
   :show-inheritance:
   :noindex:

.. list-table::
   :header-rows: 1

   * - ATTRIBUTES
     - Type
     - Description
   * - ``hBoxLayout``
     - QHBoxLayout
     - A horizontal box layout used to arrange the child widgets in a horizontal line.
   * - ``search_button``
     - `PushButton <doc_pushbutton.html>`_
     - A custom push button configured with an icon for searching. It has a rounded corner on the left side and custom colors for different states (default, hover, press).
   * - ``search_linEdit``
     - `LineEdit <doc_lineedit.html>`_
     - A line edit widget for inputting search queries. It features a placeholder text that prompts the user to "Search".
   * - ``deleted_button``
     - `PushButton <doc_pushbutton.html>`_
     - A custom push button configured with a close icon to clear the search input. It has a rounded corner on the right side and custom colors for different states.