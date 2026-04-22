from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, 
    QSpinBox, QPushButton, QGroupBox, QScrollArea, QLabel
)
from PyQt6.QtCore import pyqtSignal, Qt
from src.axaltyx_i18n.manager import I18nManager


class PropertyPanel(QWidget):
    """右侧属性面板"""

    sig_variable_changed = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.current_var_name = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        # 变量属性组
        var_group = QGroupBox(self.i18n.get_text('dialog.file_dialog.encoding'))  # 暂时用已有的i18n键
        var_layout = QFormLayout()
        var_layout.setSpacing(8)
        var_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        var_group.setLayout(var_layout)

        # 变量名称
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText(self.i18n.get_text('common.name'))
        var_layout.addRow(self.i18n.get_text('common.name') + ":", self.name_edit)

        # 变量类型
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Numeric", "String", "Date", "Time", "Datetime"])
        var_layout.addRow(self.i18n.get_text('common.type') + ":", self.type_combo)

        # 宽度
        self.width_spin = QSpinBox()
        self.width_spin.setMinimum(1)
        self.width_spin.setMaximum(1000)
        self.width_spin.setValue(8)
        var_layout.addRow("Width:", self.width_spin)

        # 小数位
        self.decimal_spin = QSpinBox()
        self.decimal_spin.setMinimum(0)
        self.decimal_spin.setMaximum(10)
        self.decimal_spin.setValue(2)
        var_layout.addRow("Decimals:", self.decimal_spin)

        # 标签
        self.label_edit = QLineEdit()
        var_layout.addRow("Label:", self.label_edit)

        # 值标签
        self.value_labels_edit = QLineEdit()
        var_layout.addRow("Value Labels:", self.value_labels_edit)

        # 缺失值
        self.missing_combo = QComboBox()
        self.missing_combo.addItems(["None", "Discrete Missing", "Range Missing"])
        var_layout.addRow("Missing:", self.missing_combo)

        # 列对齐
        self.align_combo = QComboBox()
        self.align_combo.addItems(["Left", "Center", "Right"])
        self.align_combo.setCurrentIndex(2)
        var_layout.addRow("Align:", self.align_combo)

        # 度量
        self.measure_combo = QComboBox()
        self.measure_combo.addItems(["Scale", "Ordinal", "Nominal"])
        var_layout.addRow("Measure:", self.measure_combo)

        # 角色
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Input", "Target", "Both", "None", "Partition", "Split"])
        var_layout.addRow("Role:", self.role_combo)

        content_layout.addWidget(var_group)

        # 按钮组
        button_layout = QVBoxLayout()
        button_layout.setSpacing(8)

        self.apply_btn = QPushButton(self.i18n.get_text('dialog.apply'))
        self.apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #165DFF;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4080FF;
            }
            QPushButton:pressed {
                background-color: #0E42D2;
            }
        """)
        self.apply_btn.clicked.connect(self.apply_changes)

        self.reset_btn = QPushButton(self.i18n.get_text('dialog.reset'))
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #1D2129;
                border: 1px solid #E5E6EB;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                border-color: #4080FF;
                color: #165DFF;
            }
            QPushButton:pressed {
                background-color: #F2F3F5;
            }
        """)
        self.reset_btn.clicked.connect(self.reset)

        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.reset_btn)
        content_layout.addLayout(button_layout)

        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        self.setMinimumWidth(240)
        self.setMaximumWidth(300)

    def set_variable(self, var_name, metadata):
        self.current_var_name = var_name
        self.name_edit.setText(var_name)
        
        if metadata:
            self.type_combo.setCurrentText(metadata.get('type', 'Numeric'))
            self.width_spin.setValue(metadata.get('width', 8))
            self.decimal_spin.setValue(metadata.get('decimals', 2))
            self.label_edit.setText(metadata.get('label', ''))
            self.value_labels_edit.setText(metadata.get('value_labels', ''))
            self.missing_combo.setCurrentText(metadata.get('missing', 'None'))
            self.align_combo.setCurrentText(metadata.get('align', 'Right'))
            self.measure_combo.setCurrentText(metadata.get('measure', 'Scale'))
            self.role_combo.setCurrentText(metadata.get('role', 'Input'))

    def get_variable_metadata(self):
        return {
            'type': self.type_combo.currentText(),
            'width': self.width_spin.value(),
            'decimals': self.decimal_spin.value(),
            'label': self.label_edit.text(),
            'value_labels': self.value_labels_edit.text(),
            'missing': self.missing_combo.currentText(),
            'align': self.align_combo.currentText(),
            'measure': self.measure_combo.currentText(),
            'role': self.role_combo.currentText()
        }

    def apply_changes(self):
        if self.current_var_name:
            new_name = self.name_edit.text()
            metadata = self.get_variable_metadata()
            self.sig_variable_changed.emit(new_name, metadata)

    def reset(self):
        if self.current_var_name:
            self.name_edit.setText(self.current_var_name)
            self.type_combo.setCurrentIndex(0)
            self.width_spin.setValue(8)
            self.decimal_spin.setValue(2)
            self.label_edit.clear()
            self.value_labels_edit.clear()
            self.missing_combo.setCurrentIndex(0)
            self.align_combo.setCurrentIndex(2)
            self.measure_combo.setCurrentIndex(0)
            self.role_combo.setCurrentIndex(0)
