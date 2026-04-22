from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QLabel, QComboBox
from axaltyx_gui.dialogs.base_dialog import AnalysisDialogBase
from axaltyx_i18n.manager import I18nManager

class RegressionDialog(AnalysisDialogBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('analysis.regression.title'))
        self.title_label.setText(self.i18n.get_text('analysis.regression.title'))
        self._init_options()
    
    def _init_options(self):
        # 回归类型
        regression_type_group = QGroupBox(self.i18n.get_text('analysis.regression.type'))
        regression_type_layout = QVBoxLayout()
        
        self.regression_type_combo = QComboBox()
        self.regression_type_combo.addItem(self.i18n.get_text('analysis.regression.linear'), 'linear')
        self.regression_type_combo.addItem(self.i18n.get_text('analysis.regression.logistic'), 'logistic')
        self.regression_type_combo.addItem(self.i18n.get_text('analysis.regression.multiple'), 'multiple')
        regression_type_layout.addWidget(self.regression_type_combo)
        
        regression_type_group.setLayout(regression_type_layout)
        self.options_layout.addWidget(regression_type_group)
        
        # 选项
        options_group = QGroupBox(self.i18n.get_text('analysis.regression.options'))
        options_layout = QVBoxLayout()
        
        self.confidence_interval_check = QCheckBox(self.i18n.get_text('analysis.regression.confidence_interval'))
        self.confidence_interval_check.setChecked(True)
        options_layout.addWidget(self.confidence_interval_check)
        
        self.r_squared_check = QCheckBox(self.i18n.get_text('analysis.regression.r_squared'))
        self.r_squared_check.setChecked(True)
        options_layout.addWidget(self.r_squared_check)
        
        self.anova_table_check = QCheckBox(self.i18n.get_text('analysis.regression.anova_table'))
        self.anova_table_check.setChecked(True)
        options_layout.addWidget(self.anova_table_check)
        
        options_group.setLayout(options_layout)
        self.options_layout.addWidget(options_group)
    
    def get_options(self):
        return {
            'regression_type': self.regression_type_combo.currentData(),
            'confidence_interval': self.confidence_interval_check.isChecked(),
            'r_squared': self.r_squared_check.isChecked(),
            'anova_table': self.anova_table_check.isChecked()
        }
