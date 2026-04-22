from PyQt6.QtWidgets import QWidget, QTableView, QVBoxLayout
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
import pandas as pd

class DataTab(QWidget):
    """数据视图标签页，包含表格"""

    def __init__(self, data: pd.DataFrame = None):
        super().__init__()
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)

        # 存储原始数据和修改后的数据
        self.original_data = None
        self.current_data = None
        self.modified = False

        # 撤销/重做栈
        self.undo_stack = []
        self.redo_stack = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.table_view)

        if data is not None:
            self.set_data(data)
        else:
            # 创建默认的 100x100 空表格
            self._create_default_table()

    def _create_default_table(self):
        """创建默认的 100x100 空表格"""
        data = pd.DataFrame()
        for i in range(100):
            col_name = f"VAR{i+1:05d}"
            data[col_name] = [None] * 100
        self.set_data(data)

    def set_data(self, data: pd.DataFrame) -> None:
        """设置数据

        Args:
            data: 要显示的数据
        """
        self.original_data = data.copy()
        self.current_data = data.copy()
        self.modified = False
        self.undo_stack = []
        self.redo_stack = []

        # 更新表格模型
        self.model.clear()

        # 设置列标题
        self.model.setHorizontalHeaderLabels(data.columns.tolist())

        # 设置行标题
        self.model.setVerticalHeaderLabels([str(i+1) for i in range(len(data))])

        # 填充数据
        for row_idx, row in data.iterrows():
            for col_idx, value in enumerate(row):
                item = QStandardItem(str(value) if value is not None else "")
                item.setData(value, Qt.ItemDataRole.UserRole)
                self.model.setItem(row_idx, col_idx, item)

        # 连接单元格变更信号
        self.model.itemChanged.connect(self._on_item_changed)

    def get_data(self) -> pd.DataFrame:
        """获取当前数据

        Returns:
            pd.DataFrame: 当前数据
        """
        return self.current_data

    def get_modified_data(self) -> pd.DataFrame:
        """获取修改后的数据

        Returns:
            pd.DataFrame: 修改后的数据
        """
        if self.modified:
            return self.current_data
        else:
            return self.original_data

    def is_modified(self) -> bool:
        """检查数据是否被修改

        Returns:
            bool: 是否被修改
        """
        return self.modified

    def undo(self) -> None:
        """撤销操作"""
        if self.undo_stack:
            # 保存当前状态到重做栈
            self.redo_stack.append(self.current_data.copy())
            # 恢复上一个状态
            previous_data = self.undo_stack.pop()
            self.set_data(previous_data)
            self.modified = len(self.undo_stack) > 0

    def redo(self) -> None:
        """重做操作"""
        if self.redo_stack:
            # 保存当前状态到撤销栈
            self.undo_stack.append(self.current_data.copy())
            # 恢复下一个状态
            next_data = self.redo_stack.pop()
            self.set_data(next_data)
            self.modified = True

    def _on_item_changed(self, item):
        """单元格变更处理

        Args:
            item: 变更的单元格
        """
        row = item.row()
        col = item.column()
        col_name = self.current_data.columns[col]

        # 保存当前状态到撤销栈
        self.undo_stack.append(self.current_data.copy())
        # 清空重做栈
        self.redo_stack = []

        # 更新数据
        try:
            value = float(item.text()) if item.text() else None
        except ValueError:
            value = item.text() if item.text() else None

        self.current_data.iloc[row, col] = value
        item.setData(value, Qt.ItemDataRole.UserRole)
        self.modified = True
