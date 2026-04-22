from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QComboBox, QLabel, QLineEdit, QGridLayout
from PyQt6.QtCore import Qt
from src.axaltyx_i18n.manager import I18nManager


class OpenFileDialog(QDialog):
    """打开文件对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('dialog.file_dialog.open_title'))
        self.setMinimumWidth(500)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # 文件类型选择
        file_type_layout = QHBoxLayout()
        file_type_layout.addWidget(QLabel(self.i18n.get_text('dialog.file_dialog.file_type') + ":"))
        
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems([
            self.i18n.get_text('dialog.file_dialog.all_files'),
            self.i18n.get_text('dialog.file_dialog.csv_files'),
            self.i18n.get_text('dialog.file_dialog.excel_files'),
            self.i18n.get_text('dialog.file_dialog.spss_files'),
            self.i18n.get_text('dialog.file_dialog.stata_files'),
            self.i18n.get_text('dialog.file_dialog.json_files')
        ])
        file_type_layout.addWidget(self.file_type_combo)
        main_layout.addLayout(file_type_layout)

        # 文件名
        file_name_layout = QHBoxLayout()
        file_name_layout.addWidget(QLabel("文件名:"))
        
        self.file_name_edit = QLineEdit()
        file_name_layout.addWidget(self.file_name_edit, 1)
        
        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self._browse_file)
        file_name_layout.addWidget(browse_btn)
        main_layout.addLayout(file_name_layout)

        # 编码
        encoding_layout = QHBoxLayout()
        encoding_layout.addWidget(QLabel(self.i18n.get_text('dialog.file_dialog.encoding') + ":"))
        
        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems(['UTF-8', 'GBK', 'GB2312', 'ISO-8859-1'])
        self.encoding_combo.setCurrentText('UTF-8')
        encoding_layout.addWidget(self.encoding_combo)
        main_layout.addLayout(encoding_layout)

        # 按钮组
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        button_layout.setSpacing(8)

        cancel_btn = QPushButton(self.i18n.get_text('dialog.cancel'))
        cancel_btn.clicked.connect(self.reject)

        open_btn = QPushButton(self.i18n.get_text('dialog.ok'))
        open_btn.setStyleSheet("""
            QPushButton {
                background-color: #165DFF;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #4080FF;
            }
        """)
        open_btn.clicked.connect(self.accept)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(open_btn)
        main_layout.addLayout(button_layout)

    def _browse_file(self):
        """浏览文件"""
        file_types = {
            self.i18n.get_text('dialog.file_dialog.all_files'): "*.*",
            self.i18n.get_text('dialog.file_dialog.csv_files'): "*.csv",
            self.i18n.get_text('dialog.file_dialog.excel_files'): "*.xlsx *.xls",
            self.i18n.get_text('dialog.file_dialog.spss_files'): "*.sav",
            self.i18n.get_text('dialog.file_dialog.stata_files'): "*.dta",
            self.i18n.get_text('dialog.file_dialog.json_files'): "*.json"
        }
        
        file_type = file_types.get(self.file_type_combo.currentText(), "*.*")
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.i18n.get_text('dialog.file_dialog.open_title'),
            "",
            f"{self.file_type_combo.currentText()} ({file_type})"
        )
        
        if file_path:
            self.file_name_edit.setText(file_path)

    def get_selected_file(self) -> dict:
        """获取选中的文件信息
        
        Returns:
            dict: {path, type, encoding}
        """
        file_path = self.file_name_edit.text()
        file_type = self.file_type_combo.currentText()
        encoding = self.encoding_combo.currentText()
        
        return {
            'path': file_path,
            'type': file_type,
            'encoding': encoding
        }


class SaveFileDialog(QDialog):
    """保存文件对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('dialog.file_dialog.save_title'))
        self.setMinimumWidth(500)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # 文件类型选择
        file_type_layout = QHBoxLayout()
        file_type_layout.addWidget(QLabel(self.i18n.get_text('dialog.file_dialog.file_type') + ":"))
        
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems([
            self.i18n.get_text('dialog.file_dialog.csv_files'),
            self.i18n.get_text('dialog.file_dialog.excel_files'),
            self.i18n.get_text('dialog.file_dialog.spss_files'),
            self.i18n.get_text('dialog.file_dialog.json_files')
        ])
        file_type_layout.addWidget(self.file_type_combo)
        main_layout.addLayout(file_type_layout)

        # 文件名
        file_name_layout = QHBoxLayout()
        file_name_layout.addWidget(QLabel("文件名:"))
        
        self.file_name_edit = QLineEdit()
        file_name_layout.addWidget(self.file_name_edit, 1)
        
        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self._browse_file)
        file_name_layout.addWidget(browse_btn)
        main_layout.addLayout(file_name_layout)

        # 编码
        encoding_layout = QHBoxLayout()
        encoding_layout.addWidget(QLabel(self.i18n.get_text('dialog.file_dialog.encoding') + ":"))
        
        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems(['UTF-8', 'GBK', 'GB2312', 'ISO-8859-1'])
        self.encoding_combo.setCurrentText('UTF-8')
        encoding_layout.addWidget(self.encoding_combo)
        main_layout.addLayout(encoding_layout)

        # 按钮组
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        button_layout.setSpacing(8)

        cancel_btn = QPushButton(self.i18n.get_text('dialog.cancel'))
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton(self.i18n.get_text('dialog.ok'))
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #165DFF;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #4080FF;
            }
        """)
        save_btn.clicked.connect(self.accept)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        main_layout.addLayout(button_layout)

    def _browse_file(self):
        """浏览文件"""
        file_types = {
            self.i18n.get_text('dialog.file_dialog.csv_files'): "*.csv",
            self.i18n.get_text('dialog.file_dialog.excel_files'): "*.xlsx",
            self.i18n.get_text('dialog.file_dialog.spss_files'): "*.sav",
            self.i18n.get_text('dialog.file_dialog.json_files'): "*.json"
        }
        
        file_type = file_types.get(self.file_type_combo.currentText(), "*.csv")
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self.i18n.get_text('dialog.file_dialog.save_title'),
            "",
            f"{self.file_type_combo.currentText()} ({file_type})"
        )
        
        if file_path:
            self.file_name_edit.setText(file_path)

    def get_save_path(self) -> dict:
        """获取保存路径信息
        
        Returns:
            dict: {path, type, encoding}
        """
        file_path = self.file_name_edit.text()
        file_type = self.file_type_combo.currentText()
        encoding = self.encoding_combo.currentText()
        
        return {
            'path': file_path,
            'type': file_type,
            'encoding': encoding
        }
