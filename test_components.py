#!/usr/bin/env python3
"""测试输出视图组件是否能成功导入和基本功能"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'AxaltyX'))

print("开始测试导入...")
try:
    from src.axaltyx_gui.output_view.output_widget import OutputWidget
    from src.axaltyx_gui.output_view.result_table import ResultTable, ResultTableModel
    from src.axaltyx_gui.chart_view.chart_widget import ChartWidget
    from src.axaltyx_gui.tab_system.output_tab import OutputTab
    print("✅ 所有组件导入成功！")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)

print("\n开始创建组件对象...")
try:
    # 测试ResultTableModel
    headers = ["列1", "列2", "列3"]
    data = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
    model = ResultTableModel(data=data, headers=headers)
    print("✅ ResultTableModel 创建成功")
    
    print("\n测试完成！")
except Exception as e:
    print(f"❌ 创建组件对象失败: {e}")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)

print("\n✅ 所有基本功能测试通过！")
