from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate, QStyleOptionViewItem, QStyle, QListView, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QColor, QFont, QPainter, QPen

from wblenderstylewidget.common.style_sheet import BlenderStyleSheet
from .widget_base import WidgetBaseSetting

class ComboBoxItemDelegate(QStyledItemDelegate):
    '''自定義元素樣式'''
    def __init__(self, parent=None):
        super(ComboBoxItemDelegate, self).__init__(parent)
        self.normal_color = QColor(0, 0, 0, 0)
        self.hover_color = QColor("#303030")
        self.selected_color = QColor("#4772b3")

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        option_copy = QStyleOptionViewItem(option)
        # HACK：暫定設定每個元素的高度
        option_copy.rect.setHeight(10)

        border_radius = 5

        if option.state & QStyle.StateFlag.State_MouseOver:
            fill_color = self.hover_color
        elif option.state & QStyle.StateFlag.State_Selected:
            fill_color = self.selected_color
        else:
            fill_color = self.normal_color

        fill_rect = option.rect.adjusted(0, 0, 0, 0)
        painter.setBrush(fill_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(fill_rect, border_radius, border_radius)

        # 繪製元素內容
        self.initStyleOption(option_copy, index)
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.setPen(QColor(Qt.GlobalColor.white))
        painter.drawText(option.rect.adjusted(5, 0, -5, 0), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, index.data(Qt.ItemDataRole.DisplayRole))

class ComboBox(QComboBox, WidgetBaseSetting):
    """ Custom combobox
        
        Parameters :
        ---------
            parent (QWidget): The parent widget. Default is None.

        Attributes :
        ---------
            text_label (QLabel): The label displaying the current selection text.

        Usage :
        ---------
            combo_box = ComboBox(parent)
    """
    def __init__(self, parent=None, **kwargs):
        super(ComboBox, self).__init__(parent=parent)

        self.setView(QListView())
        delegate = ComboBoxItemDelegate(self)
        self.setItemDelegate(delegate)

        self.text_label = QLabel(self)
        self.text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.text_label.setStyleSheet('color: #FFFFFF;')

        # 滑鼠進入和離開事件處理程序
        self.enterEvent = self.mouse_enter
        self.leaveEvent = self.mouse_leave
        self.is_mouse_over = False

        self.BaseSetting()

        BlenderStyleSheet.COMBOBOX.apply(self)

    def mouse_enter(self, event):
        self.is_mouse_over = True
        self.repaint()

    def mouse_leave(self, event):
        self.is_mouse_over = False
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        border_radius = 3
        padding = 0

        if self.is_mouse_over:
            fill_color = self.itemDelegate().hover_color
        else:
            fill_color = self.itemDelegate().normal_color

        if self.currentIndex() >= 0:
            fill_color = self.itemDelegate().selected_color

        fill_rect = rect.adjusted(padding, padding, -padding, -padding)
        painter.fillRect(fill_rect, fill_color)

        painter.setPen(QPen(QColor("#464646"), 0.5))

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawRoundedRect(fill_rect, border_radius, border_radius)

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect.adjusted(0, 0, 0, -self.view().height()), 10, 10)

        current_index = self.currentIndex()
        if current_index >= 0:
            current_text = self.itemText(current_index)
            self.text_label.setText(current_text)
            self.text_label.adjustSize()
            text_label_height = self.text_label.height()
            combobox_height = self.height()
            text_label_y = int((combobox_height - text_label_height) / 2)
            self.text_label.move(5, text_label_y)

    def showPopup(self):
        '''重寫 showPopup 方法,讓下拉式選單本身具有下半部圓角效果'''
        super().showPopup()
        self.view().setStyleSheet('border-bottom-left-radius: 3px; border-bottom-right-radius: 3px;')