from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
import pandas as pd

class DataTableModel(QAbstractTableModel):
    def __init__(self, rows=100, columns=100, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.columns = columns
        self.column_names = [f"VAR{i:05d}" for i in range(1, columns + 1)]
        self.data = pd.DataFrame(index=range(rows), columns=self.column_names)
    
    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return self.rows
    
    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return self.columns
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        row = index.row()
        col = index.column()
        
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            value = self.data.iloc[row, col]
            return str(value) if pd.notna(value) else ""
        
        return None
    
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False
        
        row = index.row()
        col = index.column()
        
        try:
            # 尝试转换为适当的数据类型
            if value == "":
                self.data.iloc[row, col] = pd.NA
            else:
                # 尝试转换为数字
                try:
                    value = float(value)
                    if value.is_integer():
                        value = int(value)
                except ValueError:
                    pass
                self.data.iloc[row, col] = value
            
            self.dataChanged.emit(index, index, [role])
            return True
        except Exception:
            return False
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        
        if orientation == Qt.Orientation.Horizontal:
            if 0 <= section < self.columns:
                return self.column_names[section]
        else:  # Vertical
            return str(section + 1)
    
    def setHeaderData(self, section, orientation, value, role=Qt.ItemDataRole.EditRole):
        if role != Qt.ItemDataRole.EditRole or orientation != Qt.Orientation.Horizontal:
            return False
        
        if 0 <= section < self.columns:
            self.column_names[section] = value
            self.headerDataChanged.emit(orientation, section, section)
            return True
        return False
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled
    
    def insertRows(self, position, rows, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        self.rows += rows
        # 扩展数据
        new_rows = pd.DataFrame(index=range(rows), columns=self.column_names)
        self.data = pd.concat([self.data.iloc[:position], new_rows, self.data.iloc[position:]]).reset_index(drop=True)
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows, parent=QModelIndex()):
        if self.rows <= rows:
            return False
        
        self.beginRemoveRows(parent, position, position + rows - 1)
        self.rows -= rows
        # 移除数据
        self.data = self.data.drop(self.data.index[position:position+rows]).reset_index(drop=True)
        self.endRemoveRows()
        return True
    
    def insertColumns(self, position, columns, parent=QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        self.columns += columns
        # 生成新列名
        start_idx = len(self.column_names) + 1
        new_columns = [f"VAR{i:05d}" for i in range(start_idx, start_idx + columns)]
        self.column_names = self.column_names[:position] + new_columns + self.column_names[position:]
        # 扩展数据
        for col in new_columns:
            self.data[col] = pd.NA
        self.endInsertColumns()
        return True
    
    def removeColumns(self, position, columns, parent=QModelIndex()):
        if self.columns <= columns:
            return False
        
        self.beginRemoveColumns(parent, position, position + columns - 1)
        self.columns -= columns
        # 移除列
        cols_to_remove = self.column_names[position:position+columns]
        self.data = self.data.drop(cols_to_remove, axis=1)
        self.column_names = self.column_names[:position] + self.column_names[position+columns:]
        self.endRemoveColumns()
        return True
    
    def get_dataframe(self):
        return self.data.copy()
    
    def set_dataframe(self, df):
        self.beginResetModel()
        self.data = df.copy()
        self.rows, self.columns = df.shape
        self.column_names = list(df.columns)
        self.endResetModel()
        return True