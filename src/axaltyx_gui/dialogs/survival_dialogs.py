from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QLabel, QComboBox
from axaltyx_gui.dialogs.base_dialog import AnalysisDialogBase
from axaltyx_i18n.manager import I18nManager

class SurvivalDialog(AnalysisDialogBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('analysis.survival.title'))
        self.title_label.setText(self.i18n.get_text('analysis.survival.title'))
        self._init_options()
    
    def _init_options(self):
        # 分析类型
        analysis_type_group = QGroupBox(self.i18n.get_text('analysis.survival.type'))
        analysis_type_layout = QVBoxLayout()
        
        self.analysis_type_combo = QComboBox()
        self.analysis_type_combo.addItem(self.i18n.get_text('analysis.survival.km'), 'km')
        self.analysis_type_combo.addItem(self.i18n.get_text('analysis.survival.cox'), 'cox')
        analysis_type_layout.addWidget(self.analysis_type_combo)
        
        analysis_type_group.setLayout(analysis_type_layout)
        self.options_layout.addWidget(analysis_type_group)
        
        # 选项
        options_group = QGroupBox(self.i18n.get_text('analysis.survival.options'))
        options_layout = QVBoxLayout()
        
        self.log_rank_check = QCheckBox(self.i18n.get_text('analysis.survival.log_rank'))
        self.log_rank_check.setChecked(True)
        options_layout.addWidget(self.log_rank_check)
        
        self.survival_curve_check = QCheckBox(self.i18n.get_text('analysis.survival.survival_curve'))
        self.survival_curve_check.setChecked(True)
        options_layout.addWidget(self.survival_curve_check)
        
        options_group.setLayout(options_layout)
        self.options_layout.addWidget(options_group)
    
    def get_options(self):
        return {
            'analysis_type': self.analysis_type_combo.currentData(),
            'log_rank': self.log_rank_check.isChecked(),
            'survival_curve': self.survival_curve_check.isChecked()
        }
