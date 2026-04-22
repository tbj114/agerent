from .base_dialog import AnalysisDialogBase
from src.axaltyx_gui.custom_widgets import AxaltyXVariableSelector
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QFormLayout, QComboBox, QLabel, QRadioButton, QButtonGroup
from PyQt6.QtCore import Qt


class NonparametricDialog(AnalysisDialogBase):
    """非参数检验对话框"""

    def __init__(self, available_vars, parent=None):
        super().__init__("非参数检验", parent)
        self.available_vars = available_vars
        self.selected_vars = []
        self.test_type = 'mann_whitney'
        self.group_var = []
        # 重新初始化UI
        self.init_ui()

    def setup_variable_selector(self) -> None:
        """设置变量选择器"""
        self.variable_selector_widget = QGroupBox("变量")
        layout = QVBoxLayout(self.variable_selector_widget)
        
        # 检验变量
        test_var_layout = QVBoxLayout()
        test_var_layout.addWidget(QLabel("检验变量:"))
        self.test_selector = AxaltyXVariableSelector(self.available_vars)
        self.test_selector.sig_variables_selected.connect(self._on_test_variables_selected)
        test_var_layout.addWidget(self.test_selector)
        layout.addLayout(test_var_layout)
        
        # 分组变量
        group_var_layout = QVBoxLayout()
        group_var_layout.addWidget(QLabel("分组变量:"))
        self.group_selector = AxaltyXVariableSelector(self.available_vars)
        self.group_selector.sig_variables_selected.connect(self._on_group_variable_selected)
        group_var_layout.addWidget(self.group_selector)
        layout.addLayout(group_var_layout)
        
        # 检验类型
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("检验类型:"))
        
        self.test_type_group = QButtonGroup()
        
        self.mann_whitney_radio = QRadioButton("Mann-Whitney U 检验")
        self.mann_whitney_radio.setChecked(True)
        self.test_type_group.addButton(self.mann_whitney_radio)
        
        self.wilcoxon_radio = QRadioButton("Wilcoxon 符号秩检验")
        self.test_type_group.addButton(self.wilcoxon_radio)
        
        self.kruskal_wallis_radio = QRadioButton("Kruskal-Wallis 检验")
        self.test_type_group.addButton(self.kruskal_wallis_radio)
        
        self.friedman_radio = QRadioButton("Friedman 检验")
        self.test_type_group.addButton(self.friedman_radio)
        
        self.test_type_group.buttonClicked.connect(self._on_test_type_changed)
        
        type_layout.addWidget(self.mann_whitney_radio)
        type_layout.addWidget(self.wilcoxon_radio)
        type_layout.addWidget(self.kruskal_wallis_radio)
        type_layout.addWidget(self.friedman_radio)
        layout.addLayout(type_layout)

    def setup_options_panel(self) -> None:
        """设置选项面板"""
        self.options_panel = QGroupBox("选项")
        layout = QFormLayout(self.options_panel)
        
        # 显示描述统计
        self.descriptive_checkbox = QCheckBox("显示描述统计")
        self.descriptive_checkbox.setChecked(True)
        layout.addRow(self.descriptive_checkbox)
        
        # 显示秩和
        self.ranks_checkbox = QCheckBox("显示秩和")
        self.ranks_checkbox.setChecked(True)
        layout.addRow(self.ranks_checkbox)
        
        # 显示效应量
        self.effect_size_checkbox = QCheckBox("显示效应量")
        self.effect_size_checkbox.setChecked(False)
        layout.addRow(self.effect_size_checkbox)

    def _on_test_variables_selected(self, variables):
        """检验变量选择变化处理"""
        self.selected_vars = variables

    def _on_group_variable_selected(self, variables):
        """分组变量选择变化处理"""
        self.group_var = variables

    def _on_test_type_changed(self, button):
        """检验类型变化处理"""
        if button == self.mann_whitney_radio:
            self.test_type = 'mann_whitney'
        elif button == self.wilcoxon_radio:
            self.test_type = 'wilcoxon'
        elif button == self.kruskal_wallis_radio:
            self.test_type = 'kruskal_wallis'
        elif button == self.friedman_radio:
            self.test_type = 'friedman'

    def get_parameters(self) -> dict:
        """获取分析参数"""
        return {
            'test_type': self.test_type,
            'variables': self.selected_vars,
            'group_variable': self.group_var,
            'show_descriptive': self.descriptive_checkbox.isChecked(),
            'show_ranks': self.ranks_checkbox.isChecked(),
            'show_effect_size': self.effect_size_checkbox.isChecked()
        }

    def validate_inputs(self) -> tuple[bool, str]:
        """验证输入"""
        if not self.selected_vars:
            return False, "请至少选择一个检验变量"
        if not self.group_var and self.test_type in ['mann_whitney', 'kruskal_wallis']:
            return False, "请选择一个分组变量"
        return True, ""
