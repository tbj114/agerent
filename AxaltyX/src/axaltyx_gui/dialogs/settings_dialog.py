from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTabWidget, QWidget, QFormLayout, QComboBox, QSpinBox, QCheckBox, QLineEdit, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from src.axaltyx_i18n.manager import I18nManager


class SettingsDialog(QDialog):
    """设置对话框"""

    sig_settings_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle("设置")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # 标签页
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # 常规设置
        general_tab = QWidget()
        general_layout = QFormLayout(general_tab)
        
        # 语言
        self.language_combo = self._create_language_combo()
        general_layout.addRow("语言:", self.language_combo)
        
        # 主题
        self.theme_combo = self._create_theme_combo()
        general_layout.addRow("主题:", self.theme_combo)
        
        # 启动时
        self.startup_combo = self._create_startup_combo()
        general_layout.addRow("启动时:", self.startup_combo)
        
        # 自动保存
        self.auto_save_checkbox = QCheckBox("自动保存")
        general_layout.addRow(self.auto_save_checkbox)
        
        # 自动保存间隔
        self.auto_save_interval_spin = self._create_auto_save_interval_spin()
        general_layout.addRow("自动保存间隔(分钟):", self.auto_save_interval_spin)
        
        # 最近文件数量
        self.recent_files_spin = self._create_recent_files_spin()
        general_layout.addRow("最近文件数量:", self.recent_files_spin)
        
        # 小数位数
        self.decimal_places_spin = self._create_decimal_places_spin()
        general_layout.addRow("小数位数:", self.decimal_places_spin)
        
        self.tab_widget.addTab(general_tab, "常规")

        # 外观设置
        appearance_tab = QWidget()
        appearance_layout = QFormLayout(appearance_tab)
        
        # 字体大小
        self.font_size_spin = self._create_font_size_spin()
        appearance_layout.addRow("字体大小:", self.font_size_spin)
        
        # 表格字体
        self.font_combo = self._create_font_combo()
        appearance_layout.addRow("表格字体:", self.font_combo)
        
        # 缩放级别
        self.zoom_combo = self._create_zoom_combo()
        appearance_layout.addRow("缩放级别:", self.zoom_combo)
        
        self.tab_widget.addTab(appearance_tab, "外观")

        # 数据设置
        data_tab = QWidget()
        data_layout = QFormLayout(data_tab)
        
        # 默认行数
        self.default_rows_spin = self._create_default_rows_spin()
        data_layout.addRow("默认行数:", self.default_rows_spin)
        
        # 默认列数
        self.default_cols_spin = self._create_default_cols_spin()
        data_layout.addRow("默认列数:", self.default_cols_spin)
        
        # 小数分隔符
        self.decimal_separator_combo = self._create_decimal_separator_combo()
        data_layout.addRow("小数分隔符:", self.decimal_separator_combo)
        
        # 千位分隔符
        self.thousand_separator_combo = self._create_thousand_separator_combo()
        data_layout.addRow("千位分隔符:", self.thousand_separator_combo)
        
        self.tab_widget.addTab(data_tab, "数据")

        # 输出设置
        output_tab = QWidget()
        output_layout = QFormLayout(output_tab)
        
        # 默认图表格式
        self.chart_format_combo = self._create_chart_format_combo()
        output_layout.addRow("默认图表格式:", self.chart_format_combo)
        
        # 默认图表分辨率
        self.chart_dpi_spin = self._create_chart_dpi_spin()
        output_layout.addRow("默认图表分辨率:", self.chart_dpi_spin)
        
        # 表格输出格式
        self.table_format_combo = self._create_table_format_combo()
        output_layout.addRow("表格输出格式:", self.table_format_combo)
        
        self.tab_widget.addTab(output_tab, "输出")

        # 性能设置
        performance_tab = QWidget()
        performance_layout = QFormLayout(performance_tab)
        
        # 最大线程数
        self.max_threads_spin = self._create_max_threads_spin()
        performance_layout.addRow("最大线程数:", self.max_threads_spin)
        
        # 虚拟滚动
        self.virtual_scroll_checkbox = QCheckBox("虚拟滚动")
        performance_layout.addRow(self.virtual_scroll_checkbox)
        
        # 缓存大小
        self.cache_size_spin = self._create_cache_size_spin()
        performance_layout.addRow("缓存大小(MB):", self.cache_size_spin)
        
        self.tab_widget.addTab(performance_tab, "性能")

        # 按钮组
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        button_layout.setSpacing(8)

        reset_btn = QPushButton("重置为默认")
        reset_btn.clicked.connect(self.reset_to_default)

        cancel_btn = QPushButton(self.i18n.get_text('dialog.cancel'))
        cancel_btn.clicked.connect(self.reject)

        ok_btn = QPushButton(self.i18n.get_text('dialog.ok'))
        ok_btn.setStyleSheet("""
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
        ok_btn.clicked.connect(self.apply_settings)

        button_layout.addWidget(reset_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)
        main_layout.addLayout(button_layout)

    def _create_language_combo(self):
        combo = QComboBox()
        combo.addItems(['简体中文', 'English', '日本語'])
        combo.setCurrentText('简体中文')
        return combo

    def _create_theme_combo(self):
        combo = QComboBox()
        combo.addItems(['亮色主题', '暗色主题'])
        combo.setCurrentText('亮色主题')
        return combo

    def _create_startup_combo(self):
        combo = QComboBox()
        combo.addItems(['显示欢迎屏幕', '打开空白数据集', '打开最近文件'])
        combo.setCurrentText('显示欢迎屏幕')
        return combo

    def _create_auto_save_interval_spin(self):
        spin = QSpinBox()
        spin.setMinimum(1)
        spin.setMaximum(60)
        spin.setValue(5)
        return spin

    def _create_recent_files_spin(self):
        spin = QSpinBox()
        spin.setMinimum(1)
        spin.setMaximum(20)
        spin.setValue(10)
        return spin

    def _create_decimal_places_spin(self):
        spin = QSpinBox()
        spin.setMinimum(0)
        spin.setMaximum(10)
        spin.setValue(2)
        return spin

    def _create_font_size_spin(self):
        spin = QSpinBox()
        spin.setMinimum(8)
        spin.setMaximum(24)
        spin.setValue(14)
        return spin

    def _create_font_combo(self):
        combo = QComboBox()
        combo.addItems(['Microsoft YaHei', 'PingFang SC', 'Noto Sans SC', 'Arial', 'Times New Roman'])
        combo.setCurrentText('Microsoft YaHei')
        return combo

    def _create_zoom_combo(self):
        combo = QComboBox()
        combo.addItems(['75%', '100%', '125%', '150%', '200%'])
        combo.setCurrentText('100%')
        return combo

    def _create_default_rows_spin(self):
        spin = QSpinBox()
        spin.setMinimum(10)
        spin.setMaximum(1000)
        spin.setValue(100)
        return spin

    def _create_default_cols_spin(self):
        spin = QSpinBox()
        spin.setMinimum(5)
        spin.setMaximum(100)
        spin.setValue(20)
        return spin

    def _create_decimal_separator_combo(self):
        combo = QComboBox()
        combo.addItems(['.', ','])
        combo.setCurrentText('.')
        return combo

    def _create_thousand_separator_combo(self):
        combo = QComboBox()
        combo.addItems([',', '.', ' '])
        combo.setCurrentText(',')
        return combo

    def _create_chart_format_combo(self):
        combo = QComboBox()
        combo.addItems(['PNG', 'JPG', 'SVG', 'PDF'])
        combo.setCurrentText('PNG')
        return combo

    def _create_chart_dpi_spin(self):
        spin = QSpinBox()
        spin.setMinimum(72)
        spin.setMaximum(600)
        spin.setValue(300)
        return spin

    def _create_table_format_combo(self):
        combo = QComboBox()
        combo.addItems(['HTML', 'CSV', 'Excel', 'Plain Text'])
        combo.setCurrentText('HTML')
        return combo

    def _create_max_threads_spin(self):
        spin = QSpinBox()
        spin.setMinimum(1)
        spin.setMaximum(16)
        spin.setValue(4)
        return spin

    def _create_cache_size_spin(self):
        spin = QSpinBox()
        spin.setMinimum(10)
        spin.setMaximum(500)
        spin.setValue(100)
        return spin

    def get_settings(self) -> dict:
        """获取设置
        
        Returns:
            dict: 设置字典
        """
        # 语言映射
        lang_map = {
            '简体中文': 'zh_CN',
            'English': 'en_US',
            '日本語': 'ja_JP'
        }
        
        # 主题映射
        theme_map = {
            '亮色主题': 'light',
            '暗色主题': 'dark'
        }
        
        # 启动动作映射
        startup_map = {
            '显示欢迎屏幕': 'welcome',
            '打开空白数据集': 'empty',
            '打开最近文件': 'recent'
        }
        
        # 缩放级别映射
        zoom_map = {
            '75%': 75,
            '100%': 100,
            '125%': 125,
            '150%': 150,
            '200%': 200
        }
        
        # 获取设置值
        return {
            'general': {
                'language': lang_map.get(self.language_combo.currentText(), 'zh_CN'),
                'theme': theme_map.get(self.theme_combo.currentText(), 'light'),
                'startup_action': startup_map.get(self.startup_combo.currentText(), 'welcome'),
                'auto_save': self.auto_save_checkbox.isChecked(),
                'auto_save_interval': self.auto_save_interval_spin.value(),
                'recent_files_count': self.recent_files_spin.value(),
                'decimal_places': self.decimal_places_spin.value()
            },
            'appearance': {
                'font_size': self.font_size_spin.value(),
                'table_font': self.font_combo.currentText(),
                'zoom_level': zoom_map.get(self.zoom_combo.currentText(), 100)
            },
            'data': {
                'default_rows': self.default_rows_spin.value(),
                'default_cols': self.default_cols_spin.value(),
                'decimal_separator': self.decimal_separator_combo.currentText(),
                'thousand_separator': self.thousand_separator_combo.currentText()
            },
            'output': {
                'chart_format': self.chart_format_combo.currentText(),
                'chart_dpi': self.chart_dpi_spin.value(),
                'table_format': self.table_format_combo.currentText()
            },
            'performance': {
                'max_threads': self.max_threads_spin.value(),
                'virtual_scroll': self.virtual_scroll_checkbox.isChecked(),
                'cache_size': self.cache_size_spin.value()
            }
        }

    def apply_settings(self) -> None:
        """应用设置"""
        settings = self.get_settings()
        self.sig_settings_changed.emit(settings)
        self.accept()

    def reset_to_default(self):
        """重置为默认设置"""
        # 重置常规设置
        self.language_combo.setCurrentText('简体中文')
        self.theme_combo.setCurrentText('亮色主题')
        self.startup_combo.setCurrentText('显示欢迎屏幕')
        self.auto_save_checkbox.setChecked(True)
        self.auto_save_interval_spin.setValue(5)
        self.recent_files_spin.setValue(10)
        self.decimal_places_spin.setValue(2)
        
        # 重置外观设置
        self.font_size_spin.setValue(14)
        self.font_combo.setCurrentText('Microsoft YaHei')
        self.zoom_combo.setCurrentText('100%')
        
        # 重置数据设置
        self.default_rows_spin.setValue(100)
        self.default_cols_spin.setValue(20)
        self.decimal_separator_combo.setCurrentText('.')
        self.thousand_separator_combo.setCurrentText(',')
        
        # 重置输出设置
        self.chart_format_combo.setCurrentText('PNG')
        self.chart_dpi_spin.setValue(300)
        self.table_format_combo.setCurrentText('HTML')
        
        # 重置性能设置
        self.max_threads_spin.setValue(4)
        self.virtual_scroll_checkbox.setChecked(True)
        self.cache_size_spin.setValue(100)
