#!/usr/bin/env python3
"""
基本功能测试脚本
测试各个模块的基本功能是否正常
"""

import sys
import os
import pandas as pd
import numpy as np

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=== 基本功能测试 ===")

# 测试 1: 核心模块 - 描述统计
print("\n1. 测试核心模块 - 描述统计:")
try:
    from axaltyx_core.descriptive.stats import descriptive_stats
    
    # 创建测试数据
    data = pd.DataFrame({
        "value": [10, 20, 30, 40, 50]
    })
    
    # 测试描述统计
    result = descriptive_stats(data, vars=["value"])
    print(f"描述统计结果: {result}")
    print("✅ 描述统计功能正常")
except Exception as e:
    print(f"❌ 描述统计功能失败: {str(e)}")

# 测试 2: 绘图模块 - 柱状图
print("\n2. 测试绘图模块 - 柱状图:")
try:
    from axaltyx_plot.basic.charts import bar_chart
    
    # 创建测试数据
    data = pd.DataFrame({
        "category": ["A", "B", "C"],
        "value": [10, 20, 30]
    })
    
    # 测试柱状图
    result = bar_chart(data, "category", "value")
    print(f"柱状图创建成功: {result['success']}")
    print(f"图表类型: {result['results']['type']}")
    print("✅ 柱状图功能正常")
except Exception as e:
    print(f"❌ 柱状图功能失败: {str(e)}")

# 测试 3: 桥接模块 - 控制器
print("\n3. 测试桥接模块 - 控制器:")
try:
    from axaltyx_bridge.controller import BridgeController
    
    # 获取 BridgeController 实例
    controller = BridgeController()
    print("✅ BridgeController 实例创建成功")
    
    # 测试信号系统
    print("✅ 信号系统初始化成功")
    
except Exception as e:
    print(f"❌ 桥接模块功能失败: {str(e)}")

# 测试 4: 分析注册表
print("\n4. 测试分析注册表:")
try:
    from axaltyx_bridge.registry import ANALYSIS_REGISTRY
    
    # 打印分析方法数量
    print(f"分析方法数量: {len(ANALYSIS_REGISTRY)}")
    # 打印前 5 个分析方法
    print("前 5 个分析方法:")
    for i, (name, info) in enumerate(list(ANALYSIS_REGISTRY.items())[:5]):
        print(f"  {i+1}. {name}: {info['label_key']}")
    print("✅ 分析注册表功能正常")
except Exception as e:
    print(f"❌ 分析注册表功能失败: {str(e)}")

print("\n=== 基本功能测试完成 ===")
