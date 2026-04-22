from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QLabel, QComboBox, QSpinBox, QDoubleSpinBox
from axaltyx_gui.dialogs.base_dialog import AnalysisDialogBase
from axaltyx_i18n.manager import I18nManager

class FactorDialog(AnalysisDialogBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('analysis.factor.title'))
        self.title_label.setText(self.i18n.get_text('analysis.factor.title'))
        self._init_options()
    
    def _init_options(self):
        # 提取方法
        extraction_group = QGroupBox(self.i18n.get_text('analysis.factor.extraction'))
        extraction_layout = QVBoxLayout()
        
        self.extraction_method_combo = QComboBox()
        self.extraction_method_combo.addItem(self.i18n.get_text('analysis.factor.principal_components'), 'principal_components')
        self.extraction_method_combo.addItem(self.i18n.get_text('analysis.factor.varimax'), 'varimax')
        extraction_layout.addWidget(self.extraction_method_combo)
        
        extraction_group.setLayout(extraction_layout)
        self.options_layout.addWidget(extraction_group)
        
        # 因子数量
        factors_group = QGroupBox(self.i18n.get_text('analysis.factor.factors'))
        factors_layout = QVBoxLayout()
        
        self.factors_spin = QSpinBox()
        self.factors_spin.setMinimum(1)
        self.factors_spin.setMaximum(10)
        self.factors_spin.setValue(2)
        factors_layout.addWidget(self.factors_spin)
        
        factors_group.setLayout(factors_layout)
        self.options_layout.addWidget(factors_group)
        
        # 选项
        options_group = QGroupBox(self.i18n.get_text('analysis.factor.options'))
        options_layout = QVBoxLayout()
        
        self.rotation_check = QCheckBox(self.i18n.get_text('analysis.factor.rotation'))
        self.rotation_check.setChecked(True)
        options_layout.addWidget(self.rotation_check)
        
        self.scree_plot_check = QCheckBox(self.i18n.get_text('analysis.factor.scree_plot'))
        self.scree_plot_check.setChecked(False)
        options_layout.addWidget(self.scree_plot_check)
        
        options_group.setLayout(options_layout)
        self.options_layout.addWidget(options_group)
    
    def get_options(self):
        return {
            'extraction_method': self.extraction_method_combo.currentData(),
            'factors': self.factors_spin.value(),
            'rotation': self.rotation_check.isChecked(),
            'scree_plot': self.scree_plot_check.isChecked()
        }
