from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QScrollArea, QPushButton, QHBoxLayout, QFileDialog
from PyQt6.QtGui import QTextDocument, QTextCursor
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.axaltyx_gui.output_view.output_widget import OutputWidget
from src.axaltyx_i18n.manager import I18nManager

class OutputTab(QWidget):
    """输出视图标签页"""

    def __init__(self):
        super().__init__()
        self.i18n = I18nManager()
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        # 按钮行
        button_layout = QHBoxLayout()
        
        # 清空按钮
        self.clear_button = QPushButton(self.i18n.get_text("dialog.analysis.clear"))
        self.clear_button.setMaximumWidth(100)
        self.clear_button.clicked.connect(self._on_clear)
        button_layout.addWidget(self.clear_button)
        
        # 导出按钮
        self.export_button = QPushButton(self.i18n.get_text("dialog.file.save.title"))
        self.export_button.setMaximumWidth(100)
        self.export_button.clicked.connect(self._on_export)
        button_layout.addWidget(self.export_button)
        
        button_layout.addStretch()
        
        # 示例按钮
        self.sample_button = QPushButton("加载示例")
        self.sample_button.setMaximumWidth(100)
        self.sample_button.clicked.connect(self._load_sample)
        button_layout.addWidget(self.sample_button)
        
        main_layout.addLayout(button_layout)

        # 输出组件
        self.output_widget = OutputWidget()
        main_layout.addWidget(self.output_widget)

    def _on_clear(self):
        """清空按钮点击处理"""
        self.output_widget._clearOutput()

    def append_result(self, result: dict) -> None:
        """添加分析结果

        Args:
            result: 分析结果
        """
        # 使用新的组件添加结果
        title = result.get('title', self.i18n.get_text("dialog.analysis.title"))
        content = ""
        if 'summary' in result:
            content += f"摘要: {result['summary']}\n"
        if 'details' in result:
            content += f"详细信息: {result['details']}\n"
        if 'statistics' in result:
            content += "统计结果:\n"
            for key, value in result['statistics'].items():
                content += f"  {key}: {value}\n"
                
        self.output_widget.addText(title, content)

    def append_table(self, table_data: dict) -> None:
        """添加表格

        Args:
            table_data: 表格数据
        """
        title = table_data.get('title', self.i18n.get_text("dialog.analysis.title"))
        
        if 'data' in table_data:
            df = pd.DataFrame(table_data['data'])
            headers = list(df.columns)
            data = [headers] + df.values.tolist()
        elif 'rows' in table_data and 'columns' in table_data:
            headers = table_data['columns']
            data = [headers] + table_data['rows']
        else:
            return
            
        self.output_widget.addResult(title, data, headers)

    def append_chart(self, figure, chart_id: str) -> None:
        """添加图表

        Args:
            figure: matplotlib 图表对象
            chart_id: 图表ID
        """
        title = self.i18n.get_text("dialog.analysis.chart") + ": " + chart_id
        self.output_widget.addChart(title, figure)

    def append_text(self, text: str, format: str = "plain") -> None:
        """添加文本

        Args:
            text: 文本内容
            format: 格式，可选 'plain' 或 'markdown'
        """
        self.output_widget.addText(self.i18n.get_text("dialog.analysis.title"), text)

    def clear_output(self) -> None:
        """清空输出（保留旧方法名）"""
        self._on_clear()

    def export_output(self, path: str, format: str) -> None:
        """导出输出

        Args:
            path: 导出路径
            format: 导出格式
        """
        # 使用新组件的导出功能
        self.output_widget._exportOutput()

    def _on_export(self):
        """导出按钮点击处理"""
        self.output_widget._exportOutput()

    def _load_sample(self):
        """加载示例数据"""
        self.output_widget.addSampleDescriptiveStatistics()
        self.output_widget.addSampleHistogram()
