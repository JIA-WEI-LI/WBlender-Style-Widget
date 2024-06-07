from PyQt5.QtWidgets import QScrollArea

from wblenderstylewidget.common.style_sheet import BlenderStyleSheet
from ..widgets.widget_base import WidgetBaseSetting

class ScrollArea(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        BlenderStyleSheet.SCROLLAREA.apply(self)