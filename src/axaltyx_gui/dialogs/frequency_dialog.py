from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QLabel
from axaltyx_gui.dialogs.base_dialog import AnalysisDialogBase
from axaltyx_i18n.manager import I18nManager

class FrequencyDialog(AnalysisDialogBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('analysis.frequency.title'))
        self.title_label.setText(self.i18n.get_text('analysis.frequency.title'))
        self._init_options()
    
    def _init_options(self):
        # 统计量选项
        stats_group = QGroupBox(self.i18n.get_text('analysis.frequency.stats'))
        stats_layout = QVBoxLayout()
        
        self.count_check = QCheckBox(self.i18n.get_text('analysis.frequency.count'))
        self.count_check.setChecked(True)
        stats_layout.addWidget(self.count_check)
        
        self.percent_check = QCheckBox(self.i18n.get_text('analysis.frequency.percent'))
        self.percent_check.setChecked(True)
        stats_layout.addWidget(self.percent_check)
        
        self.valid_percent_check = QCheckBox(self.i18n.get_text('analysis.frequency.valid_percent'))
        self.valid_percent_check.setChecked(True)
        stats_layout.addWidget(self.valid_percent_check)
        
        self.cumulative_percent_check = QCheckBox(self.i18n.get_text('analysis.frequency.cumulative_percent'))
        self.cumulative_percent_check.setChecked(True)
        stats_layout.addWidget(self.cumulative_percent_check)
        
        stats_group.setLayout(stats_layout)
        self.options_layout.addWidget(stats_group)
        
        # 图表选项
        chart_group = QGroupBox(self.i18n.get_text('analysis.frequency.chart'))
        chart_layout = QVBoxLayout()
        
        self.bar_chart_check = QCheckBox(self.i18n.get_text('analysis.frequency.bar_chart'))
        self.bar_chart_check.setChecked(False)
        chart_layout.addWidget(self.bar_chart_check)
        
        self.pie_chart_check = QCheckBox(self.i18n.get_text('analysis.frequency.pie_chart'))
        self.pie_chart_check.setChecked(False)
        chart_layout.addWidget(self.pie_chart_check)
        
        chart_group.setLayout(chart_layout)
        self.options_layout.addWidget(chart_group)
    
    def get_options(self):
        return {
            'count': self.count_check.isChecked(),
            'percent': self.percent_check.isChecked(),
            'valid_percent': self.valid_percent_check.isChecked(),
            'cumulative_percent': self.cumulative_percent_check.isChecked(),
            'bar_chart': self.bar_chart_check.isChecked(),
            'pie_chart': self.pie_chart_check.isChecked()
        }
