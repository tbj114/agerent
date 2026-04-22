from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QScrollArea, QPushButton, QHBoxLayout, QFileDialog
from PyQt6.QtGui import QTextDocument, QTextCursor
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

class OutputTab(QWidget):
    """输出视图标签页"""

    def __init__(self):
        super().__init__()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.content_widget)

        # 清空按钮
        self.clear_button = QPushButton("清空输出")
        self.clear_button.clicked.connect(self.clear_output)

        # 导出按钮
        self.export_button = QPushButton("导出")
        self.export_button.clicked.connect(self._on_export)

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.export_button)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.scroll_area)

    def append_result(self, result: dict) -> None:
        """添加分析结果

        Args:
            result: 分析结果
        """
        # 创建结果文本
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("QTextEdit { border: 1px solid #E5E6EB; border-radius: 4px; padding: 8px; margin-bottom: 8px; }")

        # 构建结果文本
        content = f"# {result.get('title', '分析结果')}\n\n"
        if 'summary' in result:
            content += f"## 摘要\n{result['summary']}\n\n"
        if 'details' in result:
            content += f"## 详细信息\n{result['details']}\n\n"
        if 'statistics' in result:
            content += "## 统计结果\n"
            for key, value in result['statistics'].items():
                content += f"- {key}: {value}\n"
            content += "\n"

        text_edit.setMarkdown(content)
        self.content_layout.addWidget(text_edit)

    def append_table(self, table_data: dict) -> None:
        """添加表格

        Args:
            table_data: 表格数据
        """
        # 创建表格文本
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("QTextEdit { border: 1px solid #E5E6EB; border-radius: 4px; padding: 8px; margin-bottom: 8px; }")

        # 构建表格文本
        content = f"# {table_data.get('title', '表格')}\n\n"
        
        if 'data' in table_data:
            df = pd.DataFrame(table_data['data'])
            # 转换为 markdown 表格
            content += df.to_markdown(index=False)
        elif 'rows' in table_data and 'columns' in table_data:
            # 构建简单表格
            content += "| " + " | ".join(table_data['columns']) + " |\n"
            content += "| " + " | ".join(["---"] * len(table_data['columns'])) + " |\n"
            for row in table_data['rows']:
                content += "| " + " | ".join(map(str, row)) + " |\n"

        text_edit.setMarkdown(content)
        self.content_layout.addWidget(text_edit)

    def append_chart(self, figure, chart_id: str) -> None:
        """添加图表

        Args:
            figure: matplotlib 图表对象
            chart_id: 图表ID
        """
        # 创建图表容器
        chart_widget = QWidget()
        chart_layout = QVBoxLayout(chart_widget)
        chart_layout.setContentsMargins(0, 0, 0, 0)

        # 添加图表标题
        from PyQt6.QtWidgets import QLabel
        title_label = QLabel(f"图表: {chart_id}")
        title_label.setStyleSheet("QLabel { font-weight: bold; margin-bottom: 4px; }")
        chart_layout.addWidget(title_label)

        # 创建画布
        canvas = FigureCanvas(figure)
        chart_layout.addWidget(canvas)

        self.content_layout.addWidget(chart_widget)

    def append_text(self, text: str, format: str = "plain") -> None:
        """添加文本

        Args:
            text: 文本内容
            format: 格式，可选 'plain' 或 'markdown'
        """
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("QTextEdit { border: 1px solid #E5E6EB; border-radius: 4px; padding: 8px; margin-bottom: 8px; }")

        if format == "markdown":
            text_edit.setMarkdown(text)
        else:
            text_edit.setPlainText(text)

        self.content_layout.addWidget(text_edit)

    def clear_output(self) -> None:
        """清空输出"""
        # 移除所有子组件
        while self.content_layout.count() > 0:
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def export_output(self, path: str, format: str) -> None:
        """导出输出

        Args:
            path: 导出路径
            format: 导出格式
        """
        if format == "txt":
            # 导出为文本文件
            content = ""
            for i in range(self.content_layout.count()):
                widget = self.content_layout.itemAt(i).widget()
                if isinstance(widget, QTextEdit):
                    content += widget.toPlainText() + "\n\n"
                elif hasattr(widget, "layout"):
                    # 处理图表容器
                    layout = widget.layout()
                    for j in range(layout.count()):
                        child_widget = layout.itemAt(j).widget()
                        if isinstance(child_widget, QTextEdit):
                            content += child_widget.toPlainText() + "\n\n"

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        elif format == "html":
            # 导出为 HTML 文件
            content = "<html><body>"
            for i in range(self.content_layout.count()):
                widget = self.content_layout.itemAt(i).widget()
                if isinstance(widget, QTextEdit):
                    content += widget.toHtml() + "<br><br>"

            content += "</body></html>"
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

    def _on_export(self):
        """导出按钮点击处理"""
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilters(["Text Files (*.txt)", "HTML Files (*.html)"])
        file_dialog.setDefaultSuffix("txt")

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            file_filter = file_dialog.selectedNameFilter()

            if "Text Files" in file_filter:
                self.export_output(file_path, "txt")
            elif "HTML Files" in file_filter:
                self.export_output(file_path, "html")
