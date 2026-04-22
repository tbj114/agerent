from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QLabel
from axaltyx_gui.dialogs.base_dialog import AnalysisDialogBase
from axaltyx_i18n.manager import I18nManager

class DescriptiveDialog(AnalysisDialogBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('analysis.descriptive.title'))
        self.title_label.setText(self.i18n.get_text('analysis.descriptive.title'))
        self._init_options()
    
    def _init_options(self):
        # 统计量选项
        stats_group = QGroupBox(self.i18n.get_text('analysis.descriptive.stats'))
        stats_layout = QVBoxLayout()
        
        self.mean_check = QCheckBox(self.i18n.get_text('analysis.descriptive.mean'))
        self.mean_check.setChecked(True)
        stats_layout.addWidget(self.mean_check)
        
        self.std_check = QCheckBox(self.i18n.get_text('analysis.descriptive.std'))
        self.std_check.setChecked(True)
        stats_layout.addWidget(self.std_check)
        
        self.min_check = QCheckBox(self.i18n.get_text('analysis.descriptive.min'))
        self.min_check.setChecked(True)
        stats_layout.addWidget(self.min_check)
        
        self.max_check = QCheckBox(self.i18n.get_text('analysis.descriptive.max'))
        self.max_check.setChecked(True)
        stats_layout.addWidget(self.max_check)
        
        self.median_check = QCheckBox(self.i18n.get_text('analysis.descriptive.median'))
        self.median_check.setChecked(True)
        stats_layout.addWidget(self.median_check)
        
        self.sum_check = QCheckBox(self.i18n.get_text('analysis.descriptive.sum'))
        self.sum_check.setChecked(True)
        stats_layout.addWidget(self.sum_check)
        
        self.count_check = QCheckBox(self.i18n.get_text('analysis.descriptive.count'))
        self.count_check.setChecked(True)
        stats_layout.addWidget(self.count_check)
        
        stats_group.setLayout(stats_layout)
        self.options_layout.addWidget(stats_group)
    
    def get_options(self):
        return {
            'mean': self.mean_check.isChecked(),
            'std': self.std_check.isChecked(),
            'min': self.min_check.isChecked(),
            'max': self.max_check.isChecked(),
            'median': self.median_check.isChecked(),
            'sum': self.sum_check.isChecked(),
            'count': self.count_check.isChecked()
        }
