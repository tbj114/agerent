from PyQt6.QtWidgets import QWidget, QTableView, QVBoxLayout, QLabel, QLineEdit, QComboBox, QFormLayout, QGroupBox, QPushButton, QHBoxLayout
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
import pandas as pd

class VariableTab(QWidget):
    """变量视图标签页"""

    def __init__(self, data: pd.DataFrame = None):
        super().__init__()
        self.data = data
        self.variable_metadata = {}

        # 创建表格显示变量列表
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.selectionModel().selectionChanged.connect(self._on_variable_selected)

        # 创建变量属性编辑区域
        self.property_group = QGroupBox("变量属性")
        self.property_layout = QFormLayout()

        # 变量名
        self.var_name_label = QLabel("变量名:")
        self.var_name_edit = QLineEdit()
        self.property_layout.addRow(self.var_name_label, self.var_name_edit)

        # 变量类型
        self.var_type_label = QLabel("类型:")
        self.var_type_combo = QComboBox()
        self.var_type_combo.addItems(["数值", "字符串", "日期", "布尔"])
        self.property_layout.addRow(self.var_type_label, self.var_type_combo)

        # 宽度
        self.var_width_label = QLabel("宽度:")
        self.var_width_edit = QLineEdit("8")
        self.property_layout.addRow(self.var_width_label, self.var_width_edit)

        # 小数位
        self.var_decimals_label = QLabel("小数位:")
        self.var_decimals_edit = QLineEdit("2")
        self.property_layout.addRow(self.var_decimals_label, self.var_decimals_edit)

        # 标签
        self.var_label_label = QLabel("标签:")
        self.var_label_edit = QLineEdit()
        self.property_layout.addRow(self.var_label_label, self.var_label_edit)

        # 按钮
        self.button_layout = QHBoxLayout()
        self.apply_button = QPushButton("应用")
        self.apply_button.clicked.connect(self._on_apply)
        self.reset_button = QPushButton("重置")
        self.reset_button.clicked.connect(self._on_reset)
        self.button_layout.addWidget(self.apply_button)
        self.button_layout.addWidget(self.reset_button)
        self.property_layout.addRow(self.button_layout)

        self.property_group.setLayout(self.property_layout)

        # 主布局
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.table_view, 1)
        main_layout.addWidget(self.property_group, 1)

        if data is not None:
            self.set_data(data)

    def set_data(self, data: pd.DataFrame) -> None:
        """设置数据

        Args:
            data: 要显示的数据
        """
        self.data = data
        self._update_variable_list()
        # 初始化变量元数据
        for col in data.columns:
            if col not in self.variable_metadata:
                self.variable_metadata[col] = {
                    "name": col,
                    "type": "数值",
                    "width": 8,
                    "decimals": 2,
                    "label": ""
                }

    def get_variable_metadata(self) -> dict:
        """获取变量元数据

        Returns:
            dict: 变量元数据
        """
        return self.variable_metadata

    def set_variable_metadata(self, metadata: dict) -> None:
        """设置变量元数据

        Args:
            metadata: 变量元数据
        """
        self.variable_metadata = metadata
        self._update_variable_list()

    def _update_variable_list(self):
        """更新变量列表"""
        if self.data is None:
            return

        self.model.clear()
        self.model.setHorizontalHeaderLabels(["变量名", "类型", "宽度", "小数位", "标签"])

        for col in self.data.columns:
            meta = self.variable_metadata.get(col, {
                "name": col,
                "type": "数值",
                "width": 8,
                "decimals": 2,
                "label": ""
            })

            row = []
            row.append(QStandardItem(meta["name"]))
            row.append(QStandardItem(meta["type"]))
            row.append(QStandardItem(str(meta["width"])))
            row.append(QStandardItem(str(meta["decimals"])))
            row.append(QStandardItem(meta["label"]))

            for item in row:
                item.setEditable(False)

            self.model.appendRow(row)

    def _on_variable_selected(self, selected, deselected):
        """变量选择处理

        Args:
            selected: 选中的项
            deselected: 取消选中的项
        """
        indexes = selected.indexes()
        if indexes:
            row = indexes[0].row()
            var_name = self.model.item(row, 0).text()
            self._load_variable_properties(var_name)

    def _load_variable_properties(self, var_name):
        """加载变量属性

        Args:
            var_name: 变量名
        """
        meta = self.variable_metadata.get(var_name, {
            "name": var_name,
            "type": "数值",
            "width": 8,
            "decimals": 2,
            "label": ""
        })

        self.var_name_edit.setText(meta["name"])
        self.var_type_combo.setCurrentText(meta["type"])
        self.var_width_edit.setText(str(meta["width"]))
        self.var_decimals_edit.setText(str(meta["decimals"]))
        self.var_label_edit.setText(meta["label"])

    def _on_apply(self):
        """应用变量属性变更"""
        indexes = self.table_view.selectionModel().selectedIndexes()
        if indexes:
            row = indexes[0].row()
            old_var_name = self.model.item(row, 0).text()
            new_var_name = self.var_name_edit.text()

            # 更新元数据
            self.variable_metadata[new_var_name] = {
                "name": new_var_name,
                "type": self.var_type_combo.currentText(),
                "width": int(self.var_width_edit.text()),
                "decimals": int(self.var_decimals_edit.text()),
                "label": self.var_label_edit.text()
            }

            # 如果变量名变更，删除旧的元数据
            if old_var_name != new_var_name:
                del self.variable_metadata[old_var_name]
                # 更新数据框列名
                if old_var_name in self.data.columns:
                    self.data = self.data.rename(columns={old_var_name: new_var_name})

            # 更新变量列表
            self._update_variable_list()

    def _on_reset(self):
        """重置变量属性"""
        indexes = self.table_view.selectionModel().selectedIndexes()
        if indexes:
            row = indexes[0].row()
            var_name = self.model.item(row, 0).text()
            self._load_variable_properties(var_name)
