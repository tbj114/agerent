from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QLabel, QComboBox, QSpinBox
from axaltyx_gui.dialogs.base_dialog import AnalysisDialogBase
from axaltyx_i18n.manager import I18nManager

class ClusteringDialog(AnalysisDialogBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('analysis.clustering.title'))
        self.title_label.setText(self.i18n.get_text('analysis.clustering.title'))
        self._init_options()
    
    def _init_options(self):
        # 聚类方法
        method_group = QGroupBox(self.i18n.get_text('analysis.clustering.method'))
        method_layout = QVBoxLayout()
        
        self.method_combo = QComboBox()
        self.method_combo.addItem(self.i18n.get_text('analysis.clustering.kmeans'), 'kmeans')
        self.method_combo.addItem(self.i18n.get_text('analysis.clustering.hierarchical'), 'hierarchical')
        self.method_combo.addItem(self.i18n.get_text('analysis.clustering.dbscan'), 'dbscan')
        method_layout.addWidget(self.method_combo)
        
        method_group.setLayout(method_layout)
        self.options_layout.addWidget(method_group)
        
        # 聚类数量
        clusters_group = QGroupBox(self.i18n.get_text('analysis.clustering.clusters'))
        clusters_layout = QVBoxLayout()
        
        self.clusters_spin = QSpinBox()
        self.clusters_spin.setMinimum(2)
        self.clusters_spin.setMaximum(10)
        self.clusters_spin.setValue(3)
        clusters_layout.addWidget(self.clusters_spin)
        
        clusters_group.setLayout(clusters_layout)
        self.options_layout.addWidget(clusters_group)
        
        # 选项
        options_group = QGroupBox(self.i18n.get_text('analysis.clustering.options'))
        options_layout = QVBoxLayout()
        
        self.dendrogram_check = QCheckBox(self.i18n.get_text('analysis.clustering.dendrogram'))
        self.dendrogram_check.setChecked(False)
        options_layout.addWidget(self.dendrogram_check)
        
        self.silhouette_check = QCheckBox(self.i18n.get_text('analysis.clustering.silhouette'))
        self.silhouette_check.setChecked(False)
        options_layout.addWidget(self.silhouette_check)
        
        options_group.setLayout(options_layout)
        self.options_layout.addWidget(options_group)
    
    def get_options(self):
        return {
            'method': self.method_combo.currentData(),
            'clusters': self.clusters_spin.value(),
            'dendrogram': self.dendrogram_check.isChecked(),
            'silhouette': self.silhouette_check.isChecked()
        }
