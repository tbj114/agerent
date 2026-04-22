from .base_dialog import AnalysisDialogBase
from src.axaltyx_gui.custom_widgets import AxaltyXVariableSelector
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QFormLayout, QComboBox, QLabel, QRadioButton, QButtonGroup, QSpinBox
from PyQt6.QtCore import Qt


class ClusteringDialog(AnalysisDialogBase):
    """聚类分析对话框"""

    def __init__(self, available_vars, parent=None):
        super().__init__("聚类分析", parent)
        self.available_vars = available_vars
        self.selected_vars = []
        self.clustering_type = 'hierarchical'
        self.cluster_count = 3
        self.distance_method = 'euclidean'
        self.linkage_method = 'ward'
        self.standardize = True
        # 重新初始化UI
        self.init_ui()

    def setup_variable_selector(self) -> None:
        """设置变量选择器"""
        self.variable_selector_widget = QGroupBox("变量")
        layout = QVBoxLayout(self.variable_selector_widget)
        
        self.variable_selector = AxaltyXVariableSelector(self.available_vars)
        self.variable_selector.sig_variables_selected.connect(self._on_variables_selected)
        layout.addWidget(self.variable_selector)

    def setup_options_panel(self) -> None:
        """设置选项面板"""
        self.options_panel = QGroupBox("选项")
        layout = QFormLayout(self.options_panel)
        
        # 聚类类型
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("聚类类型:"))
        
        self.clustering_type_group = QButtonGroup()
        
        self.hierarchical_radio = QRadioButton("层次聚类")
        self.hierarchical_radio.setChecked(True)
        self.clustering_type_group.addButton(self.hierarchical_radio)
        
        self.kmeans_radio = QRadioButton("K-Means 聚类")
        self.clustering_type_group.addButton(self.kmeans_radio)
        
        self.clustering_type_group.buttonClicked.connect(self._on_clustering_type_changed)
        
        type_layout.addWidget(self.hierarchical_radio)
        type_layout.addWidget(self.kmeans_radio)
        layout.addRow(type_layout)
        
        # 聚类数
        layout.addRow("聚类数:")
        self.cluster_spin = QSpinBox()
        self.cluster_spin.setMinimum(2)
        self.cluster_spin.setMaximum(20)
        self.cluster_spin.setValue(3)
        layout.addRow(self.cluster_spin)
        
        # 距离方法
        layout.addRow("距离方法:")
        self.distance_combo = QComboBox()
        self.distance_combo.addItems(['欧氏距离', '曼哈顿距离', '切比雪夫距离', '余弦相似度'])
        layout.addRow(self.distance_combo)
        
        # 链接方法（层次聚类）
        self.linkage_layout = QVBoxLayout()
        layout.addRow("链接方法:")
        self.linkage_combo = QComboBox()
        self.linkage_combo.addItems(['Ward 法', '平均连接法', '完全连接法', '单连接法'])
        layout.addRow(self.linkage_combo)
        
        # 标准化
        self.standardize_checkbox = QCheckBox("标准化变量")
        self.standardize_checkbox.setChecked(True)
        layout.addRow(self.standardize_checkbox)
        
        # 绘制树状图
        self.dendrogram_checkbox = QCheckBox("绘制树状图")
        self.dendrogram_checkbox.setChecked(True)
        layout.addRow(self.dendrogram_checkbox)

    def _on_variables_selected(self, variables):
        """变量选择变化处理"""
        self.selected_vars = variables

    def _on_clustering_type_changed(self, button):
        """聚类类型变化处理"""
        if button == self.hierarchical_radio:
            self.clustering_type = 'hierarchical'
            self.linkage_combo.setEnabled(True)
            self.dendrogram_checkbox.setEnabled(True)
        elif button == self.kmeans_radio:
            self.clustering_type = 'kmeans'
            self.linkage_combo.setEnabled(False)
            self.dendrogram_checkbox.setEnabled(False)

    def get_parameters(self) -> dict:
        """获取分析参数"""
        # 距离方法映射
        distance_methods = {
            '欧氏距离': 'euclidean',
            '曼哈顿距离': 'manhattan',
            '切比雪夫距离': 'chebyshev',
            '余弦相似度': 'cosine'
        }
        
        # 链接方法映射
        linkage_methods = {
            'Ward 法': 'ward',
            '平均连接法': 'average',
            '完全连接法': 'complete',
            '单连接法': 'single'
        }
        
        return {
            'clustering_type': self.clustering_type,
            'variables': self.selected_vars,
            'cluster_count': self.cluster_spin.value(),
            'distance_method': distance_methods.get(self.distance_combo.currentText(), 'euclidean'),
            'linkage_method': linkage_methods.get(self.linkage_combo.currentText(), 'ward'),
            'standardize': self.standardize_checkbox.isChecked(),
            'show_dendrogram': self.dendrogram_checkbox.isChecked()
        }

    def validate_inputs(self) -> tuple[bool, str]:
        """验证输入"""
        if not self.selected_vars:
            return False, "请至少选择一个变量"
        if len(self.selected_vars) < 2:
            return False, "聚类分析需要至少2个变量"
        return True, ""
