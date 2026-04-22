from .base_dialog import AnalysisDialogBase
from src.axaltyx_gui.custom_widgets import AxaltyXVariableSelector
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QFormLayout, QComboBox, QLabel, QRadioButton, QButtonGroup
from PyQt6.QtCore import Qt


class CorrelationDialog(AnalysisDialogBase):
    """相关分析对话框"""

    def __init__(self, available_vars, parent=None):
        super().__init__("相关分析", parent)
        self.available_vars = available_vars
        self.selected_vars = []
        self.correlation_type = 'pearson'
        self.show_significance = True
        self.show_matrix = True
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
        
        # 相关类型
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("相关类型:"))
        
        self.correlation_type_group = QButtonGroup()
        
        self.pearson_radio = QRadioButton("Pearson 相关")
        self.pearson_radio.setChecked(True)
        self.correlation_type_group.addButton(self.pearson_radio)
        
        self.spearman_radio = QRadioButton("Spearman 秩相关")
        self.correlation_type_group.addButton(self.spearman_radio)
        
        self.kendall_radio = QRadioButton("Kendall's tau")
        self.correlation_type_group.addButton(self.kendall_radio)
        
        self.correlation_type_group.buttonClicked.connect(self._on_correlation_type_changed)
        
        type_layout.addWidget(self.pearson_radio)
        type_layout.addWidget(self.spearman_radio)
        type_layout.addWidget(self.kendall_radio)
        layout.addRow(type_layout)
        
        # 显示显著性
        self.significance_checkbox = QCheckBox("显示显著性")
        self.significance_checkbox.setChecked(True)
        layout.addRow(self.significance_checkbox)
        
        # 显示相关矩阵
        self.matrix_checkbox = QCheckBox("显示相关矩阵")
        self.matrix_checkbox.setChecked(True)
        layout.addRow(self.matrix_checkbox)
        
        # 置信水平
        layout.addRow("置信水平:")
        self.confidence_combo = QComboBox()
        self.confidence_combo.addItems(['90%', '95%', '99%'])
        layout.addRow(self.confidence_combo)

    def _on_variables_selected(self, variables):
        """变量选择变化处理"""
        self.selected_vars = variables

    def _on_correlation_type_changed(self, button):
        """相关类型变化处理"""
        if button == self.pearson_radio:
            self.correlation_type = 'pearson'
        elif button == self.spearman_radio:
            self.correlation_type = 'spearman'
        elif button == self.kendall_radio:
            self.correlation_type = 'kendall'

    def get_parameters(self) -> dict:
        """获取分析参数"""
        return {
            'correlation_type': self.correlation_type,
            'variables': self.selected_vars,
            'show_significance': self.significance_checkbox.isChecked(),
            'show_matrix': self.matrix_checkbox.isChecked(),
            'confidence_level': float(self.confidence_combo.currentText().replace('%', ''))
        }

    def validate_inputs(self) -> tuple[bool, str]:
        """验证输入"""
        if not self.selected_vars:
            return False, "请至少选择一个变量"
        if len(self.selected_vars) < 2:
            return False, "相关分析需要至少2个变量"
        return True, ""
