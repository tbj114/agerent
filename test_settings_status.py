#!/usr/bin/env python3
"""测试设置和状态栏组件"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'AxaltyX'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QComboBox, QGroupBox, QHBoxLayout
from src.axaltyx_gui.settings import AppSettings, ThemeManager
from src.axaltyx_gui.statusbar import AxaltyXStatusBar

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("设置和状态栏测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 初始化设置和主题管理
        self.settings = AppSettings()
        self.theme_manager = ThemeManager()
        
        # 创建状态栏
        self.status_bar = AxaltyXStatusBar(self)
        self.setStatusBar(self.status_bar)
        
        # 创建中心部件
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # 测试设置
        settings_group = QGroupBox("设置测试")
        settings_layout = QVBoxLayout(settings_group)
        
        # 语言选择
        lang_layout = QHBoxLayout()
        lang_label = QLabel("语言:")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["中文 (zh_CN)", "English (en_US)", "日本語 (ja_JP)"])
        self.lang_combo.currentIndexChanged.connect(self._on_language_change)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        settings_layout.addLayout(lang_layout)
        
        # 主题选择
        theme_layout = QHBoxLayout()
        theme_label = QLabel("主题:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["亮色 (light)", "暗色 (dark)"])
        self.theme_combo.currentIndexChanged.connect(self._on_theme_change)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        settings_layout.addLayout(theme_layout)
        
        # 测试按钮
        test_button = QPushButton("测试状态栏消息")
        test_button.clicked.connect(self._test_status_message)
        settings_layout.addWidget(test_button)
        
        # 数据信息按钮
        data_button = QPushButton("更新数据信息")
        data_button.clicked.connect(self._update_data_info)
        settings_layout.addWidget(data_button)
        
        layout.addWidget(settings_group)
        
        # 显示当前设置
        self.info_label = QLabel()
        self._update_info_label()
        layout.addWidget(self.info_label)
        
        self.setCentralWidget(central_widget)
        
        # 初始更新状态栏
        self.status_bar.update_data_info(100, 100)
        self.status_bar.show_message("测试窗口已启动")
    
    def _on_language_change(self, index):
        lang_map = {0: "zh_CN", 1: "en_US", 2: "ja_JP"}
        lang_code = lang_map.get(index, "zh_CN")
        self.status_bar.update_language_indicator(lang_code)
        self.settings.set("general.language", lang_code)
        self._update_info_label()
    
    def _on_theme_change(self, index):
        theme_map = {0: "light", 1: "dark"}
        theme_name = theme_map.get(index, "light")
        self.theme_manager.apply_theme(theme_name, QApplication.instance())
        self.settings.set("general.theme", theme_name)
        self._update_info_label()
    
    def _test_status_message(self):
        self.status_bar.show_message("这是一条测试消息", 3000)
    
    def _update_data_info(self):
        import random
        rows = random.randint(50, 200)
        cols = random.randint(10, 50)
        self.status_bar.update_data_info(rows, cols)
    
    def _update_info_label(self):
        current_theme = self.settings.get("general.theme", "light")
        current_lang = self.settings.get("general.language", "zh_CN")
        info = f"当前设置:\n" \
               f"主题: {current_theme}\n" \
               f"语言: {current_lang}\n"
        self.info_label.setText(info)

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    main()
