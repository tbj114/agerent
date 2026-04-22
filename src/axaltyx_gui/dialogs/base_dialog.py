from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QScrollArea, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from axaltyx_i18n.manager import I18nManager
from axaltyx_gui.custom_widgets.variable_selector import AxaltyXVariableSelector

class AnalysisDialogBase(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('dialog.analysis.title'))
        self.setMinimumSize(800, 600)
        self.setModal(True)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(16)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        
        # 标题
        self.title_label = QLabel(self.i18n.get_text('dialog.analysis.title'))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.title_label.setFont(font)
        self.main_layout.addWidget(self.title_label)
        
        # 内容区域
        self.content_scroll = QScrollArea()
        self.content_scroll.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(16)
        self.content_scroll.setWidget(self.content_widget)
        self.main_layout.addWidget(self.content_scroll)
        
        # 变量选择器
        self.variable_selector = AxaltyXVariableSelector()
        self.content_layout.addWidget(self.variable_selector)
        
        # 选项区域
        self.options_frame = QFrame()
        self.options_layout = QVBoxLayout(self.options_frame)
        self.options_layout.setSpacing(12)
        self.content_layout.addWidget(self.options_frame)
        
        # 按钮区域
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(12)
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.ok_button = QPushButton(self.i18n.get_text('dialog.button.ok'))
        self.ok_button.setFixedWidth(100)
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton(self.i18n.get_text('dialog.button.cancel'))
        self.cancel_button.setFixedWidth(100)
        self.cancel_button.clicked.connect(self.reject)
        
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        
        self.main_layout.addLayout(self.button_layout)
    
    def get_selected_variables(self):
        return self.variable_selector.get_selected_variables()
    
    def get_options(self):
        return {}
    
    def accept(self):
        variables = self.get_selected_variables()
        if not variables:
            # 显示提示信息
            return
        super().accept()
