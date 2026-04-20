#!/usr/bin/env python3
"""
Bridge 层验证测试脚本
"""

import sys
from PyQt6.QtCore import QCoreApplication
from axaltyx_bridge.controller import BridgeController


class MockCoreEngine:
    """模拟核心引擎"""
    def __init__(self):
        self.current_data = None
    
    def load_data(self, path, file_type):
        return {
            "success": True,
            "data": f"Loaded data from {path}",
            "columns": ["col1", "col2"],
            "shape": (10, 2)
        }
    
    def save_data(self, path, file_type, encoding):
        return {
            "success": True,
            "path": path
        }
    
    def create_new_data(self, rows, cols):
        return {
            "success": True,
            "data": f"New data with {rows} rows and {cols} cols",
            "shape": (rows, cols)
        }
    
    def update_data(self, change_info):
        pass
    
    def update_variable_metadata(self, var_name, metadata):
        pass
    
    def get_current_data(self):
        return self.current_data
    
    def set_current_data(self, data):
        self.current_data = data


class MockPlotEngine:
    """模拟绘图引擎"""
    def create_chart(self, chart_type, params):
        return {
            "success": True,
            "results": {
                "figure": f"{chart_type} figure",
                "type": chart_type,
                "backend": "matplotlib"
            }
        }
    
    def export_chart(self, figure, path, format):
        return {
            "success": True,
            "path": path,
            "format": format,
            "file_size": 1024,
            "dpi": 300
        }


class MockI18nManager:
    """模拟国际化管理器"""
    def set_language(self, lang_code):
        pass


class MockThemeManager:
    """模拟主题管理器"""
    def set_theme(self, theme_name):
        pass


def test_bridge_signals():
    """测试信号发射和槽函数调用"""
    print("=== 测试 Bridge 层信号和槽 ===")
    
    # 创建应用
    app = QCoreApplication(sys.argv)
    
    # 创建模拟引擎
    core_engine = MockCoreEngine()
    plot_engine = MockPlotEngine()
    i18n_manager = MockI18nManager()
    theme_manager = MockThemeManager()
    
    # 获取 BridgeController 实例
    controller = BridgeController()
    
    # 初始化控制器
    controller.initialize(core_engine, plot_engine, i18n_manager, theme_manager)
    
    # 测试数据加载信号
    print("\n1. 测试数据加载信号")
    def on_data_load_completed(result):
        print(f"数据加载完成: {result}")
    
    # 连接信号
    controller.signals.sig_data_load_completed.connect(on_data_load_completed)
    
    # 触发数据加载
    controller.load_data("test.csv", "csv")
    
    # 测试分析请求信号
    print("\n2. 测试分析请求信号")
    def on_analysis_completed(analysis_name, result):
        print(f"分析完成: {analysis_name}, {result}")
    
    # 连接信号
    controller.signals.sig_analysis_completed.connect(on_analysis_completed)
    
    # 触发分析请求
    controller.run_analysis("descriptive_stats", {"vars": ["col1", "col2"]})
    
    # 测试图表创建信号
    print("\n3. 测试图表创建信号")
    def on_chart_created(chart_id, figure):
        print(f"图表创建完成: {chart_id}, {figure}")
    
    # 连接信号
    controller.signals.sig_chart_created.connect(on_chart_created)
    
    # 触发图表创建
    controller.create_chart("bar_chart", {"x": "category", "y": "value"})
    
    # 测试命令执行
    print("\n4. 测试命令执行")
    from axaltyx_bridge.commands.commands import EditCellCommand
    
    # 创建命令
    command = EditCellCommand(0, 0, "old", "new")
    
    # 执行命令
    controller.execute_command(command)
    
    # 测试撤销
    print("\n5. 测试撤销命令")
    controller.undo()
    
    print("\n=== 测试完成 ===")
    
    # 退出应用
    app.quit()


if __name__ == "__main__":
    test_bridge_signals()
