from .base_dialog import AnalysisDialogBase
from src.axaltyx_gui.custom_widgets import AxaltyXVariableSelector
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QFormLayout, QComboBox, QLabel, QRadioButton, QButtonGroup, QSpinBox
from PyQt6.QtCore import Qt


class FactorDialog(AnalysisDialogBase):
    """因子分析对话框"""

    def __init__(self, available_vars, parent=None):
        super().__init__("因子分析", parent)
        self.available_vars = available_vars
        self.selected_vars = []
        self.extraction_method = 'principal'
        self.rotation_method = 'varimax'
        self.factor_count = 3
        self.show_scree = True
        self.show_loadings = True
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
        
        # 提取方法
        layout.addRow("提取方法:")
        self.extraction_combo = QComboBox()
        self.extraction_combo.addItems(['主成分分析', '主轴因子法', '最大似然法'])
        layout.addRow(self.extraction_combo)
        
        # 旋转方法
        layout.addRow("旋转方法:")
        self.rotation_combo = QComboBox()
        self.rotation_combo.addItems(['无旋转', '最大方差法', 'Promax 斜交旋转'])
        layout.addRow(self.rotation_combo)
        
        # 因子数
        layout.addRow("因子数:")
        self.factor_spin = QSpinBox()
        self.factor_spin.setMinimum(1)
        self.factor_spin.setMaximum(20)
        self.factor_spin.setValue(3)
        layout.addRow(self.factor_spin)
        
        # 碎石图
        self.scree_checkbox = QCheckBox("显示碎石图")
        self.scree_checkbox.setChecked(True)
        layout.addRow(self.scree_checkbox)
        
        # 因子载荷
        self.loadings_checkbox = QCheckBox("显示因子载荷")
        self.loadings_checkbox.setChecked(True)
        layout.addRow(self.loadings_checkbox)
        
        #  communalities
        self.communalities_checkbox = QCheckBox("显示公因子方差")
        self.communalities_checkbox.setChecked(False)
        layout.addRow(self.communalities_checkbox)

    def _on_variables_selected(self, variables):
        """变量选择变化处理"""
        self.selected_vars = variables

    def get_parameters(self) -> dict:
        """获取分析参数"""
        # 提取方法映射
        extraction_methods = {
            '主成分分析': 'principal',
            '主轴因子法': 'principal_axis',
            '最大似然法': 'maximum_likelihood'
        }
        
        # 旋转方法映射
        rotation_methods = {
            '无旋转': 'none',
            '最大方差法': 'varimax',
            'Promax 斜交旋转': 'promax'
        }
        
        return {
            'variables': self.selected_vars,
            'extraction_method': extraction_methods.get(self.extraction_combo.currentText(), 'principal'),
            'rotation_method': rotation_methods.get(self.rotation_combo.currentText(), 'varimax'),
            'factor_count': self.factor_spin.value(),
            'show_scree': self.scree_checkbox.isChecked(),
            'show_loadings': self.loadings_checkbox.isChecked(),
            'show_communalities': self.communalities_checkbox.isChecked()
        }

    def validate_inputs(self) -> tuple[bool, str]:
        """验证输入"""
        if not self.selected_vars:
            return False, "请至少选择一个变量"
        if len(self.selected_vars) < 3:
            return False, "因子分析需要至少3个变量"
        return True, ""
