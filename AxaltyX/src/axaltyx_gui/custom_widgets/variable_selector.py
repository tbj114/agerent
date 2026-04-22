from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from src.axaltyx_i18n.manager import I18nManager


class AxaltyXVariableSelector(QWidget):
    """变量选择器（分析对话框中的双列表）"""

    sig_variables_selected = pyqtSignal(list[str])

    def __init__(self, available_vars: list[str], parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.available_vars = available_vars
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)

        # 可用变量列表
        available_layout = QVBoxLayout()
        available_label = QLabel(self.i18n.get_text('dialog.variable_selector.available'))
        available_label.setFont(QFont('', 10, QFont.Weight.Medium))
        available_layout.addWidget(available_label)

        self.available_list = QListWidget()
        self.available_list.addItems(self.available_vars)
        self.available_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        available_layout.addWidget(self.available_list, 1)

        # 按钮组
        button_layout = QVBoxLayout()
        button_layout.setSpacing(8)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.move_right_btn = QPushButton('>')
        self.move_right_btn.setFixedWidth(30)
        self.move_right_btn.clicked.connect(self.move_to_selected)

        self.move_left_btn = QPushButton('<')
        self.move_left_btn.setFixedWidth(30)
        self.move_left_btn.clicked.connect(self.move_to_available)

        self.move_all_right_btn = QPushButton('>>')
        self.move_all_right_btn.setFixedWidth(30)
        self.move_all_right_btn.clicked.connect(self.move_all_to_selected)

        self.move_all_left_btn = QPushButton('<<')
        self.move_all_left_btn.setFixedWidth(30)
        self.move_all_left_btn.clicked.connect(self.move_all_to_available)

        button_layout.addWidget(self.move_right_btn)
        button_layout.addWidget(self.move_left_btn)
        button_layout.addWidget(self.move_all_right_btn)
        button_layout.addWidget(self.move_all_left_btn)

        # 已选变量列表
        selected_layout = QVBoxLayout()
        selected_label = QLabel(self.i18n.get_text('dialog.variable_selector.selected'))
        selected_label.setFont(QFont('', 10, QFont.Weight.Medium))
        selected_layout.addWidget(selected_label)

        self.selected_list = QListWidget()
        self.selected_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        selected_layout.addWidget(self.selected_list, 1)

        # 组装布局
        main_layout.addLayout(available_layout, 1)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(selected_layout, 1)

    def set_available_variables(self, vars: list[str]) -> None:
        """设置可用变量列表
        
        Args:
            vars: 可用变量列表
        """
        self.available_list.clear()
        self.available_list.addItems(vars)
        self.available_vars = vars

    def get_selected_variables(self) -> list[str]:
        """获取已选变量
        
        Returns:
            list[str]: 已选变量列表
        """
        selected = []
        for i in range(self.selected_list.count()):
            selected.append(self.selected_list.item(i).text())
        return selected

    def move_to_selected(self) -> None:
        """将选中的变量移到已选列表"""
        selected_items = self.available_list.selectedItems()
        for item in selected_items:
            self.selected_list.addItem(item.text())
            self.available_list.takeItem(self.available_list.row(item))
        self.sig_variables_selected.emit(self.get_selected_variables())

    def move_to_available(self) -> None:
        """将选中的变量移回可用列表"""
        selected_items = self.selected_list.selectedItems()
        for item in selected_items:
            self.available_list.addItem(item.text())
            self.selected_list.takeItem(self.selected_list.row(item))
        self.sig_variables_selected.emit(self.get_selected_variables())

    def move_all_to_selected(self) -> None:
        """将所有变量移到已选列表"""
        while self.available_list.count() > 0:
            item = self.available_list.takeItem(0)
            self.selected_list.addItem(item.text())
        self.sig_variables_selected.emit(self.get_selected_variables())

    def move_all_to_available(self) -> None:
        """将所有变量移回可用列表"""
        while self.selected_list.count() > 0:
            item = self.selected_list.takeItem(0)
            self.available_list.addItem(item.text())
        self.sig_variables_selected.emit(self.get_selected_variables())
