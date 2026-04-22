from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QLabel, QComboBox
from axaltyx_gui.dialogs.base_dialog import AnalysisDialogBase
from axaltyx_i18n.manager import I18nManager

class CorrelationDialog(AnalysisDialogBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('analysis.correlation.title'))
        self.title_label.setText(self.i18n.get_text('analysis.correlation.title'))
        self._init_options()
    
    def _init_options(self):
        # 相关类型
        correlation_type_group = QGroupBox(self.i18n.get_text('analysis.correlation.type'))
        correlation_type_layout = QVBoxLayout()
        
        self.correlation_type_combo = QComboBox()
        self.correlation_type_combo.addItem(self.i18n.get_text('analysis.correlation.pearson'), 'pearson')
        self.correlation_type_combo.addItem(self.i18n.get_text('analysis.correlation.spearman'), 'spearman')
        self.correlation_type_combo.addItem(self.i18n.get_text('analysis.correlation.kendall'), 'kendall')
        correlation_type_layout.addWidget(self.correlation_type_combo)
        
        correlation_type_group.setLayout(correlation_type_layout)
        self.options_layout.addWidget(correlation_type_group)
        
        # 选项
        options_group = QGroupBox(self.i18n.get_text('analysis.correlation.options'))
        options_layout = QVBoxLayout()
        
        self.significance_check = QCheckBox(self.i18n.get_text('analysis.correlation.significance'))
        self.significance_check.setChecked(True)
        options_layout.addWidget(self.significance_check)
        
        self.correlation_matrix_check = QCheckBox(self.i18n.get_text('analysis.correlation.correlation_matrix'))
        self.correlation_matrix_check.setChecked(True)
        options_layout.addWidget(self.correlation_matrix_check)
        
        options_group.setLayout(options_layout)
        self.options_layout.addWidget(options_group)
    
    def get_options(self):
        return {
            'correlation_type': self.correlation_type_combo.currentData(),
            'significance': self.significance_check.isChecked(),
            'correlation_matrix': self.correlation_matrix_check.isChecked()
        }
