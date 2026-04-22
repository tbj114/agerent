from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QLabel, QComboBox
from axaltyx_gui.dialogs.base_dialog import AnalysisDialogBase
from axaltyx_i18n.manager import I18nManager

class AnovaDialog(AnalysisDialogBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('analysis.anova.title'))
        self.title_label.setText(self.i18n.get_text('analysis.anova.title'))
        self._init_options()
    
    def _init_options(self):
        # 检验类型
        test_type_group = QGroupBox(self.i18n.get_text('analysis.anova.type'))
        test_type_layout = QVBoxLayout()
        
        self.test_type_combo = QComboBox()
        self.test_type_combo.addItem(self.i18n.get_text('analysis.anova.one_way'), 'one_way')
        self.test_type_combo.addItem(self.i18n.get_text('analysis.anova.two_way'), 'two_way')
        self.test_type_combo.addItem(self.i18n.get_text('analysis.anova.repeated_measures'), 'repeated_measures')
        test_type_layout.addWidget(self.test_type_combo)
        
        test_type_group.setLayout(test_type_layout)
        self.options_layout.addWidget(test_type_group)
        
        # 选项
        options_group = QGroupBox(self.i18n.get_text('analysis.anova.options'))
        options_layout = QVBoxLayout()
        
        self.post_hoc_check = QCheckBox(self.i18n.get_text('analysis.anova.post_hoc'))
        self.post_hoc_check.setChecked(False)
        options_layout.addWidget(self.post_hoc_check)
        
        self.effect_size_check = QCheckBox(self.i18n.get_text('analysis.anova.effect_size'))
        self.effect_size_check.setChecked(False)
        options_layout.addWidget(self.effect_size_check)
        
        options_group.setLayout(options_layout)
        self.options_layout.addWidget(options_group)
    
    def get_options(self):
        return {
            'test_type': self.test_type_combo.currentData(),
            'post_hoc': self.post_hoc_check.isChecked(),
            'effect_size': self.effect_size_check.isChecked()
        }
