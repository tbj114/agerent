from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import QTableView, QMenu, QApplication
from .model import DataTableModel
from .delegate import DataTableDelegate, HeaderDelegate

class AxaltyXDataTable(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_table()
    
    def init_table(self):
        # 设置模型
        self.model = DataTableModel()
        self.setModel(self.model)
        
        # 设置委托
        self.setItemDelegate(DataTableDelegate())
        self.horizontalHeader().setItemDelegate(HeaderDelegate())
        
        # 启用排序
        self.setSortingEnabled(True)
        
        # 启用编辑
        self.setEditTriggers(QTableView.EditTrigger.DoubleClicked | QTableView.EditTrigger.EditKeyPressed)
        
        # 启用选择
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectItems)
        self.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        
        # 设置网格线
        self.setShowGrid(True)
        self.setGridStyle(Qt.PenStyle.DotLine)
        
        # 设置列宽
        self.horizontalHeader().setDefaultSectionSize(100)
        
        # 启用右键菜单
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, pos):
        menu = QMenu(self)
        
        # 添加菜单项
        copy_action = menu.addAction("复制")
        paste_action = menu.addAction("粘贴")
        cut_action = menu.addAction("剪切")
        clear_action = menu.addAction("清除")
        
        # 连接信号
        copy_action.triggered.connect(self.copy)
        paste_action.triggered.connect(self.paste)
        cut_action.triggered.connect(self.cut)
        clear_action.triggered.connect(self.clear_selection)
        
        # 显示菜单
        menu.exec(self.mapToGlobal(pos))
    
    def copy(self):
        selection = self.selectedIndexes()
        if not selection:
            return
        
        # 按行和列排序
        selection.sort(key=lambda idx: (idx.row(), idx.column()))
        
        # 构建表格数据
        rows = {}
        for idx in selection:
            row = idx.row()
            col = idx.column()
            if row not in rows:
                rows[row] = {}
            rows[row][col] = idx.data() or ""
        
        # 转换为制表符分隔的文本
        text = ""
        for row in sorted(rows.keys()):
            cols = sorted(rows[row].keys())
            row_text = "\t".join(rows[row][col] for col in cols)
            text += row_text + "\n"
        
        # 复制到剪贴板
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
    
    def paste(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if not text:
            return
        
        # 获取当前选择的左上角
        selection = self.selectedIndexes()
        if not selection:
            return
        
        # 计算起始位置
        start_row = min(idx.row() for idx in selection)
        start_col = min(idx.column() for idx in selection)
        
        # 解析剪贴板数据
        rows = text.strip().split("\n")
        for i, row_text in enumerate(rows):
            cols = row_text.split("\t")
            for j, value in enumerate(cols):
                row = start_row + i
                col = start_col + j
                if row < self.model.rowCount() and col < self.model.columnCount():
                    index = self.model.index(row, col)
                    self.model.setData(index, value)
    
    def cut(self):
        self.copy()
        self.clear_selection()
    
    def clear_selection(self):
        for index in self.selectedIndexes():
            self.model.setData(index, "")
    
    def get_data(self):
        return self.model.get_dataframe()
    
    def set_data(self, df):
        return self.model.set_dataframe(df)
    
    def insert_rows(self, position, count):
        return self.model.insertRows(position, count)
    
    def remove_rows(self, position, count):
        return self.model.removeRows(position, count)
    
    def insert_columns(self, position, count):
        return self.model.insertColumns(position, count)
    
    def remove_columns(self, position, count):
        return self.model.removeColumns(position, count)
    
    def get_column_names(self):
        return self.model.column_names
    
    def set_column_name(self, column, name):
        return self.model.setHeaderData(column, Qt.Orientation.Horizontal, name)
    
    def get_row_count(self):
        return self.model.rowCount()
    
    def get_column_count(self):
        return self.model.columnCount()
    
    def clear_data(self):
        # 清空所有数据
        for row in range(self.model.rowCount()):
            for col in range(self.model.columnCount()):
                index = self.model.index(row, col)
                self.model.setData(index, "")
    
    def resize_columns_to_contents(self):
        self.horizontalHeader().resizeSections(QTableView.ResizeMode.ResizeToContents)
    
    def resize_rows_to_contents(self):
        self.verticalHeader().resizeSections(QTableView.ResizeMode.ResizeToContents)