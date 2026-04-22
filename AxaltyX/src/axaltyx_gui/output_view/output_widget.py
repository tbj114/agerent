from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTreeWidget, 
    QTreeWidgetItem, QSplitter, QScrollArea, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from matplotlib.figure import Figure
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.axaltyx_i18n.manager import I18nManager
from .result_table import ResultTable
from ..chart_view.chart_widget import ChartWidget


class OutputWidget(QWidget):
    """输出视图组件，整合树形菜单和内容显示区域"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self._init_ui()
        self._items = []

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # 按钮行
        button_layout = QHBoxLayout()
        
        # 清空按钮
        self.clear_button = QPushButton(self.i18n.get_text("dialog.analysis.clear"))
        self.clear_button.setMaximumWidth(100)
        self.clear_button.clicked.connect(self._clearOutput)
        button_layout.addWidget(self.clear_button)
        
        # 导出按钮
        self.export_button = QPushButton(self.i18n.get_text("dialog.file.save.title"))
        self.export_button.setMaximumWidth(100)
        self.export_button.clicked.connect(self._exportOutput)
        button_layout.addWidget(self.export_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # 内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setWidget(content_widget)
        
        self._content_layout = content_layout
        layout.addWidget(self._scroll)

    def _clearOutput(self):
        """清空所有内容"""
        while self._content_layout.count() > 0:
            item = self._content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self._items = []

    def addResult(self, title, result_data, headers=None):
        """添加结果表格"""
        table = ResultTable(data=result_data, headers=headers, title=title)
        self._content_layout.addWidget(table)
        self._content_layout.addSpacing(16)
        self._items.append(table)

    def addChart(self, title, figure):
        """添加图表"""
        chart = ChartWidget(figure=figure, title=title)
        self._content_layout.addWidget(chart)
        self._content_layout.addSpacing(16)
        self._items.append(chart)

    def addText(self, title, text):
        """添加文本内容"""
        from PyQt6.QtWidgets import QLabel
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title_label.setFont(title_font)
        title_label.setStyleSheet("QLabel { color: #1D2129; padding: 8px 0; }")
        layout.addWidget(title_label)
        
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("QLabel { color: #4E5969; padding: 4px 0; }")
        layout.addWidget(text_label)
        
        self._content_layout.addWidget(widget)
        self._content_layout.addSpacing(16)
        self._items.append(widget)

    def _exportOutput(self):
        """导出整个输出"""
        QMessageBox.information(self, 
            self.i18n.get_text("dialog.analysis.title"), 
            "导出功能正在开发中")

    def addSampleDescriptiveStatistics(self):
        """添加示例描述性统计结果"""
        headers = ["变量", "N", "均值", "标准差", "最小值", "最大值"]
        data = [
            ["VAR00001", 100, 23.45, 4.32, 12.34, 45.67],
            ["VAR00002", 100, 67.89, 12.11, 34.56, 98.76],
            ["VAR00003", 98, 14.56, 3.21, 5.43, 28.76],
            ["VAR00004", 100, 89.32, 5.43, 67.89, 99.99]
        ]
        
        self.addResult(self.i18n.get_text("analysis.descriptive.title"), data, headers)

    def addSampleHistogram(self):
        """添加示例直方图"""
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.hist(np.random.normal(50, 10, 1000), bins=30)
        ax.set_title(self.i18n.get_text("dialog.analysis.chart"))
        ax.set_xlabel("值")
        ax.set_ylabel("频率")
        fig.tight_layout()
        
        self.addChart(self.i18n.get_text("dialog.analysis.chart"), fig)
