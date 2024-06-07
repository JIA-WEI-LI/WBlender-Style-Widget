import os
import sys
from PyQt5.QtWidgets import QScrollArea

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, grandparent_dir)

from common.style_sheet import BlenderStyleSheet
from ..widgets.widget_base import WidgetBaseSetting

class ScrollArea(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        BlenderStyleSheet.SCROLLAREA.apply(self)