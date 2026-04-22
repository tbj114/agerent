from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QLabel, QComboBox
from axaltyx_gui.dialogs.base_dialog import AnalysisDialogBase
from axaltyx_i18n.manager import I18nManager

class ReliabilityDialog(AnalysisDialogBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('analysis.reliability.title'))
        self.title_label.setText(self.i18n.get_text('analysis.reliability.title'))
        self._init_options()
    
    def _init_options(self):
        # 信度类型
        reliability_type_group = QGroupBox(self.i18n.get_text('analysis.reliability.type'))
        reliability_type_layout = QVBoxLayout()
        
        self.reliability_type_combo = QComboBox()
        self.reliability_type_combo.addItem(self.i18n.get_text('analysis.reliability.cronbach_alpha'), 'cronbach_alpha')
        self.reliability_type_combo.addItem(self.i18n.get_text('analysis.reliability.split_half'), 'split_half')
        reliability_type_layout.addWidget(self.reliability_type_combo)
        
        reliability_type_group.setLayout(reliability_type_layout)
        self.options_layout.addWidget(reliability_type_group)
        
        # 选项
        options_group = QGroupBox(self.i18n.get_text('analysis.reliability.options'))
        options_layout = QVBoxLayout()
        
        self.item_analysis_check = QCheckBox(self.i18n.get_text('analysis.reliability.item_analysis'))
        self.item_analysis_check.setChecked(True)
        options_layout.addWidget(self.item_analysis_check)
        
        options_group.setLayout(options_layout)
        self.options_layout.addWidget(options_group)
    
    def get_options(self):
        return {
            'reliability_type': self.reliability_type_combo.currentData(),
            'item_analysis': self.item_analysis_check.isChecked()
        }
