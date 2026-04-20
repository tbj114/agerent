#!/usr/bin/env python3
"""
Bridge 层测试脚本
验证信号发射和槽函数调用
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from axaltyx_bridge.controller import BridgeController


class MockCoreEngine:
    """模拟核心引擎"""
    
    def load_data(self, path, file_type):
        """模拟加载数据"""
        print(f"MockCoreEngine.load_data called with path={path}, file_type={file_type}")
        return {
            "success": True,
            "data": "mock_data",
            "columns": ["col1", "col2"],
            "shape": (10, 2)
        }
    
    def save_data(self, path, file_type, encoding):
        """模拟保存数据"""
        print(f"MockCoreEngine.save_data called with path={path}, file_type={file_type}, encoding={encoding}")
        return {
            "success": True,
            "path": path
        }
    
    def new_dataset(self, rows, cols):
        """模拟新建数据集"""
        print(f"MockCoreEngine.new_dataset called with rows={rows}, cols={cols}")
        return {
            "success": True,
            "data": "mock_new_data",
            "shape": (rows, cols)
        }
    
    def update_data(self, change_info):
        """模拟更新数据"""
        print(f"MockCoreEngine.update_data called with change_info={change_info}")
    
    def update_variable(self, var_name, metadata):
        """模拟更新变量"""
        print(f"MockCoreEngine.update_variable called with var_name={var_name}, metadata={metadata}")


class MockPlotEngine:
    """模拟绘图引擎"""
    
    def export_chart(self, chart, path, format):
        """模拟导出图表"""
        print(f"MockPlotEngine.export_chart called with path={path}, format={format}")
        return {
            "success": True,
            "path": path,
            "format": format
        }


class MockI18NManager:
    """模拟国际化管理器"""
    
    def set_language(self, lang_code):
        """模拟设置语言"""
        print(f"MockI18NManager.set_language called with lang_code={lang_code}")


class MockThemeManager:
    """模拟主题管理器"""
    
    def set_theme(self, theme_name):
        """模拟设置主题"""
        print(f"MockThemeManager.set_theme called with theme_name={theme_name}")


def test_bridge_controller():
    """测试 BridgeController"""
    print("Testing BridgeController...")
    
    # 创建 BridgeController 实例
    controller = BridgeController()
    
    # 创建模拟引擎
    core_engine = MockCoreEngine()
    plot_engine = MockPlotEngine()
    i18n_manager = MockI18NManager()
    theme_manager = MockThemeManager()
    
    # 初始化控制器
    controller.initialize(core_engine, plot_engine, i18n_manager, theme_manager)
    
    # 测试数据操作
    print("\n=== Testing data operations ===")
    controller.load_data("test.csv", "csv")
    controller.save_data("output.csv", "csv", "utf-8")
    controller.new_dataset(50, 5)
    
    # 测试 UI 操作
    print("\n=== Testing UI operations ===")
    controller.change_language("zh_CN")
    controller.change_theme("arco_dark")
    controller.update_settings({"font_size": 12, "theme": "dark"})
    
    # 测试分析操作
    print("\n=== Testing analysis operations ===")
    analysis_params = {
        "vars": ["var1", "var2"],
        "stats": ["mean", "std"]
    }
    controller.run_analysis("descriptive_stats", analysis_params)
    
    # 测试图表操作
    print("\n=== Testing chart operations ===")
    chart_params = {
        "data": "mock_data",
        "x": "category",
        "y": "value"
    }
    controller.create_chart("bar_chart", chart_params)
    controller.export_chart("chart1", "chart.png", "png")
    
    # 测试事件系统
    print("\n=== Testing event system ===")
    
    def test_event_handler(data):
        print(f"Event handler called with data={data}")
    
    # 订阅事件
    subscription_id = controller.subscribe("test_event", test_event_handler)
    print(f"Subscribed to test_event with id={subscription_id}")
    
    # 发布事件
    controller.publish("test_event", {"message": "Test event data"})
    
    # 取消订阅
    controller.unsubscribe(subscription_id)
    print("Unsubscribed from test_event")
    
    # 再次发布事件（应该不会被处理）
    controller.publish("test_event", {"message": "Test event data again"})
    
    print("\nBridgeController test completed!")


if __name__ == "__main__":
    test_bridge_controller()
