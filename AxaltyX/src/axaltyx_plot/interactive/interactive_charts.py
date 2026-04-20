import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from sklearn.metrics import roc_curve, auc
from axaltyx_plot.themes.arco_theme import ARCO_COLORS


def dynamic_line_chart(
    data: pd.DataFrame,
    x: str,
    y: list[str],
    title: str = "",
    width: int = 900,
    height: int = 500
) -> dict:
    """动态折线图"""
    try:
        fig = px.line(
            data, x=x, y=y,
            title=title,
            color_discrete_sequence=ARCO_COLORS,
            width=width,
            height=height
        )
        
        # 添加动画效果
        fig.update_layout(
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [{
                    'label': 'Play',
                    'method': 'animate',
                    'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True}]
                }, {
                    'label': 'Pause',
                    'method': 'animate',
                    'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}]
                }]
            }]
        )
        
        # 计算动画帧数
        animation_frames = len(data[x].unique())
        
        # 保存为HTML
        html_path = f"dynamic_line_chart.html"
        fig.write_html(html_path)
        
        return {
            "success": True,
            "results": {
                "html_path": html_path,
                "figure": fig,
                "animation_frames": animation_frames,
                "type": "dynamic_line_chart",
                "backend": "plotly",
                "metadata": {"x": x, "y": y, "width": width, "height": height}
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


def interactive_scatter(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str = None,
    size: str = None,
    tooltip_vars: list[str] = None,
    title: str = "",
    width: int = 900,
    height: int = 500
) -> dict:
    """交互式散点图"""
    try:
        fig = px.scatter(
            data, x=x, y=y, color=color, size=size,
            title=title,
            color_discrete_sequence=ARCO_COLORS,
            hover_data=tooltip_vars,
            width=width,
            height=height
        )
        
        # 添加交互功能
        fig.update_layout(
            hovermode='closest',
            clickmode='event+select'
        )
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "interactive_scatter",
                "backend": "plotly",
                "metadata": {"x": x, "y": y, "color": color, "size": size, "tooltip_vars": tooltip_vars}
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


def interactive_boxplot(
    data: pd.DataFrame,
    y: str,
    x: str = None,
    points: str = "outliers",
    title: str = "",
    width: int = 900,
    height: int = 500
) -> dict:
    """交互式箱线图"""
    try:
        fig = px.box(
            data, x=x, y=y,
            points=points,
            title=title,
            color_discrete_sequence=ARCO_COLORS,
            width=width,
            height=height
        )
        
        # 添加交互功能
        fig.update_layout(
            hovermode='x unified',
            boxmode='group' if x else 'overlay'
        )
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "interactive_boxplot",
                "backend": "plotly",
                "metadata": {"y": y, "x": x, "points": points}
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


def dynamic_time_series(
    data: pd.DataFrame,
    time_var: str,
    value_vars: list[str],
    title: str = "",
    width: int = 1000,
    height: int = 500
) -> dict:
    """动态时间序列图"""
    try:
        # 确保时间变量是 datetime 类型
        if not pd.api.types.is_datetime64_any_dtype(data[time_var]):
            data[time_var] = pd.to_datetime(data[time_var])
        
        fig = px.line(
            data, x=time_var, y=value_vars,
            title=title,
            color_discrete_sequence=ARCO_COLORS,
            width=width,
            height=height
        )
        
        # 添加时间滑块
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "dynamic_time_series",
                "backend": "plotly",
                "metadata": {"time_var": time_var, "value_vars": value_vars}
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


def dynamic_roc_curve(
    y_true: np.ndarray,
    y_scores: np.ndarray,
    title: str = "",
    width: int = 800,
    height: int = 600
) -> dict:
    """动态ROC曲线"""
    try:
        # 计算ROC曲线
        fpr, tpr, thresholds = roc_curve(y_true, y_scores)
        roc_auc = auc(fpr, tpr)
        
        # 创建交互式ROC曲线
        fig = go.Figure()
        
        # 添加ROC曲线
        fig.add_trace(go.Scatter(
            x=fpr, y=tpr,
            mode='lines',
            name=f'ROC curve (AUC = {roc_auc:.3f})',
            line=dict(color=ARCO_COLORS[0], width=2)
        ))
        
        # 添加对角线
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1],
            mode='lines',
            name='Random chance',
            line=dict(color='gray', width=1, dash='dash')
        ))
        
        # 添加阈值点
        for i, threshold in enumerate(thresholds[::len(thresholds)//10]):
            fig.add_trace(go.Scatter(
                x=[fpr[i*len(thresholds)//10]], y=[tpr[i*len(thresholds)//10]],
                mode='markers',
                name=f'Threshold: {threshold:.3f}',
                marker=dict(color=ARCO_COLORS[1], size=6, opacity=0.6)
            ))
        
        # 设置布局
        fig.update_layout(
            title=title or "Dynamic ROC Curve",
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate",
            width=width,
            height=height,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "dynamic_roc_curve",
                "backend": "plotly",
                "metadata": {"n_samples": len(y_true), "auc": float(roc_auc)}
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


def correlation_network(
    correlation_matrix: pd.DataFrame,
    threshold: float = 0.3,
    title: str = "",
    width: int = 900,
    height: int = 700
) -> dict:
    """相关性网络图"""
    try:
        # 提取相关性高于阈值的边
        edges = []
        for i, row in correlation_matrix.iterrows():
            for j, col in enumerate(row):
                if i < j and abs(col) >= threshold:
                    edges.append({
                        'source': i,
                        'target': j,
                        'value': abs(col)
                    })
        
        # 创建节点列表
        nodes = [{'id': i, 'label': col} for i, col in enumerate(correlation_matrix.columns)]
        
        # 创建网络图
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=[node['label'] for node in nodes]
            ),
            link=dict(
                source=[edge['source'] for edge in edges],
                target=[edge['target'] for edge in edges],
                value=[edge['value'] * 10 for edge in edges],  # 放大值以便更好地显示
                color=[ARCO_COLORS[i % len(ARCO_COLORS)] for i in range(len(edges))]
            )
        )])
        
        fig.update_layout(
            title=title or "Correlation Network",
            width=width,
            height=height
        )
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "correlation_network",
                "backend": "plotly",
                "metadata": {"threshold": threshold, "n_nodes": len(nodes), "n_edges": len(edges)}
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


def sankey_diagram(
    data: pd.DataFrame,
    source: str,
    target: str,
    value: str,
    title: str = "",
    width: int = 900,
    height: int = 600
) -> dict:
    """桑基图"""
    try:
        # 创建节点映射
        all_nodes = list(data[source].unique()) + list(data[target].unique())
        node_dict = {node: i for i, node in enumerate(all_nodes)}
        
        # 准备数据
        sources = data[source].map(node_dict)
        targets = data[target].map(node_dict)
        values = data[value]
        
        # 创建桑基图
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=all_nodes
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=[ARCO_COLORS[i % len(ARCO_COLORS)] for i in range(len(data))]
            )
        )])
        
        fig.update_layout(
            title=title or "Sankey Diagram",
            width=width,
            height=height
        )
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "sankey_diagram",
                "backend": "plotly",
                "metadata": {"source": source, "target": target, "value": value, "n_nodes": len(all_nodes), "n_edges": len(data)}
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


def chord_diagram(
    matrix: Union[np.ndarray, pd.DataFrame],
    labels: list[str] = None,
    title: str = "",
    width: int = 800,
    height: int = 800
) -> dict:
    """弦图"""
    try:
        # 转换为数组
        if isinstance(matrix, pd.DataFrame):
            labels = matrix.columns.tolist() if labels is None else labels
            matrix = matrix.values
        
        # 提取边
        edges = []
        n = matrix.shape[0]
        for i in range(n):
            for j in range(n):
                if i != j and matrix[i, j] > 0:
                    edges.append({
                        'source': i,
                        'target': j,
                        'value': matrix[i, j]
                    })
        
        # 创建节点
        if labels is None:
            labels = [f'Node {i}' for i in range(n)]
        
        # 创建弦图
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels
            ),
            link=dict(
                source=[edge['source'] for edge in edges],
                target=[edge['target'] for edge in edges],
                value=[edge['value'] for edge in edges],
                color=[ARCO_COLORS[i % len(ARCO_COLORS)] for i in range(len(edges))]
            )
        )])
        
        fig.update_layout(
            title=title or "Chord Diagram",
            width=width,
            height=height
        )
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "chord_diagram",
                "backend": "plotly",
                "metadata": {"n_nodes": n, "n_edges": len(edges)}
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


def sunburst_chart(
    data: pd.DataFrame,
    path: list[str],
    values: str,
    title: str = "",
    width: int = 800,
    height: int = 600
) -> dict:
    """旭日图"""
    try:
        fig = px.sunburst(
            data, path=path, values=values,
            title=title,
            color_discrete_sequence=ARCO_COLORS,
            width=width,
            height=height
        )
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "sunburst_chart",
                "backend": "plotly",
                "metadata": {"path": path, "values": values}
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


def treemap(
    data: pd.DataFrame,
    names: str,
    values: str,
    parents: str = None,
    title: str = "",
    width: int = 900,
    height: int = 600
) -> dict:
    """树状图"""
    try:
        fig = px.treemap(
            data, names=names, values=values, parents=parents,
            title=title,
            color_discrete_sequence=ARCO_COLORS,
            width=width,
            height=height
        )
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "treemap",
                "backend": "plotly",
                "metadata": {"names": names, "values": values, "parents": parents}
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


def heatmap_cluster(
    data: pd.DataFrame,
    cluster_rows: bool = True,
    cluster_cols: bool = True,
    title: str = "",
    width: int = 900,
    height: int = 700
) -> dict:
    """聚类热力图"""
    try:
        fig = px.imshow(
            data,
            title=title,
            color_continuous_scale='Blues',
            width=width,
            height=height
        )
        
        # 添加交互功能
        fig.update_layout(
            hovermode='closest',
            xaxis_title='Columns',
            yaxis_title='Rows'
        )
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "heatmap_cluster",
                "backend": "plotly",
                "metadata": {"cluster_rows": cluster_rows, "cluster_cols": cluster_cols, "shape": data.shape}
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
