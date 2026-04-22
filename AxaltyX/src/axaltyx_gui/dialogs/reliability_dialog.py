from .base_dialog import AnalysisDialogBase
from src.axaltyx_gui.custom_widgets import AxaltyXVariableSelector
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QFormLayout, QComboBox, QLabel, QRadioButton, QButtonGroup
from PyQt6.QtCore import Qt


class ReliabilityDialog(AnalysisDialogBase):
    """信度分析对话框"""

    def __init__(self, available_vars, parent=None):
        super().__init__("信度分析", parent)
        self.available_vars = available_vars
        self.selected_vars = []
        self.reliability_type = 'cronbach_alpha'
        self.show_item_stats = True
        self.show_summary = True
        # 重新初始化UI
        self.init_ui()

    def setup_variable_selector(self) -> None:
        """设置变量选择器"""
        self.variable_selector_widget = QGroupBox("变量")
        layout = QVBoxLayout(self.variable_selector_widget)
        
        self.variable_selector = AxaltyXVariableSelector(self.available_vars)
        self.variable_selector.sig_variables_selected.connect(self._on_variables_selected)
        layout.addWidget(self.variable_selector)

    def setup_options_panel(self) -> None:
        """设置选项面板"""
        self.options_panel = QGroupBox("选项")
        layout = QFormLayout(self.options_panel)
        
        # 信度类型
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("信度类型:"))
        
        self.reliability_type_group = QButtonGroup()
        
        self.cronbach_alpha_radio = QRadioButton("Cronbach's Alpha")
        self.cronbach_alpha_radio.setChecked(True)
        self.reliability_type_group.addButton(self.cronbach_alpha_radio)
        
        self.split_half_radio = QRadioButton("分半信度")
        self.reliability_type_group.addButton(self.split_half_radio)
        
        self.reliability_type_group.buttonClicked.connect(self._on_reliability_type_changed)
        
        type_layout.addWidget(self.cronbach_alpha_radio)
        type_layout.addWidget(self.split_half_radio)
        layout.addRow(type_layout)
        
        # 显示项目统计
        self.item_stats_checkbox = QCheckBox("显示项目统计")
        self.item_stats_checkbox.setChecked(True)
        layout.addRow(self.item_stats_checkbox)
        
        # 显示摘要
        self.summary_checkbox = QCheckBox("显示摘要")
        self.summary_checkbox.setChecked(True)
        layout.addRow(self.summary_checkbox)

    def _on_variables_selected(self, variables):
        """变量选择变化处理"""
        self.selected_vars = variables

    def _on_reliability_type_changed(self, button):
        """信度类型变化处理"""
        if button == self.cronbach_alpha_radio:
            self.reliability_type = 'cronbach_alpha'
        elif button == self.split_half_radio:
            self.reliability_type = 'split_half'

    def get_parameters(self) -> dict:
        """获取分析参数"""
        return {
            'reliability_type': self.reliability_type,
            'variables': self.selected_vars,
            'show_item_stats': self.item_stats_checkbox.isChecked(),
            'show_summary': self.summary_checkbox.isChecked()
        }

    def validate_inputs(self) -> tuple[bool, str]:
        """验证输入"""
        if not self.selected_vars:
            return False, "请至少选择一个变量"
        if len(self.selected_vars) < 3:
            return False, "信度分析需要至少3个变量"
        return True, ""
