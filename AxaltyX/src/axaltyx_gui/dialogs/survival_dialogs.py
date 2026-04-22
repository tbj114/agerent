from .base_dialog import AnalysisDialogBase
from src.axaltyx_gui.custom_widgets import AxaltyXVariableSelector
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QFormLayout, QComboBox, QLabel, QRadioButton, QButtonGroup
from PyQt6.QtCore import Qt


class SurvivalDialog(AnalysisDialogBase):
    """生存分析对话框"""

    def __init__(self, available_vars, parent=None):
        super().__init__("生存分析", parent)
        self.available_vars = available_vars
        self.time_var = []
        self.event_var = []
        self.group_var = []
        self.covariates = []
        self.survival_type = 'kaplan_meier'
        self.show_survival = True
        self.show_hazard = False
        self.show_confidence = True
        # 重新初始化UI
        self.init_ui()

    def setup_variable_selector(self) -> None:
        """设置变量选择器"""
        self.variable_selector_widget = QGroupBox("变量")
        layout = QVBoxLayout(self.variable_selector_widget)
        
        # 时间变量
        time_var_layout = QVBoxLayout()
        time_var_layout.addWidget(QLabel("时间变量:"))
        self.time_selector = AxaltyXVariableSelector(self.available_vars)
        self.time_selector.sig_variables_selected.connect(self._on_time_variable_selected)
        time_var_layout.addWidget(self.time_selector)
        layout.addLayout(time_var_layout)
        
        # 事件变量
        event_var_layout = QVBoxLayout()
        event_var_layout.addWidget(QLabel("事件变量:"))
        self.event_selector = AxaltyXVariableSelector(self.available_vars)
        self.event_selector.sig_variables_selected.connect(self._on_event_variable_selected)
        event_var_layout.addWidget(self.event_selector)
        layout.addLayout(event_var_layout)
        
        # 分组变量
        group_var_layout = QVBoxLayout()
        group_var_layout.addWidget(QLabel("分组变量:"))
        self.group_selector = AxaltyXVariableSelector(self.available_vars)
        self.group_selector.sig_variables_selected.connect(self._on_group_variable_selected)
        group_var_layout.addWidget(self.group_selector)
        layout.addLayout(group_var_layout)
        
        # 协变量（Cox回归）
        covariate_layout = QVBoxLayout()
        covariate_layout.addWidget(QLabel("协变量:"))
        self.covariate_selector = AxaltyXVariableSelector(self.available_vars)
        self.covariate_selector.sig_variables_selected.connect(self._on_covariate_selected)
        covariate_layout.addWidget(self.covariate_selector)
        layout.addLayout(covariate_layout)
        
        # 分析类型
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("分析类型:"))
        
        self.survival_type_group = QButtonGroup()
        
        self.kaplan_meier_radio = QRadioButton("Kaplan-Meier 生存分析")
        self.kaplan_meier_radio.setChecked(True)
        self.survival_type_group.addButton(self.kaplan_meier_radio)
        
        self.cox_radio = QRadioButton("Cox 回归")
        self.survival_type_group.addButton(self.cox_radio)
        
        self.survival_type_group.buttonClicked.connect(self._on_survival_type_changed)
        
        type_layout.addWidget(self.kaplan_meier_radio)
        type_layout.addWidget(self.cox_radio)
        layout.addLayout(type_layout)

    def setup_options_panel(self) -> None:
        """设置选项面板"""
        self.options_panel = QGroupBox("选项")
        layout = QFormLayout(self.options_panel)
        
        # 显示生存函数
        self.survival_checkbox = QCheckBox("显示生存函数")
        self.survival_checkbox.setChecked(True)
        layout.addRow(self.survival_checkbox)
        
        # 显示风险函数
        self.hazard_checkbox = QCheckBox("显示风险函数")
        self.hazard_checkbox.setChecked(False)
        layout.addRow(self.hazard_checkbox)
        
        # 显示置信区间
        self.confidence_checkbox = QCheckBox("显示置信区间")
        self.confidence_checkbox.setChecked(True)
        layout.addRow(self.confidence_checkbox)
        
        # 置信水平
        layout.addRow("置信水平:")
        self.confidence_combo = QComboBox()
        self.confidence_combo.addItems(['90%', '95%', '99%'])
        layout.addRow(self.confidence_combo)

    def _on_time_variable_selected(self, variables):
        """时间变量选择变化处理"""
        self.time_var = variables

    def _on_event_variable_selected(self, variables):
        """事件变量选择变化处理"""
        self.event_var = variables

    def _on_group_variable_selected(self, variables):
        """分组变量选择变化处理"""
        self.group_var = variables

    def _on_covariate_selected(self, variables):
        """协变量选择变化处理"""
        self.covariates = variables

    def _on_survival_type_changed(self, button):
        """生存分析类型变化处理"""
        if button == self.kaplan_meier_radio:
            self.survival_type = 'kaplan_meier'
        elif button == self.cox_radio:
            self.survival_type = 'cox_regression'

    def get_parameters(self) -> dict:
        """获取分析参数"""
        return {
            'survival_type': self.survival_type,
            'time_variable': self.time_var,
            'event_variable': self.event_var,
            'group_variable': self.group_var,
            'covariates': self.covariates,
            'show_survival': self.survival_checkbox.isChecked(),
            'show_hazard': self.hazard_checkbox.isChecked(),
            'show_confidence': self.confidence_checkbox.isChecked(),
            'confidence_level': float(self.confidence_combo.currentText().replace('%', ''))
        }

    def validate_inputs(self) -> tuple[bool, str]:
        """验证输入"""
        if not self.time_var:
            return False, "请选择一个时间变量"
        if not self.event_var:
            return False, "请选择一个事件变量"
        return True, ""
