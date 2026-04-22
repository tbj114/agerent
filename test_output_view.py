#!/usr/bin/env python3
"""简单的测试脚本，测试输出视图组件"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'AxaltyX'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from src.axaltyx_gui.tab_system.output_tab import OutputTab

def main():
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("输出视图测试")
    window.setMinimumSize(800, 600)
    
    tab_widget = QTabWidget()
    output_tab = OutputTab()
    tab_widget.addTab(output_tab, "输出")
    
    window.setCentralWidget(tab_widget)
    window.show()
    
    # 加载示例数据
    output_tab._load_sample()
    
    return app.exec()

if __name__ == "__main__":
    main()
