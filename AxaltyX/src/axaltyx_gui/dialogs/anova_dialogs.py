from .base_dialog import AnalysisDialogBase
from src.axaltyx_gui.custom_widgets import AxaltyXVariableSelector
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QFormLayout, QComboBox, QLabel, QRadioButton, QButtonGroup
from PyQt6.QtCore import Qt


class AnovaDialog(AnalysisDialogBase):
    """方差分析对话框"""

    def __init__(self, available_vars, parent=None):
        super().__init__("方差分析", parent)
        self.available_vars = available_vars
        self.dependent_vars = []
        self.factor_vars = []
        self.anova_type = 'one_way'
        self.post_hoc = False
        self.effect_size = False
        self.homogeneity = False
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
        self.dep_selector.sig_variables_selected.connect(self._on_dependent_variables_selected)
        dep_var_layout.addWidget(self.dep_selector)
        layout.addLayout(dep_var_layout)
        
        # 因子变量
        factor_var_layout = QVBoxLayout()
        factor_var_layout.addWidget(QLabel("因子变量:"))
        self.factor_selector = AxaltyXVariableSelector(self.available_vars)
        self.factor_selector.sig_variables_selected.connect(self._on_factor_variables_selected)
        factor_var_layout.addWidget(self.factor_selector)
        layout.addLayout(factor_var_layout)
        
        # 方差分析类型
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("分析类型:"))
        
        self.anova_type_group = QButtonGroup()
        
        self.one_way_radio = QRadioButton("单因素方差分析")
        self.one_way_radio.setChecked(True)
        self.anova_type_group.addButton(self.one_way_radio)
        
        self.two_way_radio = QRadioButton("多因素方差分析")
        self.anova_type_group.addButton(self.two_way_radio)
        
        self.rm_anova_radio = QRadioButton("重复测量方差分析")
        self.anova_type_group.addButton(self.rm_anova_radio)
        
        self.ancova_radio = QRadioButton("协方差分析")
        self.anova_type_group.addButton(self.ancova_radio)
        
        self.anova_type_group.buttonClicked.connect(self._on_anova_type_changed)
        
        type_layout.addWidget(self.one_way_radio)
        type_layout.addWidget(self.two_way_radio)
        type_layout.addWidget(self.rm_anova_radio)
        type_layout.addWidget(self.ancova_radio)
        layout.addLayout(type_layout)

    def setup_options_panel(self) -> None:
        """设置选项面板"""
        self.options_panel = QGroupBox("选项")
        layout = QFormLayout(self.options_panel)
        
        # 事后比较
        self.post_hoc_checkbox = QCheckBox("事后比较")
        self.post_hoc_checkbox.setChecked(False)
        layout.addRow(self.post_hoc_checkbox)
        
        # 效应量
        self.effect_size_checkbox = QCheckBox("效应量")
        self.effect_size_checkbox.setChecked(False)
        layout.addRow(self.effect_size_checkbox)
        
        # 方差齐性检验
        self.homogeneity_checkbox = QCheckBox("方差齐性检验")
        self.homogeneity_checkbox.setChecked(False)
        layout.addRow(self.homogeneity_checkbox)
        
        # 事后比较方法（当事后比较被选中时显示）
        self.post_hoc_method_layout = QVBoxLayout()
        self.post_hoc_method_combo = QComboBox()
        self.post_hoc_method_combo.addItems(['LSD', 'Bonferroni', 'Tukey', 'Scheffe'])
        layout.addRow("事后比较方法:", self.post_hoc_method_combo)

    def _on_dependent_variables_selected(self, variables):
        """因变量选择变化处理"""
        self.dependent_vars = variables

    def _on_factor_variables_selected(self, variables):
        """因子变量选择变化处理"""
        self.factor_vars = variables

    def _on_anova_type_changed(self, button):
        """方差分析类型变化处理"""
        if button == self.one_way_radio:
            self.anova_type = 'one_way'
        elif button == self.two_way_radio:
            self.anova_type = 'two_way'
        elif button == self.rm_anova_radio:
            self.anova_type = 'repeated_measures'
        elif button == self.ancova_radio:
            self.anova_type = 'ancova'

    def get_parameters(self) -> dict:
        """获取分析参数"""
        return {
            'anova_type': self.anova_type,
            'dependent_variables': self.dependent_vars,
            'factor_variables': self.factor_vars,
            'post_hoc': self.post_hoc_checkbox.isChecked(),
            'post_hoc_method': self.post_hoc_method_combo.currentText(),
            'effect_size': self.effect_size_checkbox.isChecked(),
            'homogeneity': self.homogeneity_checkbox.isChecked()
        }

    def validate_inputs(self) -> tuple[bool, str]:
        """验证输入"""
        if not self.dependent_vars:
            return False, "请至少选择一个因变量"
        if not self.factor_vars:
            return False, "请至少选择一个因子变量"
        return True, ""
