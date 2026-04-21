import sys
import os
sys.path.insert(0, 'AxaltyX/src')

from axaltyx_plot.basic.charts import bar_chart
import pandas as pd

# 创建包含中文的数据框
df = pd.DataFrame({"类别": ["苹果", "香蕉", "橙子", "葡萄", "西瓜"], "销量": [100, 150, 120, 90, 80]})

# 生成条形图
print("正在生成中文条形图...")
result = bar_chart(df, "类别", "销量", title="水果销量统计", xlabel="水果类别", ylabel="销量")

if result["success"]:
    print("条形图生成成功!")
    print(f"图表类型: {result['results']['type']}")
    
    # 保存图表为图片
    output_path = "chinese_bar_chart.png"
    if "figure" in result["results"]:
        fig = result["results"]["figure"]
        backend = result["results"].get("backend", "matplotlib")
        try:
            if backend == "plotly":
                fig.write_image(output_path)
            else:  # matplotlib
                fig.savefig(output_path, bbox_inches='tight', dpi=100)
            print(f"图表已保存为: {output_path}")
            print(f"文件大小: {os.path.getsize(output_path) / 1024:.2f} KB")
        except Exception as e:
            print(f"保存图表失败: {e}")
    else:
        print("图表对象不存在")
else:
    print(f"条形图生成失败: {result['error']}")