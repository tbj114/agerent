import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union

# 导入绘图模块
from .basic.charts import (
    bar_chart, stacked_bar_chart, grouped_bar_chart, pie_chart, histogram,
    density_plot, scatter_plot, line_chart, area_chart, box_plot, violin_plot, error_bar_chart
)
from .advanced.advanced_charts import (
    heatmap, pair_plot, correlation_matrix, parallel_coordinates, radar_chart,
    bubble_chart, waterfall_chart, gantt_chart, sunburst_chart, treemap
)
from .statistical.stat_charts import (
    qq_plot, residual_plot, regression_plot, box_cox_plot, normal_probability_plot
)
from .interactive.interactive_charts import (
    interactive_scatter, interactive_bar, interactive_line, interactive_histogram,
    interactive_heatmap, interactive_surface
)
from .export.exporter import export_chart as export_chart_file


class PlotEngine:
    """绘图引擎，提供图表创建和导出功能"""

    def __init__(self):
        """初始化绘图引擎"""
        pass

    def create_chart(self, chart_type: str, params: dict) -> dict:
        """创建图表"""
        try:
            # 提取数据和参数
            data = params.get('data')
            if data is None:
                return {"success": False, "error": "No data provided"}
            
            # 基本图表
            if chart_type == "bar":
                return bar_chart(
                    data=data,
                    x=params.get('x'),
                    y=params.get('y'),
                    color=params.get('color'),
                    orientation=params.get('orientation', "vertical"),
                    title=params.get('title', ""),
                    xlabel=params.get('xlabel', ""),
                    ylabel=params.get('ylabel', ""),
                    figsize=params.get('figsize', (10, 6)),
                    style=params.get('style', "arco"),
                    interactive=params.get('interactive', False)
                )
            
            elif chart_type == "stacked_bar":
                return stacked_bar_chart(
                    data=data,
                    x=params.get('x'),
                    y=params.get('y'),
                    stack=params.get('stack'),
                    normalize=params.get('normalize', False),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (10, 6)),
                    interactive=params.get('interactive', False)
                )
            
            elif chart_type == "grouped_bar":
                return grouped_bar_chart(
                    data=data,
                    x=params.get('x'),
                    y=params.get('y'),
                    group=params.get('group'),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (10, 6)),
                    interactive=params.get('interactive', False)
                )
            
            elif chart_type == "pie":
                return pie_chart(
                    data=data,
                    labels=params.get('labels'),
                    values=params.get('values'),
                    hole=params.get('hole', 0),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (8, 8)),
                    interactive=params.get('interactive', False)
                )
            
            elif chart_type == "histogram":
                return histogram(
                    data=data,
                    var=params.get('var'),
                    bins=params.get('bins', "auto"),
                    kde=params.get('kde', True),
                    color=params.get('color'),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (10, 6)),
                    interactive=params.get('interactive', False)
                )
            
            elif chart_type == "density":
                return density_plot(
                    data=data,
                    var=params.get('var'),
                    group_var=params.get('group_var'),
                    fill=params.get('fill', True),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (10, 6)),
                    interactive=params.get('interactive', False)
                )
            
            elif chart_type == "scatter":
                return scatter_plot(
                    data=data,
                    x=params.get('x'),
                    y=params.get('y'),
                    color=params.get('color'),
                    size=params.get('size'),
                    trend_line=params.get('trend_line'),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (10, 6)),
                    interactive=params.get('interactive', False)
                )
            
            elif chart_type == "line":
                return line_chart(
                    data=data,
                    x=params.get('x'),
                    y=params.get('y'),
                    group=params.get('group'),
                    markers=params.get('markers', True),
                    fill_area=params.get('fill_area', False),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (10, 6)),
                    interactive=params.get('interactive', False)
                )
            
            elif chart_type == "area":
                return area_chart(
                    data=data,
                    x=params.get('x'),
                    y=params.get('y'),
                    stacked=params.get('stacked', True),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (10, 6)),
                    interactive=params.get('interactive', False)
                )
            
            elif chart_type == "box":
                return box_plot(
                    data=data,
                    y=params.get('y'),
                    x=params.get('x'),
                    group=params.get('group'),
                    notch=params.get('notch', False),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (10, 6)),
                    interactive=params.get('interactive', False)
                )
            
            elif chart_type == "violin":
                return violin_plot(
                    data=data,
                    y=params.get('y'),
                    x=params.get('x'),
                    group=params.get('group'),
                    split=params.get('split', False),
                    inner=params.get('inner', "box"),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (10, 6)),
                    interactive=params.get('interactive', False)
                )
            
            elif chart_type == "error_bar":
                return error_bar_chart(
                    data=data,
                    x=params.get('x'),
                    y=params.get('y'),
                    yerr=params.get('yerr'),
                    ci=params.get('ci', 0.95),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (10, 6)),
                    interactive=params.get('interactive', False)
                )
            
            # 高级图表
            elif chart_type == "heatmap":
                return heatmap(
                    data=data,
                    x=params.get('x'),
                    y=params.get('y'),
                    z=params.get('z'),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (10, 8)),
                    interactive=params.get('interactive', False)
                )
            
            elif chart_type == "pair":
                return pair_plot(
                    data=data,
                    vars=params.get('vars'),
                    hue=params.get('hue'),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (10, 10))
                )
            
            elif chart_type == "correlation_matrix":
                return correlation_matrix(
                    data=data,
                    vars=params.get('vars'),
                    method=params.get('method', "pearson"),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (10, 8))
                )
            
            # 统计图表
            elif chart_type == "qq":
                return qq_plot(
                    data=data,
                    var=params.get('var'),
                    distribution=params.get('distribution', "norm"),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (8, 8))
                )
            
            elif chart_type == "residual":
                return residual_plot(
                    data=data,
                    x=params.get('x'),
                    y=params.get('y'),
                    model=params.get('model'),
                    title=params.get('title', ""),
                    figsize=params.get('figsize', (10, 6))
                )
            
            # 交互式图表
            elif chart_type == "interactive_scatter":
                return interactive_scatter(
                    data=data,
                    x=params.get('x'),
                    y=params.get('y'),
                    color=params.get('color'),
                    size=params.get('size'),
                    title=params.get('title', "")
                )
            
            else:
                return {"success": False, "error": f"Unknown chart type: {chart_type}"}
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "chart_type": chart_type,
                "params": params
            }

    def export_chart(self, figure, path: str, format: str) -> dict:
        """导出图表"""
        try:
            # 使用export.exporter模块导出图表
            result = export_chart_file(figure, path, format)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": path,
                "format": format
            }
