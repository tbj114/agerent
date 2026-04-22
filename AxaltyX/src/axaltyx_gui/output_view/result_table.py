from PyQt6.QtWidgets import (
    QTableView, QWidget, QVBoxLayout, QPushButton, QMenu, QFileDialog,
    QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QColor, QFont
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.axaltyx_i18n.manager import I18nManager


class ResultTableModel(QAbstractTableModel):
    """结果表格数据模型"""

    def __init__(self, data=None, headers=None):
        super().__init__()
        self._data = data if data is not None else []
        self._headers = headers if headers is not None else []

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0]) if self._data else 0

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[row][col]
            if isinstance(value, float):
                return f"{value:.4f}"
            return str(value)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        if role == Qt.ItemDataRole.BackgroundRole:
            if row % 2 == 0:
                return QColor("#F7F8FA")
            return QColor("#FFFFFF")

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                return self._headers[section] if section < len(self._headers) else ""
            if role == Qt.ItemDataRole.FontRole:
                font = QFont()
                font.setBold(True)
                return font

        if orientation == Qt.Orientation.Vertical:
            if role == Qt.ItemDataRole.DisplayRole:
                return str(section + 1)

        return None

    def setData(self, data, headers):
        self.beginResetModel()
        self._data = data
        self._headers = headers
        self.endResetModel()

    def toList(self):
        return self._data


class ResultTable(QWidget):
    """结果表格组件"""

    def __init__(self, data=None, headers=None, title=None):
        super().__init__()
        self.i18n = I18nManager()
        self._title = title if title is not None else self.i18n.get_text("dialog.analysis.title")
        self._init_ui()
        self.setData(data, headers)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # 标题和按钮行
        header_layout = QVBoxLayout()
        
        # 标题
        from PyQt6.QtWidgets import QLabel
        title_label = QLabel(self._title)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title_label.setFont(title_font)
        title_label.setStyleSheet("QLabel { color: #1D2129; padding: 8px 0; }")
        header_layout.addWidget(title_label)
        
        # 按钮行
        button_layout = QVBoxLayout()
        
        # 导出按钮
        self.export_button = QPushButton(self.i18n.get_text("dialog.file.save.title"))
        self.export_button.setMaximumWidth(100)
        self.export_button.clicked.connect(self._exportData)
        button_layout.addWidget(self.export_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        header_layout.addLayout(button_layout)
        
        layout.addLayout(header_layout)

        # 表格
        self.table = QTableView()
        self.table.setAlternatingRowColors(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(True)
        self.table.setStyleSheet("""
            QTableView {
                border: 1px solid #E5E6EB;
                border-radius: 4px;
                background-color: #FFFFFF;
                gridline-color: #E5E6EB;
            }
            QTableView::item {
                padding: 4px;
            }
            QHeaderView::section {
                background-color: #F2F3F5;
                color: #1D2129;
                padding: 6px;
                border: 1px solid #E5E6EB;
                font-weight: bold;
            }
        """)

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._showContextMenu)

        layout.addWidget(self.table)

        # 数据模型
        self._model = ResultTableModel()
        self.table.setModel(self._model)

    def setData(self, data, headers):
        """设置数据"""
        if data is not None and headers is not None:
            self._model.setData(data, headers)

    def _exportData(self):
        """导出数据"""
        menu = QMenu(self)
        
        csv_action = menu.addAction(self.i18n.get_text("dialog.file.save.title") + " CSV")
        csv_action.triggered.connect(lambda: self._saveCSV())
        
        excel_action = menu.addAction(self.i18n.get_text("dialog.file.save.title") + " Excel")
        excel_action.triggered.connect(lambda: self._saveExcel())
        
        menu.exec(self.mapToGlobal(self.export_button.geometry().bottomLeft()))

    def _saveCSV(self):
        """保存为CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.i18n.get_text("dialog.file.save.title"),
            "",
            "CSV Files (*.csv)"
        )
        
        if file_path:
            data = self._model.toList()
            if data:
                df = pd.DataFrame(data[1:], columns=data[0])
                df.to_csv(file_path, index=False, encoding='utf-8')

    def _saveExcel(self):
        """保存为Excel"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.i18n.get_text("dialog.file.save.title"),
            "",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            data = self._model.toList()
            if data:
                df = pd.DataFrame(data[1:], columns=data[0])
                df.to_excel(file_path, index=False)

    def _showContextMenu(self, position):
        """显示右键菜单"""
        menu = QMenu(self)
        
        copy_action = menu.addAction(self.i18n.get_text("dialog.file.save.title"))
        copy_action.triggered.connect(self._copySelection)
        
        menu.exec(self.table.mapToGlobal(position))

    def _copySelection(self):
        """复制选中内容"""
        selected_indexes = self.table.selectionModel().selectedIndexes()
        if not selected_indexes:
            return
        
        selection_data = {}
        for index in selected_indexes:
            row = index.row()
            col = index.column()
            if row not in selection_data:
                selection_data[row] = {}
            selection_data[row][col] = index.data()
        
        if selection_data:
            min_row = min(selection_data.keys())
            max_row = max(selection_data.keys())
            min_col = min([min(row_data.keys()) for row_data in selection_data.values()])
            max_col = max([max(row_data.keys()) for row_data in selection_data.values()])
            
            text = ""
            for row in range(min_row, max_row + 1):
                row_text = []
                for col in range(min_col, max_col + 1):
                    cell = selection_data.get(row, {}).get(col, "")
                    row_text.append(str(cell))
                text += "\t".join(row_text) + "\n"
            
            if text:
                from PyQt6.QtGui import QClipboard
                from PyQt6.QtWidgets import QApplication
                clipboard = QApplication.clipboard()
                clipboard.setText(text)
