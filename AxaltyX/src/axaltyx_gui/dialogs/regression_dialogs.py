from .base_dialog import AnalysisDialogBase
from src.axaltyx_gui.custom_widgets import AxaltyXVariableSelector
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QFormLayout, QComboBox, QLabel, QRadioButton, QButtonGroup, QLineEdit
from PyQt6.QtCore import Qt


class RegressionDialog(AnalysisDialogBase):
    """回归分析对话框"""

    def __init__(self, available_vars, parent=None):
        super().__init__("回归分析", parent)
        self.available_vars = available_vars
        self.dependent_var = []
        self.independent_vars = []
        self.regression_type = 'linear'
        self.method = 'enter'
        self.confidence_level = 95
        self.collinearity = False
        # 重新初始化UI
        self.init_ui()

    def setup_variable_selector(self) -> None:
        """设置变量选择器"""
        self.variable_selector_widget = QGroupBox("变量")
        layout = QVBoxLayout(self.variable_selector_widget)
        
        # 因变量
        dep_var_layout = QVBoxLayout()
        dep_var_layout.addWidget(QLabel("因变量:"))
        self.dep_selector = AxaltyXVariableSelector(self.available_vars)
        self.dep_selector.sig_variables_selected.connect(self._on_dependent_variable_selected)
        dep_var_layout.addWidget(self.dep_selector)
        layout.addLayout(dep_var_layout)
        
        # 自变量
        indep_var_layout = QVBoxLayout()
        indep_var_layout.addWidget(QLabel("自变量:"))
        self.indep_selector = AxaltyXVariableSelector(self.available_vars)
        self.indep_selector.sig_variables_selected.connect(self._on_independent_variables_selected)
        indep_var_layout.addWidget(self.indep_selector)
        layout.addLayout(indep_var_layout)
        
        # 回归类型
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("回归类型:"))
        
        self.regression_type_group = QButtonGroup()
        
        self.linear_radio = QRadioButton("线性回归")
        self.linear_radio.setChecked(True)
        self.regression_type_group.addButton(self.linear_radio)
        
        self.logistic_radio = QRadioButton("Logistic 回归")
        self.regression_type_group.addButton(self.logistic_radio)
        
        self.ordinal_radio = QRadioButton("有序回归")
        self.regression_type_group.addButton(self.ordinal_radio)
        
        self.regression_type_group.buttonClicked.connect(self._on_regression_type_changed)
        
        type_layout.addWidget(self.linear_radio)
        type_layout.addWidget(self.logistic_radio)
        type_layout.addWidget(self.ordinal_radio)
        layout.addLayout(type_layout)

    def setup_options_panel(self) -> None:
        """设置选项面板"""
        self.options_panel = QGroupBox("选项")
        layout = QFormLayout(self.options_panel)
        
        # 方法
        layout.addRow("方法:")
        self.method_combo = QComboBox()
        self.method_combo.addItems(['进入法', '逐步法', '向前法', '向后法'])
        layout.addRow(self.method_combo)
        
        # 置信水平
        layout.addRow("置信水平:", QLineEdit("95"))
        
        # 共线性诊断
        self.collinearity_checkbox = QCheckBox("共线性诊断")
        self.collinearity_checkbox.setChecked(False)
        layout.addRow(self.collinearity_checkbox)
        
        # 残差分析
        self.residuals_checkbox = QCheckBox("残差分析")
        self.residuals_checkbox.setChecked(False)
        layout.addRow(self.residuals_checkbox)
        
        # 模型拟合图
        self.plot_checkbox = QCheckBox("模型拟合图")
        self.plot_checkbox.setChecked(False)
        layout.addRow(self.plot_checkbox)

    def _on_dependent_variable_selected(self, variables):
        """因变量选择变化处理"""
        self.dependent_var = variables

    def _on_independent_variables_selected(self, variables):
        """自变量选择变化处理"""
        self.independent_vars = variables

    def _on_regression_type_changed(self, button):
        """回归类型变化处理"""
        if button == self.linear_radio:
            self.regression_type = 'linear'
        elif button == self.logistic_radio:
            self.regression_type = 'logistic'
        elif button == self.ordinal_radio:
            self.regression_type = 'ordinal'

    def get_parameters(self) -> dict:
        """获取分析参数"""
        # 方法映射
        methods = {
            '进入法': 'enter',
            '逐步法': 'stepwise',
            '向前法': 'forward',
            '向后法': 'backward'
        }
        
        return {
            'regression_type': self.regression_type,
            'dependent_variable': self.dependent_var,
            'independent_variables': self.independent_vars,
            'method': methods.get(self.method_combo.currentText(), 'enter'),
            'collinearity': self.collinearity_checkbox.isChecked(),
            'residuals': self.residuals_checkbox.isChecked(),
            'plot': self.plot_checkbox.isChecked()
        }

    def validate_inputs(self) -> tuple[bool, str]:
        """验证输入"""
        if not self.dependent_var:
            return False, "请选择一个因变量"
        if not self.independent_vars:
            return False, "请至少选择一个自变量"
        return True, ""
