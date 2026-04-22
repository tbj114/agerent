from .base_dialog import AnalysisDialogBase
from src.axaltyx_gui.custom_widgets import AxaltyXVariableSelector
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QFormLayout, QLabel
from PyQt6.QtCore import Qt


class CrosstabsDialog(AnalysisDialogBase):
    """交叉表对话框"""

    def __init__(self, available_vars, parent=None):
        super().__init__("交叉表", parent)
        self.available_vars = available_vars
        self.row_vars = []
        self.column_vars = []
        self.options = {
            'chi_square': True,
            'phi_and_cramer_v': False,
            'contingency_coefficient': False,
            'lambda': False,
            'gamma': False,
            'kendall_tau_b': False,
            'kendall_tau_c': False,
            'spearman_rho': False
        }
        # 重新初始化UI
        self.init_ui()

    def setup_variable_selector(self) -> None:
        """设置变量选择器"""
        self.variable_selector_widget = QGroupBox("变量")
        layout = QVBoxLayout(self.variable_selector_widget)
        
        # 行变量
        row_layout = QVBoxLayout()
        row_layout.addWidget(QLabel("行变量:"))
        self.row_selector = AxaltyXVariableSelector(self.available_vars)
        self.row_selector.sig_variables_selected.connect(self._on_row_variables_selected)
        row_layout.addWidget(self.row_selector)
        layout.addLayout(row_layout)
        
        # 列变量
        col_layout = QVBoxLayout()
        col_layout.addWidget(QLabel("列变量:"))
        self.column_selector = AxaltyXVariableSelector(self.available_vars)
        self.column_selector.sig_variables_selected.connect(self._on_column_variables_selected)
        col_layout.addWidget(self.column_selector)
        layout.addLayout(col_layout)

    def setup_options_panel(self) -> None:
        """设置选项面板"""
        self.options_panel = QGroupBox("统计量")
        layout = QFormLayout(self.options_panel)
        
        # 统计量复选框
        self.option_checkboxes = {}
        for option, default in self.options.items():
            checkbox = QCheckBox(self._get_option_label(option))
            checkbox.setChecked(default)
            self.option_checkboxes[option] = checkbox
            layout.addRow(checkbox)

    def _on_row_variables_selected(self, variables):
        """行变量选择变化处理"""
        self.row_vars = variables

    def _on_column_variables_selected(self, variables):
        """列变量选择变化处理"""
        self.column_vars = variables

    def _get_option_label(self, option):
        """获取选项标签"""
        labels = {
            'chi_square': '卡方检验',
            'phi_and_cramer_v': 'Phi 和 Cramer's V',
            'contingency_coefficient': '列联系数',
            'lambda': 'Lambda',
            'gamma': 'Gamma',
            'kendall_tau_b': 'Kendall's tau-b',
            'kendall_tau_c': 'Kendall's tau-c',
            'spearman_rho': 'Spearman rho'
        }
        return labels.get(option, option)

    def get_parameters(self) -> dict:
        """获取分析参数"""
        # 收集选中的选项
        selected_options = [option for option, checkbox in self.option_checkboxes.items() if checkbox.isChecked()]
        
        return {
            'row_variables': self.row_vars,
            'column_variables': self.column_vars,
            'statistics': selected_options
        }

    def validate_inputs(self) -> tuple[bool, str]:
        """验证输入"""
        if not self.row_vars:
            return False, "请至少选择一个行变量"
        if not self.column_vars:
            return False, "请至少选择一个列变量"
        return True, ""
