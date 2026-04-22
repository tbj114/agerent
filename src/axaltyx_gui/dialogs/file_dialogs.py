from PyQt6.QtWidgets import QFileDialog, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit
from PyQt6.QtCore import Qt
from axaltyx_i18n.manager import I18nManager

class OpenFileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('dialog.file.open.title'))
        self.setMinimumSize(600, 400)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(16)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        
        # 文件类型选择
        file_type_group = QHBoxLayout()
        file_type_label = QLabel(self.i18n.get_text('dialog.file.type'))
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItem('CSV (*.csv)', 'csv')
        self.file_type_combo.addItem('Excel (*.xlsx, *.xls)', 'excel')
        self.file_type_combo.addItem('SPSS (*.sav)', 'sav')
        self.file_type_combo.addItem('Stata (*.dta)', 'dta')
        self.file_type_combo.addItem('JSON (*.json)', 'json')
        file_type_group.addWidget(file_type_label)
        file_type_group.addWidget(self.file_type_combo)
        self.main_layout.addLayout(file_type_group)
        
        # 文件路径
        file_path_group = QHBoxLayout()
        file_path_label = QLabel(self.i18n.get_text('dialog.file.path'))
        self.file_path_edit = QLineEdit()
        self.browse_button = QPushButton(self.i18n.get_text('dialog.file.browse'))
        self.browse_button.clicked.connect(self.browse_file)
        file_path_group.addWidget(file_path_label)
        file_path_group.addWidget(self.file_path_edit)
        file_path_group.addWidget(self.browse_button)
        self.main_layout.addLayout(file_path_group)
        
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
    
    def browse_file(self):
        file_type = self.file_type_combo.currentData()
        filters = {
            'csv': 'CSV Files (*.csv)',
            'excel': 'Excel Files (*.xlsx *.xls)',
            'sav': 'SPSS Files (*.sav)',
            'dta': 'Stata Files (*.dta)',
            'json': 'JSON Files (*.json)'
        }
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            self.i18n.get_text('dialog.file.open.title'),
            '',
            filters.get(file_type, 'All Files (*.*)')
        )
        if file_path:
            self.file_path_edit.setText(file_path)
    
    def get_file_path(self):
        return self.file_path_edit.text()
    
    def get_file_type(self):
        return self.file_type_combo.currentData()

class SaveFileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('dialog.file.save.title'))
        self.setMinimumSize(600, 400)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(16)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        
        # 文件类型选择
        file_type_group = QHBoxLayout()
        file_type_label = QLabel(self.i18n.get_text('dialog.file.type'))
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItem('CSV (*.csv)', 'csv')
        self.file_type_combo.addItem('Excel (*.xlsx)', 'excel')
        self.file_type_combo.addItem('JSON (*.json)', 'json')
        file_type_group.addWidget(file_type_label)
        file_type_group.addWidget(self.file_type_combo)
        self.main_layout.addLayout(file_type_group)
        
        # 文件路径
        file_path_group = QHBoxLayout()
        file_path_label = QLabel(self.i18n.get_text('dialog.file.path'))
        self.file_path_edit = QLineEdit()
        self.browse_button = QPushButton(self.i18n.get_text('dialog.file.browse'))
        self.browse_button.clicked.connect(self.browse_file)
        file_path_group.addWidget(file_path_label)
        file_path_group.addWidget(self.file_path_edit)
        file_path_group.addWidget(self.browse_button)
        self.main_layout.addLayout(file_path_group)
        
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
    
    def browse_file(self):
        file_type = self.file_type_combo.currentData()
        filters = {
            'csv': 'CSV Files (*.csv)',
            'excel': 'Excel Files (*.xlsx)',
            'json': 'JSON Files (*.json)'
        }
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            self.i18n.get_text('dialog.file.save.title'),
            '',
            filters.get(file_type, 'All Files (*.*)')
        )
        if file_path:
            self.file_path_edit.setText(file_path)
    
    def get_file_path(self):
        return self.file_path_edit.text()
    
    def get_file_type(self):
        return self.file_type_combo.currentData()
