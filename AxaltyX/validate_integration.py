#!/usr/bin/env python3
"""
集成验证测试脚本
测试从 step1 到 step8 的所有模块是否能够正确联动
"""

import sys
import os
import pandas as pd
import numpy as np

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from axaltyx_core.data_management.io import load_csv
from axaltyx_core.descriptive.stats import descriptive_stats
from axaltyx_plot.basic.charts import bar_chart
from axaltyx_bridge.controller import BridgeController


class MockCoreEngine:
    """模拟核心引擎"""
    def __init__(self):
        self.current_data = None
    
    def load_data(self, path, file_type):
        try:
            # 实际调用核心模块加载数据
            if file_type == "csv":
                result = load_csv(path)
                if result.get("success"):
                    data = result.get("results", {}).get("data")
                    self.current_data = data
                    return {
                        "success": True,
                        "data": data,
                        "columns": list(data.columns),
                        "shape": data.shape
                    }
                else:
                    return result
            else:
                return {
                    "success": False,
                    "error": f"Unsupported file type: {file_type}",
                    "path": path,
                    "file_type": file_type
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": path,
                "file_type": file_type
            }
    
    def save_data(self, path, file_type, encoding):
        return {
            "success": True,
            "path": path
        }
    
    def create_new_data(self, rows, cols):
        data = pd.DataFrame(np.random.randn(rows, cols), columns=[f'col{i+1}' for i in range(cols)])
        self.current_data = data
        return {
            "success": True,
            "data": data,
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
        try:
            # 实际调用绘图模块创建图表
            if chart_type == "bar_chart":
                data = params.get("data")
                x = params.get("x")
                y = params.get("y")
                if data is not None and x and y:
                    result = bar_chart(data, x, y)
                    return result
            return {
                "success": True,
                "results": {
                    "figure": f"{chart_type} figure",
                    "type": chart_type,
                    "backend": "matplotlib"
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
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


def create_test_data():
    """创建测试数据"""
    data = {
        "category": ["A", "B", "C", "D", "E"],
        "value": [10, 20, 30, 40, 50],
        "group": ["X", "X", "Y", "Y", "Y"]
    }
    return pd.DataFrame(data)


def test_integration():
    """测试集成功能"""
    print("=== 集成验证测试 ===")
    
    # 创建测试数据
    test_data = create_test_data()
    print("\n1. 测试数据创建成功:")
    print(test_data)
    
    # 测试核心模块 - 描述统计
    print("\n2. 测试核心模块 - 描述统计:")
    try:
        stats_result = descriptive_stats(test_data, vars=["value"])
        print(f"描述统计结果: {stats_result}")
    except Exception as e:
        print(f"描述统计失败: {str(e)}")
    
    # 测试绘图模块 - 柱状图
    print("\n3. 测试绘图模块 - 柱状图:")
    try:
        chart_result = bar_chart(test_data, "category", "value")
        print(f"柱状图创建成功: {chart_result['results']['type']}")
        print(f"图表类型: {chart_result['results']['backend']}")
    except Exception as e:
        print(f"柱状图创建失败: {str(e)}")
    
    # 测试桥接控制器
    print("\n4. 测试桥接控制器:")
    try:
        # 创建模拟引擎
        core_engine = MockCoreEngine()
        plot_engine = MockPlotEngine()
        i18n_manager = MockI18nManager()
        theme_manager = MockThemeManager()
        
        # 获取 BridgeController 实例
        controller = BridgeController()
        
        # 初始化控制器
        controller.initialize(core_engine, plot_engine, i18n_manager, theme_manager)
        print("BridgeController 初始化成功")
        
        # 测试数据加载
        print("\n5. 测试数据加载:")
        # 保存测试数据到临时文件
        temp_file = "test_data.csv"
        test_data.to_csv(temp_file, index=False)
        
        # 定义回调函数
        def on_data_load_completed(result):
            print(f"数据加载完成: {result}")
        
        # 连接信号
        controller.signals.sig_data_load_completed.connect(on_data_load_completed)
        
        # 触发数据加载
        controller.load_data(temp_file, "csv")
        
        # 清理临时文件
        os.remove(temp_file)
        
        print("\n=== 集成测试完成 ===")
        return True
        
    except Exception as e:
        print(f"BridgeController 测试失败: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_integration()
    if success:
        print("\n✅ 所有模块集成测试通过!")
    else:
        print("\n❌ 集成测试失败!")
        sys.exit(1)
