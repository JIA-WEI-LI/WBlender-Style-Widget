ProgressBarSlider
===========================

.. automodule:: wblenderstylewidget.components.widgets.slider
   :members: ProgressBarSlider
   :exclude-members: innerSetting, paintEvent
   :undoc-members: innerSetting
   :show-inheritance:
   :noindex:

.. list-table::
   :header-rows: 1

   * - ATTRIBUTES
     - Type
     - Description
   * - ``apply_style``
     - bool
     - A flag indicating whether additional styles have been applied to the widget.
   * - ``color``
     - str
     - The color used for the progress bar's fill.
   * - ``decimal_places``
     - int
     - The number of decimal places to use when displaying the progress value.
   * - ``initial_value``
     - Union[float, int]
     - The initial value set on the progress bar during instantiation. It accepts either a percentage as a float or an absolute value as an integer.
   * - ``isDragging``
     - bool
     - A flag that indicates whether the user is currently dragging the progress bar slider to change its value.
   * - ``isEnter``
     - bool
     - A flag that indicates whether the mouse cursor is inside the widget's area.
   * - ``maximum``
     - int
     - The maximum value that the progress bar can represent.
   * - ``minimum``
     - int
     - The minimum value that the progress bar can represent.
   * - ``text``
     - str
     - The text displayed on the progress bar, indicating the value or other information.