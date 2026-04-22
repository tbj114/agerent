from .base_dialog import AnalysisDialogBase
from src.axaltyx_gui.custom_widgets import AxaltyXVariableSelector
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QFormLayout
from PyQt6.QtCore import Qt


class DescriptiveDialog(AnalysisDialogBase):
    """描述性统计对话框"""

    def __init__(self, available_vars, parent=None):
        super().__init__("描述性统计", parent)
        self.available_vars = available_vars
        self.selected_vars = []
        self.statistics = {
            'mean': True,
            'std': True,
            'min': True,
            'max': True,
            'skewness': False,
            'kurtosis': False,
            'median': False,
            'sum': False,
            'count': False,
            'sem': False,
            'cv': False
        }
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
        self.options_panel = QGroupBox("统计量")
        layout = QFormLayout(self.options_panel)
        
        # 统计量复选框
        self.stat_checkboxes = {}
        for stat, default in self.statistics.items():
            checkbox = QCheckBox(self._get_stat_label(stat))
            checkbox.setChecked(default)
            self.stat_checkboxes[stat] = checkbox
            layout.addRow(checkbox)

    def _on_variables_selected(self, variables):
        """变量选择变化处理"""
        self.selected_vars = variables

    def _get_stat_label(self, stat):
        """获取统计量标签"""
        labels = {
            'mean': '均值',
            'std': '标准差',
            'min': '最小值',
            'max': '最大值',
            'skewness': '偏度',
            'kurtosis': '峰度',
            'median': '中位数',
            'sum': '求和',
            'count': '计数',
            'sem': '标准误',
            'cv': '变异系数'
        }
        return labels.get(stat, stat)

    def get_parameters(self) -> dict:
        """获取分析参数"""
        # 收集选中的统计量
        selected_stats = [stat for stat, checkbox in self.stat_checkboxes.items() if checkbox.isChecked()]
        
        return {
            'variables': self.selected_vars,
            'statistics': selected_stats
        }

    def validate_inputs(self) -> tuple[bool, str]:
        """验证输入"""
        if not self.selected_vars:
            return False, "请至少选择一个变量"
        if not any(checkbox.isChecked() for checkbox in self.stat_checkboxes.values()):
            return False, "请至少选择一个统计量"
        return True, ""
