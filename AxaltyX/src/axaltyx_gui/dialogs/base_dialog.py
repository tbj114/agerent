from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QGroupBox, QFormLayout, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from src.axaltyx_i18n.manager import I18nManager


class AnalysisDialogBase(QDialog):
    """分析对话框基类"""

    sig_execute = pyqtSignal(str, dict)  # analysis_name, params

    def __init__(self, analysis_name, parent=None):
        super().__init__(parent)
        self.analysis_name = analysis_name
        self.i18n = I18nManager()
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowTitleHint)
        self.setMinimumWidth(480)
        self.setFixedHeight(500)
        self.init_ui()

    def init_ui(self) -> None:
        """初始化UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # 标题
        title_label = QLabel(self.analysis_name)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # 变量选择器
        self.setup_variable_selector()
        main_layout.addWidget(self.variable_selector_widget)

        # 选项面板
        self.setup_options_panel()
        main_layout.addWidget(self.options_panel, 1)

        # 按钮组
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.reset_btn = QPushButton(self.i18n.get_text('dialog.reset'))
        self.reset_btn.clicked.connect(self.on_reset)

        self.cancel_btn = QPushButton(self.i18n.get_text('dialog.cancel'))
        self.cancel_btn.clicked.connect(self.reject)

        self.paste_btn = QPushButton(self.i18n.get_text('dialog.paste_syntax'))
        self.paste_btn.clicked.connect(self.on_paste_syntax)

        self.ok_btn = QPushButton(self.i18n.get_text('dialog.ok'))
        self.ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #165DFF;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #4080FF;
            }
        """)
        self.ok_btn.clicked.connect(self.on_execute)

        button_layout.addWidget(self.reset_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.paste_btn)
        button_layout.addWidget(self.ok_btn)

        main_layout.addLayout(button_layout)

    def setup_variable_selector(self) -> None:
        """设置变量选择器"""
        self.variable_selector_widget = QWidget()
        layout = QVBoxLayout(self.variable_selector_widget)
        
        group_box = QGroupBox(self.i18n.get_text('dialog.variable_selector.available'))
        group_layout = QFormLayout(group_box)
        
        # 这里将由子类实现具体的变量选择器
        label = QLabel("变量选择器将在子类中实现")
        group_layout.addRow(label)
        
        layout.addWidget(group_box)

    def setup_options_panel(self) -> None:
        """设置选项面板"""
        self.options_panel = QWidget()
        layout = QVBoxLayout(self.options_panel)
        
        group_box = QGroupBox("分析选项")
        group_layout = QFormLayout(group_box)
        
        # 这里将由子类实现具体的选项
        label = QLabel("分析选项将在子类中实现")
        group_layout.addRow(label)
        
        layout.addWidget(group_box)

    def get_parameters(self) -> dict:
        """获取分析参数
        
        Returns:
            dict: 分析参数
        """
        return {}

    def validate_inputs(self) -> tuple[bool, str]:
        """验证输入
        
        Returns:
            tuple[bool, str]: (是否有效, 错误信息)
        """
        return True, ""

    def on_execute(self) -> None:
        """执行分析"""
        is_valid, error_msg = self.validate_inputs()
        if not is_valid:
            print(f"Error: {error_msg}")
            return
        
        params = self.get_parameters()
        self.sig_execute.emit(self.analysis_name, params)
        self.accept()

    def on_paste_syntax(self) -> None:
        """粘贴语法"""
        # 子类可以实现具体的粘贴语法逻辑
        print("Paste syntax clicked")

    def on_reset(self) -> None:
        """重置选项"""
        # 子类可以实现具体的重置逻辑
        print("Reset clicked")
