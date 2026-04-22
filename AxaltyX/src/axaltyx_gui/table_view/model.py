from PyQt6.QtCore import QAbstractTableModel, Qt
import pandas as pd

class DataTableModel(QAbstractTableModel):
    """自定义数据模型，支持虚拟滚动"""

    def __init__(self, data: pd.DataFrame = None):
        super().__init__()
        if data is None:
            # 创建默认的 100x100 空表格
            data = pd.DataFrame()
            for i in range(100):
                col_name = f"VAR{i+1:05d}"
                data[col_name] = [None] * 100
        self.data = data

    def rowCount(self, parent=None):
        """获取行数"""
        return len(self.data)

    def columnCount(self, parent=None):
        """获取列数"""
        return len(self.data.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """获取单元格数据"""
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            value = self.data.iloc[row, col]
            return str(value) if value is not None else ""
        elif role == Qt.ItemDataRole.EditRole:
            return self.data.iloc[row, col]
        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        """设置单元格数据"""
        if role == Qt.ItemDataRole.EditRole:
            row = index.row()
            col = index.column()
            self.data.iloc[row, col] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        """获取表头数据"""
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.data.columns[section]
            else:
                return str(section + 1)
        return None

    def setHeaderData(self, section, orientation, value, role=Qt.ItemDataRole.EditRole):
        """设置表头数据"""
        if role == Qt.ItemDataRole.EditRole and orientation == Qt.Orientation.Horizontal:
            old_name = self.data.columns[section]
            self.data.rename(columns={old_name: value}, inplace=True)
            self.headerDataChanged.emit(orientation, section, section)
            return True
        return False

    def flags(self, index):
        """获取单元格标志"""
        return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def insertRows(self, position, rows, parent=None):
        """插入行"""
        self.beginInsertRows(parent, position, position + rows - 1)
        # 创建新行数据
        new_rows = pd.DataFrame([[None] * len(self.data.columns)], index=range(rows))
        new_rows.columns = self.data.columns
        # 插入到指定位置
        self.data = pd.concat([self.data.iloc[:position], new_rows, self.data.iloc[position:]], ignore_index=True)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=None):
        """删除行"""
        self.beginRemoveRows(parent, position, position + rows - 1)
        self.data = self.data.drop(self.data.index[position:position + rows])
        self.data.reset_index(drop=True, inplace=True)
        self.endRemoveRows()
        return True

    def insertColumns(self, position, columns, parent=None):
        """插入列"""
        self.beginInsertColumns(parent, position, position + columns - 1)
        # 创建新列数据
        for i in range(columns):
            col_name = f"VAR{len(self.data.columns) + i + 1:05d}"
            self.data[col_name] = [None] * len(self.data)
        # 重新排列列顺序
        cols = list(self.data.columns)
        new_cols = cols[:position] + cols[-columns:] + cols[position:-columns]
        self.data = self.data[new_cols]
        self.endInsertColumns()
        return True

    def removeColumns(self, position, columns, parent=None):
        """删除列"""
        self.beginRemoveColumns(parent, position, position + columns - 1)
        cols_to_remove = self.data.columns[position:position + columns]
        self.data.drop(cols_to_remove, axis=1, inplace=True)
        self.endRemoveColumns()
        return True

    def get_dataframe(self):
        """获取数据框"""
        return self.data

    def set_dataframe(self, data: pd.DataFrame):
        """设置数据框"""
        self.beginResetModel()
        self.data = data
        self.endResetModel()
