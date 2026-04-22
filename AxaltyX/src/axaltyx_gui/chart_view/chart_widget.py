from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMenu, QFileDialog, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.axaltyx_i18n.manager import I18nManager


class ChartWidget(QWidget):
    """图表显示组件"""

    def __init__(self, figure=None, title=None):
        super().__init__()
        self.i18n = I18nManager()
        self._title = title if title is not None else self.i18n.get_text("dialog.analysis.title")
        self._figure = figure if figure is not None else Figure(figsize=(8, 6), dpi=100)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # 标题和按钮行
        header_layout = QVBoxLayout()
        
        # 标题
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
        self.export_button.clicked.connect(self._exportChart)
        button_layout.addWidget(self.export_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        header_layout.addLayout(button_layout)
        
        layout.addLayout(header_layout)

        # 图表区域
        chart_container = QWidget()
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(0, 0, 0, 0)

        # 画布
        self._canvas = FigureCanvas(self._figure)
        chart_layout.addWidget(self._canvas)

        # 工具栏
        self._toolbar = NavigationToolbar(self._canvas, self)
        self._toolbar.setStyleSheet("""
            QToolBar {
                border: none;
                spacing: 4px;
                background-color: #F7F8FA;
            }
            QToolButton {
                border: none;
                padding: 4px;
                border-radius: 4px;
            }
            QToolButton:hover {
                background-color: #E5E6EB;
            }
        """)
        chart_layout.addWidget(self._toolbar)

        layout.addWidget(chart_container)

        # 右键菜单
        self._canvas.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._canvas.customContextMenuRequested.connect(self._showContextMenu)

    def setFigure(self, figure):
        """设置图表"""
        self._figure = figure
        self._canvas.figure = self._figure
        self._canvas.draw()

    def getFigure(self):
        """获取图表"""
        return self._figure

    def setTitle(self, title):
        """设置标题"""
        self._title = title

    def _exportChart(self):
        """导出图表"""
        menu = QMenu(self)
        
        png_action = menu.addAction(self.i18n.get_text("dialog.file.save.title") + " PNG")
        png_action.triggered.connect(lambda: self._savePNG())
        
        jpg_action = menu.addAction(self.i18n.get_text("dialog.file.save.title") + " JPG")
        jpg_action.triggered.connect(lambda: self._saveJPG())
        
        pdf_action = menu.addAction(self.i18n.get_text("dialog.file.save.title") + " PDF")
        pdf_action.triggered.connect(lambda: self._savePDF())
        
        svg_action = menu.addAction(self.i18n.get_text("dialog.file.save.title") + " SVG")
        svg_action.triggered.connect(lambda: self._saveSVG())
        
        menu.exec(self.mapToGlobal(self.export_button.geometry().bottomLeft()))

    def _savePNG(self):
        """保存为PNG"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.i18n.get_text("dialog.file.save.title"),
            "",
            "PNG Files (*.png)"
        )
        
        if file_path:
            self._figure.savefig(file_path, dpi=300, bbox_inches='tight')

    def _saveJPG(self):
        """保存为JPG"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.i18n.get_text("dialog.file.save.title"),
            "",
            "JPG Files (*.jpg)"
        )
        
        if file_path:
            self._figure.savefig(file_path, dpi=300, bbox_inches='tight')

    def _savePDF(self):
        """保存为PDF"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.i18n.get_text("dialog.file.save.title"),
            "",
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            self._figure.savefig(file_path, dpi=300, bbox_inches='tight')

    def _saveSVG(self):
        """保存为SVG"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.i18n.get_text("dialog.file.save.title"),
            "",
            "SVG Files (*.svg)"
        )
        
        if file_path:
            self._figure.savefig(file_path, dpi=300, bbox_inches='tight')

    def _showContextMenu(self, position):
        """显示右键菜单"""
        menu = QMenu(self)
        
        export_action = menu.addAction(self.i18n.get_text("dialog.file.save.title"))
        export_action.triggered.connect(self._exportChart)
        
        menu.exec(self._canvas.mapToGlobal(position))
