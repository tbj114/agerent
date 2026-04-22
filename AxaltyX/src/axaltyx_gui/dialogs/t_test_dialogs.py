from .base_dialog import AnalysisDialogBase
from src.axaltyx_gui.custom_widgets import AxaltyXVariableSelector
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QFormLayout, QComboBox, QLineEdit, QRadioButton, QButtonGroup, QLabel
from PyQt6.QtCore import Qt


class TTestDialog(AnalysisDialogBase):
    """t 检验对话框"""

    def __init__(self, available_vars, parent=None):
        super().__init__("t 检验", parent)
        self.available_vars = available_vars
        self.selected_vars = []
        self.test_type = 'one_sample'
        self.test_value = 0.0
        self.group_variable = ''
        self.group_1 = 1
        self.group_2 = 2
        self.equal_variance = True
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
        
        # 测试类型选择
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("测试类型:"))
        
        self.test_type_group = QButtonGroup()
        
        self.one_sample_radio = QRadioButton("单样本 t 检验")
        self.one_sample_radio.setChecked(True)
        self.test_type_group.addButton(self.one_sample_radio)
        
        self.independent_radio = QRadioButton("独立样本 t 检验")
        self.test_type_group.addButton(self.independent_radio)
        
        self.paired_radio = QRadioButton("配对样本 t 检验")
        self.test_type_group.addButton(self.paired_radio)
        
        self.test_type_group.buttonClicked.connect(self._on_test_type_changed)
        
        type_layout.addWidget(self.one_sample_radio)
        type_layout.addWidget(self.independent_radio)
        type_layout.addWidget(self.paired_radio)
        layout.addLayout(type_layout)
        
        # 分组变量（独立样本）
        self.group_var_layout = QVBoxLayout()
        self.group_var_layout.addWidget(QLabel("分组变量:"))
        self.group_selector = AxaltyXVariableSelector(self.available_vars)
        self.group_selector.sig_variables_selected.connect(self._on_group_variable_selected)
        self.group_var_layout.addWidget(self.group_selector)
        self.group_var_layout.setVisible(False)
        layout.addLayout(self.group_var_layout)
        
        # 配对变量（配对样本）
        self.paired_var_layout = QVBoxLayout()
        self.paired_var_layout.addWidget(QLabel("配对变量:"))
        self.paired_selector = AxaltyXVariableSelector(self.available_vars)
        self.paired_selector.sig_variables_selected.connect(self._on_paired_variables_selected)
        self.paired_var_layout.addWidget(self.paired_selector)
        self.paired_var_layout.setVisible(False)
        layout.addLayout(self.paired_var_layout)

    def setup_options_panel(self) -> None:
        """设置选项面板"""
        self.options_panel = QGroupBox("选项")
        layout = QFormLayout(self.options_panel)
        
        # 检验值（单样本）
        self.test_value_layout = QVBoxLayout()
        self.test_value_edit = QLineEdit("0.0")
        layout.addRow("检验值:", self.test_value_edit)
        
        # 定义组（独立样本）
        self.group_def_layout = QVBoxLayout()
        layout.addRow("组 1 值:", QLineEdit("1"))
        layout.addRow("组 2 值:", QLineEdit("2"))
        
        # 假设方差齐性（独立样本）
        self.equal_variance_checkbox = QCheckBox("假设方差齐性")
        self.equal_variance_checkbox.setChecked(True)
        layout.addRow(self.equal_variance_checkbox)
        
        # 置信区间
        layout.addRow("置信区间:", QLineEdit("95"))

    def _on_test_variables_selected(self, variables):
        """检验变量选择变化处理"""
        self.selected_vars = variables

    def _on_group_variable_selected(self, variables):
        """分组变量选择变化处理"""
        if variables:
            self.group_variable = variables[0]

    def _on_paired_variables_selected(self, variables):
        """配对变量选择变化处理"""
        # 配对变量处理
        pass

    def _on_test_type_changed(self, button):
        """测试类型变化处理"""
        if button == self.one_sample_radio:
            self.test_type = 'one_sample'
            self.group_var_layout.setVisible(False)
            self.paired_var_layout.setVisible(False)
        elif button == self.independent_radio:
            self.test_type = 'independent'
            self.group_var_layout.setVisible(True)
            self.paired_var_layout.setVisible(False)
        elif button == self.paired_radio:
            self.test_type = 'paired'
            self.group_var_layout.setVisible(False)
            self.paired_var_layout.setVisible(True)

    def get_parameters(self) -> dict:
        """获取分析参数"""
        return {
            'test_type': self.test_type,
            'variables': self.selected_vars,
            'test_value': float(self.test_value_edit.text()),
            'group_variable': self.group_variable,
            'equal_variance': self.equal_variance_checkbox.isChecked()
        }

    def validate_inputs(self) -> tuple[bool, str]:
        """验证输入"""
        if not self.selected_vars:
            return False, "请至少选择一个检验变量"
        
        if self.test_type == 'independent' and not self.group_variable:
            return False, "请选择一个分组变量"
        
        try:
            float(self.test_value_edit.text())
        except ValueError:
            return False, "检验值必须是数字"
        
        return True, ""
