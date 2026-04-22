from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QLabel, QHBoxLayout
from axaltyx_gui.dialogs.base_dialog import AnalysisDialogBase
from axaltyx_i18n.manager import I18nManager

class CrosstabsDialog(AnalysisDialogBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('analysis.crosstabs.title'))
        self.title_label.setText(self.i18n.get_text('analysis.crosstabs.title'))
        self._init_options()
    
    def _init_options(self):
        # 统计量选项
        stats_group = QGroupBox(self.i18n.get_text('analysis.crosstabs.stats'))
        stats_layout = QVBoxLayout()
        
        self.chi_square_check = QCheckBox(self.i18n.get_text('analysis.crosstabs.chi_square'))
        self.chi_square_check.setChecked(True)
        stats_layout.addWidget(self.chi_square_check)
        
        self.phi_check = QCheckBox(self.i18n.get_text('analysis.crosstabs.phi'))
        self.phi_check.setChecked(False)
        stats_layout.addWidget(self.phi_check)
        
        self.cramer_v_check = QCheckBox(self.i18n.get_text('analysis.crosstabs.cramer_v'))
        self.cramer_v_check.setChecked(False)
        stats_layout.addWidget(self.cramer_v_check)
        
        stats_group.setLayout(stats_layout)
        self.options_layout.addWidget(stats_group)
        
        # 单元格选项
        cell_group = QGroupBox(self.i18n.get_text('analysis.crosstabs.cell'))
        cell_layout = QVBoxLayout()
        
        self.count_check = QCheckBox(self.i18n.get_text('analysis.crosstabs.count'))
        self.count_check.setChecked(True)
        cell_layout.addWidget(self.count_check)
        
        self.percent_row_check = QCheckBox(self.i18n.get_text('analysis.crosstabs.percent_row'))
        self.percent_row_check.setChecked(False)
        cell_layout.addWidget(self.percent_row_check)
        
        self.percent_column_check = QCheckBox(self.i18n.get_text('analysis.crosstabs.percent_column'))
        self.percent_column_check.setChecked(False)
        cell_layout.addWidget(self.percent_column_check)
        
        self.percent_total_check = QCheckBox(self.i18n.get_text('analysis.crosstabs.percent_total'))
        self.percent_total_check.setChecked(False)
        cell_layout.addWidget(self.percent_total_check)
        
        cell_group.setLayout(cell_layout)
        self.options_layout.addWidget(cell_group)
    
    def get_options(self):
        return {
            'chi_square': self.chi_square_check.isChecked(),
            'phi': self.phi_check.isChecked(),
            'cramer_v': self.cramer_v_check.isChecked(),
            'count': self.count_check.isChecked(),
            'percent_row': self.percent_row_check.isChecked(),
            'percent_column': self.percent_column_check.isChecked(),
            'percent_total': self.percent_total_check.isChecked()
        }
