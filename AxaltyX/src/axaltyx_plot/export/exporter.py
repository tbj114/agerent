import os
import json
from typing import Any, Dict, Optional, Union

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio

from axaltyx_plot.themes.arco_theme import get_theme

def export_figure(
    figure,  # matplotlib.Figure 或 plotly.Figure
    path: str,
    format: str = "png",
    dpi: int = 300,
    width: float = None,
    height: float = None,
    transparent: bool = False
) -> dict:
    """
    导出图表到指定格式
    
    Args:
        figure: matplotlib.Figure 或 plotly.Figure 对象
        path: 导出路径
        format: 导出格式（png/jpg/svg/pdf/tiff/eps）
        dpi: 分辨率
        width: 宽度（英寸）
        height: 高度（英寸）
        transparent: 是否透明背景
    
    Returns:
        包含导出结果的字典
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        
        # 根据图表类型处理
        if hasattr(figure, 'savefig'):  # matplotlib 图表
            if width and height:
                figure.set_size_inches(width, height)
            figure.savefig(
                path,
                format=format,
                dpi=dpi,
                transparent=transparent,
                bbox_inches='tight'
            )
        elif hasattr(figure, 'write_image'):  # plotly 图表
            figure.write_image(
                path,
                format=format,
                width=width * 100 if width else None,
                height=height * 100 if height else None,
                scale=dpi / 100
            )
        else:
            return {
                "success": False,
                "results": {},
                "warnings": [],
                "error": "Unsupported figure type"
            }
        
        # 获取文件大小
        file_size = os.path.getsize(path)
        
        return {
            "success": True,
            "results": {
                "path": path,
                "format": format,
                "file_size": file_size,
                "dpi": dpi
            },
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }

def export_interactive(
    figure,  # plotly.Figure
    path: str,
    format: str = "html"
) -> dict:
    """
    导出交互式图表
    
    Args:
        figure: plotly.Figure 对象
        path: 导出路径
        format: 导出格式（html/json）
    
    Returns:
        包含导出结果的字典
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        
        if format == "html":
            figure.write_html(path)
        elif format == "json":
            figure.write_json(path)
        else:
            return {
                "success": False,
                "results": {},
                "warnings": [],
                "error": "Unsupported format"
            }
        
        # 获取文件大小
        file_size = os.path.getsize(path)
        
        return {
            "success": True,
            "results": {
                "path": path,
                "format": format,
                "file_size": file_size
            },
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }

def apply_style(
    figure,
    theme: str = "arco",
    custom_params: dict = None
) -> dict:
    """
    应用主题样式到图表
    
    Args:
        figure: matplotlib.Figure 或 plotly.Figure 对象
        theme: 主题（arco/arco_dark/minimal/publication）
        custom_params: 自定义样式参数
    
    Returns:
        包含应用结果的字典
    """
    try:
        # 获取主题配置
        theme_config = get_theme(theme)
        
        # 应用自定义参数
        if custom_params:
            theme_config.update(custom_params)
        
        # 根据图表类型处理
        if hasattr(figure, 'gca'):  # matplotlib 图表
            ax = figure.gca()
            
            # 应用背景色
            if 'facecolor' in theme_config:
                figure.set_facecolor(theme_config['facecolor'])
                ax.set_facecolor(theme_config['facecolor'])
            
            # 应用轴线样式
            if 'axes.edgecolor' in theme_config:
                ax.spines['top'].set_color(theme_config['axes.edgecolor'])
                ax.spines['right'].set_color(theme_config['axes.edgecolor'])
                ax.spines['left'].set_color(theme_config['axes.edgecolor'])
                ax.spines['bottom'].set_color(theme_config['axes.edgecolor'])
            
            # 应用刻度样式
            if 'xtick.color' in theme_config:
                ax.tick_params(axis='x', colors=theme_config['xtick.color'])
            if 'ytick.color' in theme_config:
                ax.tick_params(axis='y', colors=theme_config['ytick.color'])
            
            # 应用标签样式
            if 'axes.labelcolor' in theme_config:
                ax.xaxis.label.set_color(theme_config['axes.labelcolor'])
                ax.yaxis.label.set_color(theme_config['axes.labelcolor'])
            
            # 应用标题样式
            if 'axes.titlecolor' in theme_config:
                ax.title.set_color(theme_config['axes.titlecolor'])
        
        elif hasattr(figure, 'update_layout'):  # plotly 图表
            # 应用布局样式
            layout_update = {}
            if 'facecolor' in theme_config:
                layout_update['paper_bgcolor'] = theme_config['facecolor']
                layout_update['plot_bgcolor'] = theme_config['facecolor']
            if 'axes.labelcolor' in theme_config:
                layout_update['font'] = {'color': theme_config['axes.labelcolor']}
            if 'axes.edgecolor' in theme_config:
                layout_update['xaxis'] = {'gridcolor': theme_config['axes.edgecolor']}
                layout_update['yaxis'] = {'gridcolor': theme_config['axes.edgecolor']}
            
            figure.update_layout(**layout_update)
        
        return {
            "success": True,
            "results": {
                "figure": figure,
                "applied_theme": theme,
                "applied_params": theme_config
            },
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }

def add_annotation(
    figure,
    x: float,
    y: float,
    text: str,
    arrow: bool = False,
    fontsize: int = 12,
    color: str = None
) -> dict:
    """
    向图表添加标注
    
    Args:
        figure: matplotlib.Figure 或 plotly.Figure 对象
        x: x 坐标
        y: y 坐标
        text: 标注文本
        arrow: 是否添加箭头
        fontsize: 字体大小
        color: 文本颜色
    
    Returns:
        包含添加结果的字典
    """
    try:
        annotation_id = None
        
        # 根据图表类型处理
        if hasattr(figure, 'gca'):  # matplotlib 图表
            ax = figure.gca()
            
            # 添加标注
            kwargs = {
                'xy': (x, y),
                'text': text,
                'fontsize': fontsize
            }
            
            if color:
                kwargs['color'] = color
            
            if arrow:
                kwargs['arrowprops'] = {'arrowstyle': '->'}
            
            ax.annotate(**kwargs)
            annotation_id = id(kwargs)
        
        elif hasattr(figure, 'add_annotation'):  # plotly 图表
            # 添加标注
            kwargs = {
                'x': x,
                'y': y,
                'text': text,
                'font': {'size': fontsize}
            }
            
            if color:
                kwargs['font']['color'] = color
            
            if arrow:
                kwargs['showarrow'] = True
            
            figure.add_annotation(**kwargs)
            annotation_id = len(figure.layout.annotations) - 1
        
        return {
            "success": True,
            "results": {
                "figure": figure,
                "annotation_id": annotation_id
            },
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }

def set_chart_title(
    figure,
    title: str,
    subtitle: str = "",
    fontsize: int = 16,
    color: str = None
) -> dict:
    """
    设置图表标题
    
    Args:
        figure: matplotlib.Figure 或 plotly.Figure 对象
        title: 主标题
        subtitle: 副标题
        fontsize: 字体大小
        color: 文本颜色
    
    Returns:
        包含设置结果的字典
    """
    try:
        # 根据图表类型处理
        if hasattr(figure, 'gca'):  # matplotlib 图表
            ax = figure.gca()
            
            # 设置主标题
            ax.set_title(title, fontsize=fontsize, color=color)
            
            # 设置副标题（如果有）
            if subtitle:
                ax.text(
                    0.5, 0.95,
                    subtitle,
                    ha='center',
                    va='top',
                    transform=ax.transAxes,
                    fontsize=fontsize * 0.8,
                    color=color
                )
        
        elif hasattr(figure, 'update_layout'):  # plotly 图表
            # 设置标题
            title_text = title
            if subtitle:
                title_text += f'<br><span style="font-size: {fontsize * 0.8}px">{subtitle}</span>'
            
            layout_update = {
                'title': {
                    'text': title_text,
                    'font': {'size': fontsize}
                }
            }
            
            if color:
                layout_update['title']['font']['color'] = color
            
            figure.update_layout(**layout_update)
        
        return {
            "success": True,
            "results": {
                "figure": figure
            },
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }
