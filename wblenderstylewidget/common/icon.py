from PyQt5.QtGui import QIcon

class BlenderStyleIcon:
    CHECK = "wblenderstylewidget/resources/icons/icon_check.svg"
    CLOSE = "wblenderstylewidget/resources/icons/icon_close.svg"
    LEFTARROWHEAD = "wblenderstylewidget/resources/icons/icon_leftarrowhead.svg"
    RIGHTARROWHEAD = "wblenderstylewidget/resources/icons/icon_rightarrowhead.svg"
    SEARCH = "wblenderstylewidget/resources/icons/icon_search.svg"

    def __getattribute__(self, name):
        value = super(BlenderStyleIcon, self).__getattribute__(name)
        if name is not None:
            if isinstance(value, str):
                return QIcon(value)
            else:
                return value
        return value