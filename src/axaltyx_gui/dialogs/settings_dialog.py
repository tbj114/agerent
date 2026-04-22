from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTabWidget, QWidget, QCheckBox, QComboBox, QSpinBox, QLineEdit
from PyQt6.QtCore import Qt
from axaltyx_i18n.manager import I18nManager

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setWindowTitle(self.i18n.get_text('dialog.settings.title'))
        self.setMinimumSize(800, 600)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(16)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        
        # 标签页
        self.tab_widget = QTabWidget()
        
        # 一般设置
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        
        # 语言设置
        language_group = QHBoxLayout()
        language_label = QLabel(self.i18n.get_text('dialog.settings.language'))
        self.language_combo = QComboBox()
        self.language_combo.addItem('中文', 'zh_CN')
        self.language_combo.addItem('English', 'en_US')
        self.language_combo.addItem('日本語', 'ja_JP')
        language_group.addWidget(language_label)
        language_group.addWidget(self.language_combo)
        general_layout.addLayout(language_group)
        
        # 主题设置
        theme_group = QHBoxLayout()
        theme_label = QLabel(self.i18n.get_text('dialog.settings.theme'))
        self.theme_combo = QComboBox()
        self.theme_combo.addItem('亮色', 'light')
        self.theme_combo.addItem('暗色', 'dark')
        theme_group.addWidget(theme_label)
        theme_group.addWidget(self.theme_combo)
        general_layout.addLayout(theme_group)
        
        # 启动行为
        startup_group = QHBoxLayout()
        startup_label = QLabel(self.i18n.get_text('dialog.settings.startup'))
        self.startup_check = QCheckBox(self.i18n.get_text('dialog.settings.startup_recent'))
        startup_group.addWidget(startup_label)
        startup_group.addWidget(self.startup_check)
        general_layout.addLayout(startup_group)
        
        self.tab_widget.addTab(general_tab, self.i18n.get_text('dialog.settings.general'))
        
        # 外观设置
        appearance_tab = QWidget()
        appearance_layout = QVBoxLayout(appearance_tab)
        
        # 字体大小
        font_size_group = QHBoxLayout()
        font_size_label = QLabel(self.i18n.get_text('dialog.settings.font_size'))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setMinimum(8)
        self.font_size_spin.setMaximum(24)
        self.font_size_spin.setValue(12)
        font_size_group.addWidget(font_size_label)
        font_size_group.addWidget(self.font_size_spin)
        appearance_layout.addLayout(font_size_group)
        
        # 界面缩放
        scaling_group = QHBoxLayout()
        scaling_label = QLabel(self.i18n.get_text('dialog.settings.scaling'))
        self.scaling_spin = QSpinBox()
        self.scaling_spin.setMinimum(50)
        self.scaling_spin.setMaximum(200)
        self.scaling_spin.setValue(100)
        scaling_group.addWidget(scaling_label)
        scaling_group.addWidget(self.scaling_spin)
        appearance_layout.addLayout(scaling_group)
        
        self.tab_widget.addTab(appearance_tab, self.i18n.get_text('dialog.settings.appearance'))
        
        # 数据设置
        data_tab = QWidget()
        data_layout = QVBoxLayout(data_tab)
        
        # 自动保存
        autosave_group = QHBoxLayout()
        autosave_label = QLabel(self.i18n.get_text('dialog.settings.autosave'))
        self.autosave_check = QCheckBox(self.i18n.get_text('dialog.settings.autosave_enable'))
        autosave_group.addWidget(autosave_label)
        autosave_group.addWidget(self.autosave_check)
        data_layout.addLayout(autosave_group)
        
        # 自动保存间隔
        autosave_interval_group = QHBoxLayout()
        autosave_interval_label = QLabel(self.i18n.get_text('dialog.settings.autosave_interval'))
        self.autosave_interval_spin = QSpinBox()
        self.autosave_interval_spin.setMinimum(1)
        self.autosave_interval_spin.setMaximum(60)
        self.autosave_interval_spin.setValue(5)
        autosave_interval_group.addWidget(autosave_interval_label)
        autosave_interval_group.addWidget(self.autosave_interval_spin)
        data_layout.addLayout(autosave_interval_group)
        
        self.tab_widget.addTab(data_tab, self.i18n.get_text('dialog.settings.data'))
        
        # 输出设置
        output_tab = QWidget()
        output_layout = QVBoxLayout(output_tab)
        
        # 图表格式
        chart_format_group = QHBoxLayout()
        chart_format_label = QLabel(self.i18n.get_text('dialog.settings.chart_format'))
        self.chart_format_combo = QComboBox()
        self.chart_format_combo.addItem('PNG', 'png')
        self.chart_format_combo.addItem('JPG', 'jpg')
        self.chart_format_combo.addItem('SVG', 'svg')
        self.chart_format_combo.addItem('PDF', 'pdf')
        chart_format_group.addWidget(chart_format_label)
        chart_format_group.addWidget(self.chart_format_combo)
        output_layout.addLayout(chart_format_group)
        
        # 图表分辨率
        chart_dpi_group = QHBoxLayout()
        chart_dpi_label = QLabel(self.i18n.get_text('dialog.settings.chart_dpi'))
        self.chart_dpi_spin = QSpinBox()
        self.chart_dpi_spin.setMinimum(72)
        self.chart_dpi_spin.setMaximum(300)
        self.chart_dpi_spin.setValue(150)
        chart_dpi_group.addWidget(chart_dpi_label)
        chart_dpi_group.addWidget(self.chart_dpi_spin)
        output_layout.addLayout(chart_dpi_group)
        
        self.tab_widget.addTab(output_tab, self.i18n.get_text('dialog.settings.output'))
        
        # 性能设置
        performance_tab = QWidget()
        performance_layout = QVBoxLayout(performance_tab)
        
        # 线程数
        threads_group = QHBoxLayout()
        threads_label = QLabel(self.i18n.get_text('dialog.settings.threads'))
        self.threads_spin = QSpinBox()
        self.threads_spin.setMinimum(1)
        self.threads_spin.setMaximum(8)
        self.threads_spin.setValue(4)
        threads_group.addWidget(threads_label)
        threads_group.addWidget(self.threads_spin)
        performance_layout.addLayout(threads_group)
        
        # 内存限制
        memory_group = QHBoxLayout()
        memory_label = QLabel(self.i18n.get_text('dialog.settings.memory'))
        self.memory_edit = QLineEdit('2GB')
        memory_group.addWidget(memory_label)
        memory_group.addWidget(self.memory_edit)
        performance_layout.addLayout(memory_group)
        
        self.tab_widget.addTab(performance_tab, self.i18n.get_text('dialog.settings.performance'))
        
        self.main_layout.addWidget(self.tab_widget)
        
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
        
        self.reset_button = QPushButton(self.i18n.get_text('dialog.button.reset'))
        self.reset_button.setFixedWidth(100)
        self.reset_button.clicked.connect(self.reset_settings)
        
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        self.main_layout.addLayout(button_layout)
    
    def reset_settings(self):
        # 重置为默认设置
        self.language_combo.setCurrentIndex(0)
        self.theme_combo.setCurrentIndex(0)
        self.startup_check.setChecked(True)
        self.font_size_spin.setValue(12)
        self.scaling_spin.setValue(100)
        self.autosave_check.setChecked(True)
        self.autosave_interval_spin.setValue(5)
        self.chart_format_combo.setCurrentIndex(0)
        self.chart_dpi_spin.setValue(150)
        self.threads_spin.setValue(4)
        self.memory_edit.setText('2GB')
    
    def get_settings(self):
        return {
            'language': self.language_combo.currentData(),
            'theme': self.theme_combo.currentData(),
            'startup_recent': self.startup_check.isChecked(),
            'font_size': self.font_size_spin.value(),
            'scaling': self.scaling_spin.value(),
            'autosave': self.autosave_check.isChecked(),
            'autosave_interval': self.autosave_interval_spin.value(),
            'chart_format': self.chart_format_combo.currentData(),
            'chart_dpi': self.chart_dpi_spin.value(),
            'threads': self.threads_spin.value(),
            'memory': self.memory_edit.text()
        }
