from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QSpinBox, QLineEdit, QCheckBox
from PyQt6.QtCore import Qt
from axaltyx_i18n.manager import I18nManager

class ExportChartDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('dialog.export.title'))
        self.setMinimumSize(600, 400)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(16)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        
        # 导出格式
        format_group = QHBoxLayout()
        format_label = QLabel(self.i18n.get_text('dialog.export.format'))
        self.format_combo = QComboBox()
        self.format_combo.addItem('PNG', 'png')
        self.format_combo.addItem('JPG', 'jpg')
        self.format_combo.addItem('SVG', 'svg')
        self.format_combo.addItem('PDF', 'pdf')
        self.format_combo.addItem('EPS', 'eps')
        format_group.addWidget(format_label)
        format_group.addWidget(self.format_combo)
        self.main_layout.addLayout(format_group)
        
        # 分辨率
        dpi_group = QHBoxLayout()
        dpi_label = QLabel(self.i18n.get_text('dialog.export.dpi'))
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setMinimum(72)
        self.dpi_spin.setMaximum(600)
        self.dpi_spin.setValue(300)
        dpi_group.addWidget(dpi_label)
        dpi_group.addWidget(self.dpi_spin)
        self.main_layout.addLayout(dpi_group)
        
        # 宽度
        width_group = QHBoxLayout()
        width_label = QLabel(self.i18n.get_text('dialog.export.width'))
        self.width_edit = QLineEdit('10')
        width_unit = QLabel('英寸')
        width_group.addWidget(width_label)
        width_group.addWidget(self.width_edit)
        width_group.addWidget(width_unit)
        self.main_layout.addLayout(width_group)
        
        # 高度
        height_group = QHBoxLayout()
        height_label = QLabel(self.i18n.get_text('dialog.export.height'))
        self.height_edit = QLineEdit('8')
        height_unit = QLabel('英寸')
        height_group.addWidget(height_label)
        height_group.addWidget(self.height_edit)
        height_group.addWidget(height_unit)
        self.main_layout.addLayout(height_group)
        
        # 选项
        options_group = QVBoxLayout()
        options_label = QLabel(self.i18n.get_text('dialog.export.options'))
        self.transparent_check = QCheckBox(self.i18n.get_text('dialog.export.transparent'))
        self.transparent_check.setChecked(False)
        self.antialias_check = QCheckBox(self.i18n.get_text('dialog.export.antialias'))
        self.antialias_check.setChecked(True)
        options_group.addWidget(options_label)
        options_group.addWidget(self.transparent_check)
        options_group.addWidget(self.antialias_check)
        self.main_layout.addLayout(options_group)
        
        # 文件路径
        path_group = QHBoxLayout()
        path_label = QLabel(self.i18n.get_text('dialog.export.path'))
        self.path_edit = QLineEdit()
        self.browse_button = QPushButton(self.i18n.get_text('dialog.file.browse'))
        path_group.addWidget(path_label)
        path_group.addWidget(self.path_edit)
        path_group.addWidget(self.browse_button)
        self.main_layout.addLayout(path_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.ok_button = QPushButton(self.i18n.get_text('dialog.button.ok'))
        self.ok_button.setFixedWidth(100)
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton(self.i18n.get_text('dialog.button.cancel'))
        self.cancel_button.setFixedWidth(100)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        self.main_layout.addLayout(button_layout)
    
    def get_export_settings(self):
        return {
            'format': self.format_combo.currentData(),
            'dpi': self.dpi_spin.value(),
            'width': float(self.width_edit.text()),
            'height': float(self.height_edit.text()),
            'transparent': self.transparent_check.isChecked(),
            'antialias': self.antialias_check.isChecked(),
            'path': self.path_edit.text()
        }
