import sys
import os
sys.path.insert(0, '/workspace/AxaltyX')

from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from src.axaltyx_gui.panels import NavigationPanel, PropertyPanel


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Panels")
        self.setGeometry(100, 100, 1200, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        
        # 导航面板
        self.nav_panel = NavigationPanel()
        self.nav_panel.sig_analysis_selected.connect(self._on_analysis_selected)
        layout.addWidget(self.nav_panel)
        
        # 内容区域
        content = QWidget()
        content.setStyleSheet("background-color: #f0f0f0;")
        layout.addWidget(content, 1)
        
        # 属性面板
        self.prop_panel = PropertyPanel()
        self.prop_panel.sig_variable_changed.connect(self._on_variable_changed)
        # 测试设置变量
        self.prop_panel.set_variable("VAR00001", {
            "type": "Numeric",
            "width": 8,
            "decimals": 2,
            "label": "测试变量"
        })
        layout.addWidget(self.prop_panel)
        
    def _on_analysis_selected(self, analysis_id, params):
        print(f"Selected analysis: {analysis_id}, params: {params}")
        
    def _on_variable_changed(self, var_name, metadata):
        print(f"Variable changed: {var_name}, metadata: {metadata}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    print("Test window successfully launched!")
    print("Panels are working correctly!")
    sys.exit(0)
