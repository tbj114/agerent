from .base_dialog import AnalysisDialogBase
from src.axaltyx_gui.custom_widgets import AxaltyXVariableSelector
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QFormLayout, QComboBox
from PyQt6.QtCore import Qt


class FrequencyDialog(AnalysisDialogBase):
    """频数分析对话框"""

    def __init__(self, available_vars, parent=None):
        super().__init__("频数分析", parent)
        self.available_vars = available_vars
        self.selected_vars = []
        self.options = {
            'frequency': True,
            'percentage': True,
            'cumulative_frequency': False,
            'cumulative_percentage': False,
            'chart': False
        }
        self.chart_type = 'bar'
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
        
        # 统计量复选框
        self.option_checkboxes = {}
        for option, default in self.options.items():
            checkbox = QCheckBox(self._get_option_label(option))
            checkbox.setChecked(default)
            self.option_checkboxes[option] = checkbox
            layout.addRow(checkbox)
        
        # 图表类型
        layout.addRow("图表类型:")
        self.chart_combo = QComboBox()
        self.chart_combo.addItems(['柱状图', '饼图', '直方图'])
        self.chart_combo.setCurrentIndex(0)
        layout.addRow(self.chart_combo)

    def _on_variables_selected(self, variables):
        """变量选择变化处理"""
        self.selected_vars = variables

    def _get_option_label(self, option):
        """获取选项标签"""
        labels = {
            'frequency': '频数',
            'percentage': '百分比',
            'cumulative_frequency': '累计频数',
            'cumulative_percentage': '累计百分比',
            'chart': '生成图表'
        }
        return labels.get(option, option)

    def get_parameters(self) -> dict:
        """获取分析参数"""
        # 收集选中的选项
        selected_options = [option for option, checkbox in self.option_checkboxes.items() if checkbox.isChecked()]
        
        # 图表类型映射
        chart_types = {
            '柱状图': 'bar',
            '饼图': 'pie',
            '直方图': 'histogram'
        }
        
        return {
            'variables': self.selected_vars,
            'options': selected_options,
            'chart_type': chart_types.get(self.chart_combo.currentText(), 'bar')
        }

    def validate_inputs(self) -> tuple[bool, str]:
        """验证输入"""
        if not self.selected_vars:
            return False, "请至少选择一个变量"
        return True, ""
