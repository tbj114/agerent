import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from axaltyx_plot.themes.arco_theme import apply_theme, ARCO_COLORS

def bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str = None,
    color: str = None,
    orientation: str = "vertical",
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    figsize: tuple = (10, 6),
    style: str = "arco",
    interactive: bool = False
) -> dict:
    try:
        if interactive:
            if y is None:
                # 计数模式
                fig = px.bar(
                    data, 
                    x=x, 
                    color=color,
                    title=title,
                    orientation=orientation,
                    color_discrete_sequence=ARCO_COLORS
                )
            else:
                fig = px.bar(
                    data, 
                    x=x, 
                    y=y, 
                    color=color,
                    title=title,
                    orientation=orientation,
                    color_discrete_sequence=ARCO_COLORS
                )
            fig.update_layout(
                xaxis_title=xlabel if xlabel else x,
                yaxis_title=ylabel if ylabel else y if y else "Count"
            )
            backend = "plotly"
        else:
            apply_theme(style)
            fig, ax = plt.subplots(figsize=figsize)
            
            if y is None:
                # 计数模式
                if color:
                    # 按颜色分组计数
                    grouped = data.groupby([x, color]).size().reset_index(name='count')
                    for i, (name, group) in enumerate(grouped.groupby(color)):
                        if orientation == "vertical":
                            ax.bar(group[x], group['count'], label=name, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                        else:
                            ax.barh(group[x], group['count'], label=name, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                    ax.legend()
                else:
                    # 简单计数
                    counts = data[x].value_counts().sort_index()
                    if orientation == "vertical":
                        ax.bar(counts.index, counts.values, color=ARCO_COLORS[0])
                    else:
                        ax.barh(counts.index, counts.values, color=ARCO_COLORS[0])
                ylabel = ylabel if ylabel else "Count"
            else:
                if color:
                    # 按颜色分组
                    for i, (name, group) in enumerate(data.groupby(color)):
                        if orientation == "vertical":
                            ax.bar(group[x], group[y], label=name, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                        else:
                            ax.barh(group[x], group[y], label=name, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                    ax.legend()
                else:
                    if orientation == "vertical":
                        ax.bar(data[x], data[y], color=ARCO_COLORS[0])
                    else:
                        ax.barh(data[x], data[y], color=ARCO_COLORS[0])
                ylabel = ylabel if ylabel else y
            
            ax.set_title(title)
            ax.set_xlabel(xlabel if xlabel else x)
            ax.set_ylabel(ylabel)
            plt.tight_layout()
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "bar_chart",
                "backend": backend,
                "metadata": {
                    "x": x,
                    "y": y,
                    "n_bars": len(data[x].unique()),
                    "color_groups": data[color].nunique() if color else 1
                }
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

def stacked_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    stack: str,
    normalize: bool = False,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict:
    try:
        if interactive:
            fig = px.bar(
                data, 
                x=x, 
                y=y, 
                color=stack,
                title=title,
                barmode="stack",
                color_discrete_sequence=ARCO_COLORS
            )
            if normalize:
                fig.update_layout(
                    yaxis_title="Percentage",
                    yaxis_tickformat=".0%"
                )
            backend = "plotly"
        else:
            apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            # 准备数据
            pivot_data = data.pivot_table(
                index=x, 
                columns=stack, 
                values=y, 
                aggfunc='sum'
            )
            
            if normalize:
                pivot_data = pivot_data.div(pivot_data.sum(axis=1), axis=0)
                ylabel = "Percentage"
            else:
                ylabel = y
            
            # 绘制堆叠条形图
            pivot_data.plot(kind='bar', stacked=True, ax=ax, color=ARCO_COLORS[:len(pivot_data.columns)])
            
            ax.set_title(title)
            ax.set_xlabel(x)
            ax.set_ylabel(ylabel)
            ax.legend(title=stack)
            plt.tight_layout()
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "stacked_bar_chart",
                "backend": backend,
                "metadata": {
                    "x": x,
                    "y": y,
                    "stack": stack,
                    "normalize": normalize
                }
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

def grouped_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    group: str,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict:
    try:
        if interactive:
            fig = px.bar(
                data, 
                x=x, 
                y=y, 
                color=group,
                title=title,
                barmode="group",
                color_discrete_sequence=ARCO_COLORS
            )
            backend = "plotly"
        else:
            apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            # 准备数据
            pivot_data = data.pivot_table(
                index=x, 
                columns=group, 
                values=y, 
                aggfunc='mean'
            )
            
            # 绘制分组条形图
            pivot_data.plot(kind='bar', ax=ax, color=ARCO_COLORS[:len(pivot_data.columns)])
            
            ax.set_title(title)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.legend(title=group)
            plt.tight_layout()
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "grouped_bar_chart",
                "backend": backend,
                "metadata": {
                    "x": x,
                    "y": y,
                    "group": group
                }
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

def pie_chart(
    data: pd.DataFrame,
    labels: str,
    values: str,
    hole: float = 0,
    title: str = "",
    figsize: tuple = (8, 8),
    interactive: bool = False
) -> dict:
    try:
        if interactive:
            fig = px.pie(
                data, 
                names=labels, 
                values=values,
                title=title,
                hole=hole,
                color_discrete_sequence=ARCO_COLORS
            )
            backend = "plotly"
        else:
            apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            # 准备数据
            pie_data = data.groupby(labels)[values].sum()
            
            # 绘制饼图
            wedges, texts, autotexts = ax.pie(
                pie_data.values,
                labels=pie_data.index,
                autopct='%1.1f%%',
                startangle=90,
                colors=ARCO_COLORS[:len(pie_data)],
                wedgeprops={'width': 1-hole}
            )
            
            ax.set_title(title)
            ax.axis('equal')  # 确保饼图是圆形
            plt.tight_layout()
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "pie_chart",
                "backend": backend,
                "metadata": {
                    "labels": labels,
                    "values": values,
                    "hole": hole,
                    "n_segments": len(data[labels].unique())
                }
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

def histogram(
    data: pd.DataFrame,
    var: str,
    bins: Union[int, str] = "auto",
    kde: bool = True,
    color: str = None,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict:
    try:
        if interactive:
            fig = px.histogram(
                data, 
                x=var,
                color=color,
                title=title,
                nbins=bins if isinstance(bins, int) else None,
                histnorm="probability density" if kde else None,
                color_discrete_sequence=ARCO_COLORS
            )
            if kde:
                fig.update_traces(opacity=0.7)
            backend = "plotly"
        else:
            apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            if color:
                # 按颜色分组绘制直方图
                groups = data[color].unique()
                for i, group in enumerate(groups):
                    group_data = data[data[color] == group]
                    ax.hist(
                        group_data[var], 
                        bins=bins, 
                        alpha=0.6, 
                        label=group,
                        color=ARCO_COLORS[i % len(ARCO_COLORS)],
                        density=kde
                    )
                ax.legend(title=color)
            else:
                ax.hist(
                    data[var], 
                    bins=bins, 
                    alpha=0.7, 
                    color=ARCO_COLORS[0],
                    density=kde
                )
            
            if kde:
                from scipy.stats import gaussian_kde
                if color:
                    for i, group in enumerate(groups):
                        group_data = data[data[color] == group]
                        kde = gaussian_kde(group_data[var])
                        x = np.linspace(data[var].min(), data[var].max(), 100)
                        ax.plot(x, kde(x), linewidth=2, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                else:
                    kde = gaussian_kde(data[var])
                    x = np.linspace(data[var].min(), data[var].max(), 100)
                    ax.plot(x, kde(x), linewidth=2, color=ARCO_COLORS[1])
            
            ax.set_title(title)
            ax.set_xlabel(var)
            ax.set_ylabel("Density" if kde else "Frequency")
            plt.tight_layout()
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "histogram",
                "backend": backend,
                "metadata": {
                    "var": var,
                    "bins": bins,
                    "kde": kde,
                    "color": color
                }
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

def density_plot(
    data: pd.DataFrame,
    var: str,
    group_var: str = None,
    fill: bool = True,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict:
    try:
        if interactive:
            fig = px.density_contour(
                data, 
                x=var,
                color=group_var,
                title=title,
                color_discrete_sequence=ARCO_COLORS
            )
            backend = "plotly"
        else:
            apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            if group_var:
                # 按组绘制密度图
                groups = data[group_var].unique()
                for i, group in enumerate(groups):
                    group_data = data[data[group_var] == group]
                    from scipy.stats import gaussian_kde
                    kde = gaussian_kde(group_data[var])
                    x = np.linspace(data[var].min(), data[var].max(), 100)
                    y = kde(x)
                    if fill:
                        ax.fill_between(x, y, alpha=0.3, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                    ax.plot(x, y, linewidth=2, label=group, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                ax.legend(title=group_var)
            else:
                # 绘制单个密度图
                from scipy.stats import gaussian_kde
                kde = gaussian_kde(data[var])
                x = np.linspace(data[var].min(), data[var].max(), 100)
                y = kde(x)
                if fill:
                    ax.fill_between(x, y, alpha=0.3, color=ARCO_COLORS[0])
                ax.plot(x, y, linewidth=2, color=ARCO_COLORS[0])
            
            ax.set_title(title)
            ax.set_xlabel(var)
            ax.set_ylabel("Density")
            plt.tight_layout()
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "density_plot",
                "backend": backend,
                "metadata": {
                    "var": var,
                    "group_var": group_var,
                    "fill": fill
                }
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

def scatter_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str = None,
    size: str = None,
    trend_line: str = None,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict:
    try:
        if interactive:
            fig = px.scatter(
                data, 
                x=x, 
                y=y,
                color=color,
                size=size,
                title=title,
                color_discrete_sequence=ARCO_COLORS
            )
            if trend_line:
                fig.add_trace(go.Scatter(
                    x=data[x],
                    y=data[y],
                    mode='lines',
                    line=dict(color=ARCO_COLORS[1], dash='dash'),
                    name='Trend Line'
                ))
            backend = "plotly"
        else:
            apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            # 绘制散点图
            scatter_kwargs = {}
            if color:
                # 按颜色分组绘制
                groups = data[color].unique()
                for i, group in enumerate(groups):
                    group_data = data[data[color] == group]
                    scatter_kwargs['color'] = ARCO_COLORS[i % len(ARCO_COLORS)]
                    scatter_kwargs['label'] = group
                    if size:
                        scatter_kwargs['s'] = group_data[size]
                    ax.scatter(group_data[x], group_data[y], **scatter_kwargs)
                ax.legend(title=color)
            else:
                scatter_kwargs['color'] = ARCO_COLORS[0]
                if size:
                    scatter_kwargs['s'] = data[size]
                ax.scatter(data[x], data[y], **scatter_kwargs)
            
            # 添加趋势线
            if trend_line:
                from scipy.stats import linregress
                slope, intercept, r_value, p_value, std_err = linregress(data[x], data[y])
                x_range = np.linspace(data[x].min(), data[x].max(), 100)
                y_range = slope * x_range + intercept
                ax.plot(x_range, y_range, color=ARCO_COLORS[1], linestyle='--', linewidth=2)
            
            ax.set_title(title)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            plt.tight_layout()
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "scatter_plot",
                "backend": backend,
                "metadata": {
                    "x": x,
                    "y": y,
                    "color": color,
                    "size": size,
                    "trend_line": trend_line
                }
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

def line_chart(
    data: pd.DataFrame,
    x: str,
    y: Union[str, List[str]],
    group: str = None,
    markers: bool = True,
    fill_area: bool = False,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict:
    try:
        if interactive:
            if isinstance(y, list):
                fig = px.line(
                    data, 
                    x=x, 
                    y=y,
                    title=title,
                    markers=markers,
                    color_discrete_sequence=ARCO_COLORS
                )
            else:
                fig = px.line(
                    data, 
                    x=x, 
                    y=y,
                    color=group,
                    title=title,
                    markers=markers,
                    color_discrete_sequence=ARCO_COLORS
                )
            if fill_area:
                fig.update_traces(fill='tozeroy', opacity=0.3)
            backend = "plotly"
        else:
            apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            if isinstance(y, list):
                # 多y变量
                for i, y_var in enumerate(y):
                    ax.plot(data[x], data[y_var], 
                            marker='o' if markers else '',
                            linewidth=2,
                            color=ARCO_COLORS[i % len(ARCO_COLORS)],
                            label=y_var)
                ax.legend()
            else:
                if group:
                    # 按组绘制
                    groups = data[group].unique()
                    for i, group_name in enumerate(groups):
                        group_data = data[data[group] == group_name]
                        ax.plot(group_data[x], group_data[y],
                                marker='o' if markers else '',
                                linewidth=2,
                                color=ARCO_COLORS[i % len(ARCO_COLORS)],
                                label=group_name)
                    ax.legend(title=group)
                else:
                    # 单条线
                    ax.plot(data[x], data[y],
                            marker='o' if markers else '',
                            linewidth=2,
                            color=ARCO_COLORS[0])
            
            if fill_area and isinstance(y, str):
                ax.fill_between(data[x], data[y], alpha=0.3, color=ARCO_COLORS[0])
            
            ax.set_title(title)
            ax.set_xlabel(x)
            ax.set_ylabel(y if isinstance(y, str) else "Value")
            plt.tight_layout()
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "line_chart",
                "backend": backend,
                "metadata": {
                    "x": x,
                    "y": y,
                    "group": group,
                    "markers": markers,
                    "fill_area": fill_area
                }
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

def area_chart(
    data: pd.DataFrame,
    x: str,
    y: Union[str, List[str]],
    stacked: bool = True,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict:
    try:
        if interactive:
            if isinstance(y, list):
                fig = px.area(
                    data, 
                    x=x, 
                    y=y,
                    title=title,
                    color_discrete_sequence=ARCO_COLORS
                )
            else:
                fig = px.area(
                    data, 
                    x=x, 
                    y=y,
                    color=group if 'group' in locals() else None,
                    title=title,
                    color_discrete_sequence=ARCO_COLORS
                )
            backend = "plotly"
        else:
            apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            if isinstance(y, list):
                # 多y变量
                if stacked:
                    # 堆叠面积图
                    ax.stackplot(data[x], 
                                [data[y_var] for y_var in y],
                                labels=y,
                                colors=ARCO_COLORS[:len(y)])
                else:
                    # 非堆叠面积图
                    for i, y_var in enumerate(y):
                        ax.fill_between(data[x], data[y_var], alpha=0.5,
                                       color=ARCO_COLORS[i % len(ARCO_COLORS)],
                                       label=y_var)
                ax.legend()
            else:
                # 单y变量
                ax.fill_between(data[x], data[y], alpha=0.5, color=ARCO_COLORS[0])
            
            ax.set_title(title)
            ax.set_xlabel(x)
            ax.set_ylabel(y if isinstance(y, str) else "Value")
            plt.tight_layout()
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "area_chart",
                "backend": backend,
                "metadata": {
                    "x": x,
                    "y": y,
                    "stacked": stacked
                }
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

def box_plot(
    data: pd.DataFrame,
    y: str,
    x: str = None,
    group: str = None,
    notch: bool = False,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict:
    try:
        if interactive:
            fig = px.box(
                data, 
                x=x, 
                y=y,
                color=group,
                title=title,
                color_discrete_sequence=ARCO_COLORS
            )
            backend = "plotly"
        else:
            apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            if x:
                if group:
                    # 分组箱线图
                    data.boxplot(column=y, by=[x, group], ax=ax, notch=notch)
                else:
                    # 按x分组箱线图
                    data.boxplot(column=y, by=x, ax=ax, notch=notch)
            else:
                # 单个箱线图
                data.boxplot(column=y, ax=ax, notch=notch)
            
            ax.set_title(title)
            ax.set_xlabel(x if x else "")
            ax.set_ylabel(y)
            plt.tight_layout()
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "box_plot",
                "backend": backend,
                "metadata": {
                    "x": x,
                    "y": y,
                    "group": group,
                    "notch": notch
                }
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

def violin_plot(
    data: pd.DataFrame,
    y: str,
    x: str = None,
    group: str = None,
    split: bool = False,
    inner: str = "box",
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict:
    try:
        if interactive:
            fig = px.violin(
                data, 
                x=x, 
                y=y,
                color=group,
                split=split,
                box=inner == "box",
                points="all" if inner == "points" else None,
                title=title,
                color_discrete_sequence=ARCO_COLORS
            )
            backend = "plotly"
        else:
            apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            if x:
                # 按x分组小提琴图
                import seaborn as sns
                sns.violinplot(
                    x=x, y=y, data=data, hue=group, split=split,
                    inner=inner, ax=ax, palette=ARCO_COLORS
                )
            else:
                # 单个小提琴图
                import seaborn as sns
                sns.violinplot(
                    y=y, data=data,
                    inner=inner, ax=ax, palette=ARCO_COLORS
                )
            
            ax.set_title(title)
            ax.set_xlabel(x if x else "")
            ax.set_ylabel(y)
            plt.tight_layout()
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "violin_plot",
                "backend": backend,
                "metadata": {
                    "x": x,
                    "y": y,
                    "group": group,
                    "split": split,
                    "inner": inner
                }
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

def error_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    yerr: Union[str, List] = None,
    ci: float = 0.95,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict:
    try:
        if interactive:
            if yerr:
                fig = px.bar(
                    data, 
                    x=x, 
                    y=y,
                    error_y=yerr,
                    title=title,
                    color_discrete_sequence=ARCO_COLORS
                )
            else:
                # 计算置信区间
                mean_data = data.groupby(x)[y].agg(['mean', 'std', 'count']).reset_index()
                mean_data['se'] = mean_data['std'] / np.sqrt(mean_data['count'])
                from scipy.stats import t
                mean_data['ci'] = mean_data['se'] * t.ppf((1 + ci) / 2, mean_data['count'] - 1)
                
                fig = px.bar(
                    mean_data, 
                    x=x, 
                    y='mean',
                    error_y='ci',
                    title=title,
                    color_discrete_sequence=ARCO_COLORS
                )
            backend = "plotly"
        else:
            apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            if yerr:
                if isinstance(yerr, str):
                    ax.errorbar(data[x], data[y], yerr=data[yerr], 
                               fmt='o', color=ARCO_COLORS[0], capsize=5)
                else:
                    ax.errorbar(data[x], data[y], yerr=yerr, 
                               fmt='o', color=ARCO_COLORS[0], capsize=5)
            else:
                # 计算置信区间
                mean_data = data.groupby(x)[y].agg(['mean', 'std', 'count']).reset_index()
                mean_data['se'] = mean_data['std'] / np.sqrt(mean_data['count'])
                from scipy.stats import t
                mean_data['ci'] = mean_data['se'] * t.ppf((1 + ci) / 2, mean_data['count'] - 1)
                
                ax.errorbar(mean_data[x], mean_data['mean'], yerr=mean_data['ci'], 
                           fmt='o', color=ARCO_COLORS[0], capsize=5)
            
            ax.set_title(title)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            plt.tight_layout()
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "error_bar_chart",
                "backend": backend,
                "metadata": {
                    "x": x,
                    "y": y,
                    "yerr": yerr,
                    "ci": ci
                }
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
