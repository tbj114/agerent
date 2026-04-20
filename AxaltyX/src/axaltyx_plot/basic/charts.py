import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from axaltyx_plot.themes.arco_theme import (
    ARCO_COLORS, get_arco_theme, get_arco_dark_theme, get_minimal_theme
)


def _apply_theme(style: str):
    """应用主题"""
    if style == "arco":
        plt.style.use(get_arco_theme())
    elif style == "arco_dark":
        plt.style.use(get_arco_dark_theme())
    elif style == "minimal":
        plt.style.use(get_minimal_theme())


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
    """柱状图"""
    try:
        if interactive:
            # 使用plotly
            if y is None:
                # 计数图
                fig = px.bar(
                    data, x=x, color=color,
                    orientation=orientation,
                    title=title,
                    color_discrete_sequence=ARCO_COLORS
                )
            else:
                # 数值图
                fig = px.bar(
                    data, x=x, y=y, color=color,
                    orientation=orientation,
                    title=title,
                    color_discrete_sequence=ARCO_COLORS
                )
            
            if xlabel:
                fig.update_xaxes(title=xlabel)
            if ylabel:
                fig.update_yaxes(title=ylabel)
            
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme(style)
            fig, ax = plt.subplots(figsize=figsize)
            
            if y is None:
                # 计数图
                if color:
                    grouped = data.groupby([x, color]).size().reset_index(name='count')
                    for i, (group, group_data) in enumerate(grouped.groupby(color)):
                        if orientation == "vertical":
                            ax.bar(group_data[x], group_data['count'], label=group, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                        else:
                            ax.barh(group_data[x], group_data['count'], label=group, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                    ax.legend()
                else:
                    counts = data[x].value_counts().sort_index()
                    if orientation == "vertical":
                        ax.bar(counts.index, counts.values, color=ARCO_COLORS[0])
                    else:
                        ax.barh(counts.index, counts.values, color=ARCO_COLORS[0])
            else:
                # 数值图
                if color:
                    grouped = data.groupby([x, color])[y].sum().reset_index()
                    for i, (group, group_data) in enumerate(grouped.groupby(color)):
                        if orientation == "vertical":
                            ax.bar(group_data[x], group_data[y], label=group, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                        else:
                            ax.barh(group_data[x], group_data[y], label=group, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                    ax.legend()
                else:
                    if orientation == "vertical":
                        ax.bar(data[x], data[y], color=ARCO_COLORS[0])
                    else:
                        ax.barh(data[x], data[y], color=ARCO_COLORS[0])
            
            ax.set_title(title)
            ax.set_xlabel(xlabel if xlabel else x)
            ax.set_ylabel(ylabel if ylabel else (y if y else "Count"))
            backend = "matplotlib"
        
        # 计算元数据
        n_bars = len(data[x].unique())
        color_groups = len(data[color].unique()) if color else 1
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "bar_chart",
                "backend": backend,
                "metadata": {"x": x, "y": y, "n_bars": n_bars, "color_groups": color_groups}
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
    """堆叠柱状图"""
    try:
        if interactive:
            # 使用plotly
            fig = px.bar(
                data, x=x, y=y, color=stack,
                title=title,
                color_discrete_sequence=ARCO_COLORS,
                barmode="stack"
            )
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            # 准备数据
            pivot_data = data.pivot_table(index=x, columns=stack, values=y, aggfunc='sum')
            
            if normalize:
                pivot_data = pivot_data.div(pivot_data.sum(axis=1), axis=0)
            
            pivot_data.plot(kind='bar', stacked=True, ax=ax, color=ARCO_COLORS[:len(pivot_data.columns)])
            ax.set_title(title)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.legend(title=stack)
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "stacked_bar_chart",
                "backend": backend,
                "metadata": {"x": x, "y": y, "stack": stack, "normalize": normalize}
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
    """分组柱状图"""
    try:
        if interactive:
            # 使用plotly
            fig = px.bar(
                data, x=x, y=y, color=group,
                title=title,
                color_discrete_sequence=ARCO_COLORS,
                barmode="group"
            )
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            # 准备数据
            pivot_data = data.pivot_table(index=x, columns=group, values=y, aggfunc='sum')
            pivot_data.plot(kind='bar', ax=ax, color=ARCO_COLORS[:len(pivot_data.columns)])
            ax.set_title(title)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.legend(title=group)
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "grouped_bar_chart",
                "backend": backend,
                "metadata": {"x": x, "y": y, "group": group}
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
    """饼图"""
    try:
        if interactive:
            # 使用plotly
            fig = px.pie(
                data, names=labels, values=values,
                title=title,
                color_discrete_sequence=ARCO_COLORS,
                hole=hole
            )
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            ax.pie(data[values], labels=data[labels], autopct='%1.1f%%',
                   colors=ARCO_COLORS[:len(data)], wedgeprops={'edgecolor': 'white'})
            if hole > 0:
                center_circle = plt.Circle((0, 0), hole, color='white')
                fig.gca().add_artist(center_circle)
            ax.set_title(title)
            ax.axis('equal')
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "pie_chart",
                "backend": backend,
                "metadata": {"labels": labels, "values": values, "hole": hole}
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
    """直方图"""
    try:
        if interactive:
            # 使用plotly
            fig = px.histogram(
                data, x=var, color=color,
                title=title,
                color_discrete_sequence=ARCO_COLORS,
                nbins=bins if isinstance(bins, int) else None,
                marginal="rug" if kde else None
            )
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            if color:
                groups = data[color].unique()
                for i, group in enumerate(groups):
                    group_data = data[data[color] == group]
                    ax.hist(group_data[var], bins=bins, alpha=0.6, label=group, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                ax.legend()
            else:
                ax.hist(data[var], bins=bins, color=ARCO_COLORS[0])
            
            if kde:
                try:
                    import seaborn as sns
                    if color:
                        for i, group in enumerate(groups):
                            group_data = data[data[color] == group]
                            sns.kdeplot(group_data[var], ax=ax, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                    else:
                        sns.kdeplot(data[var], ax=ax, color=ARCO_COLORS[0])
                except ImportError:
                    pass
            
            ax.set_title(title)
            ax.set_xlabel(var)
            ax.set_ylabel("Frequency")
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "histogram",
                "backend": backend,
                "metadata": {"var": var, "bins": bins, "kde": kde, "color": color}
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
    """密度图"""
    try:
        if interactive:
            # 使用plotly
            fig = px.density_contour(
                data, x=var,
                color=group_var,
                title=title,
                color_discrete_sequence=ARCO_COLORS,
                fill=fill
            )
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            try:
                import seaborn as sns
                if group_var:
                    sns.kdeplot(data=data, x=var, hue=group_var, fill=fill, ax=ax, palette=ARCO_COLORS)
                else:
                    sns.kdeplot(data=data, x=var, fill=fill, ax=ax, color=ARCO_COLORS[0])
            except ImportError:
                # 回退到matplotlib
                if group_var:
                    groups = data[group_var].unique()
                    for i, group in enumerate(groups):
                        group_data = data[data[group_var] == group]
                        counts, bin_edges = np.histogram(group_data[var], bins=30, density=True)
                        pdf = counts / sum(counts)
                        ax.plot(bin_edges[:-1], pdf, label=group, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                        if fill:
                            ax.fill_between(bin_edges[:-1], pdf, alpha=0.3, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                    ax.legend()
                else:
                    counts, bin_edges = np.histogram(data[var], bins=30, density=True)
                    pdf = counts / sum(counts)
                    ax.plot(bin_edges[:-1], pdf, color=ARCO_COLORS[0])
                    if fill:
                        ax.fill_between(bin_edges[:-1], pdf, alpha=0.3, color=ARCO_COLORS[0])
            
            ax.set_title(title)
            ax.set_xlabel(var)
            ax.set_ylabel("Density")
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "density_plot",
                "backend": backend,
                "metadata": {"var": var, "group_var": group_var, "fill": fill}
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
    """散点图"""
    try:
        if interactive:
            # 使用plotly
            fig = px.scatter(
                data, x=x, y=y, color=color, size=size,
                title=title,
                color_discrete_sequence=ARCO_COLORS,
                trendline=trend_line
            )
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            if color:
                groups = data[color].unique()
                for i, group in enumerate(groups):
                    group_data = data[data[color] == group]
                    scatter_kwargs = {}
                    if size:
                        scatter_kwargs['s'] = group_data[size]
                    ax.scatter(group_data[x], group_data[y], label=group, color=ARCO_COLORS[i % len(ARCO_COLORS)], **scatter_kwargs)
                ax.legend()
            else:
                scatter_kwargs = {}
                if size:
                    scatter_kwargs['s'] = data[size]
                ax.scatter(data[x], data[y], color=ARCO_COLORS[0], **scatter_kwargs)
            
            # 添加趋势线
            if trend_line:
                from sklearn.linear_model import LinearRegression
                from sklearn.preprocessing import PolynomialFeatures
                
                X = data[x].values.reshape(-1, 1)
                Y = data[y].values
                
                if trend_line == "linear":
                    model = LinearRegression()
                    model.fit(X, Y)
                    Y_pred = model.predict(X)
                elif trend_line in ["quadratic", "polynomial"]:
                    poly = PolynomialFeatures(degree=2)
                    X_poly = poly.fit_transform(X)
                    model = LinearRegression()
                    model.fit(X_poly, Y)
                    X_sorted = np.sort(X, axis=0)
                    Y_pred = model.predict(poly.transform(X_sorted))
                    ax.plot(X_sorted, Y_pred, color=ARCO_COLORS[1])
                
                if trend_line == "linear":
                    ax.plot(data[x], Y_pred, color=ARCO_COLORS[1])
            
            ax.set_title(title)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "scatter_plot",
                "backend": backend,
                "metadata": {"x": x, "y": y, "color": color, "size": size, "trend_line": trend_line}
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
    """折线图"""
    try:
        if interactive:
            # 使用plotly
            if isinstance(y, list):
                fig = px.line(
                    data, x=x, y=y,
                    title=title,
                    color_discrete_sequence=ARCO_COLORS,
                    markers=markers
                )
            else:
                fig = px.line(
                    data, x=x, y=y, color=group,
                    title=title,
                    color_discrete_sequence=ARCO_COLORS,
                    markers=markers
                )
            
            if fill_area:
                fig.update_traces(fill="tozeroy")
            
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            if isinstance(y, list):
                for i, y_col in enumerate(y):
                    ax.plot(data[x], data[y_col], label=y_col, color=ARCO_COLORS[i % len(ARCO_COLORS)], marker='o' if markers else None)
                ax.legend()
            elif group:
                groups = data[group].unique()
                for i, group_val in enumerate(groups):
                    group_data = data[data[group] == group_val]
                    ax.plot(group_data[x], group_data[y], label=group_val, color=ARCO_COLORS[i % len(ARCO_COLORS)], marker='o' if markers else None)
                ax.legend()
            else:
                ax.plot(data[x], data[y], color=ARCO_COLORS[0], marker='o' if markers else None)
            
            if fill_area:
                if isinstance(y, list):
                    for i, y_col in enumerate(y):
                        ax.fill_between(data[x], data[y_col], alpha=0.3, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                else:
                    ax.fill_between(data[x], data[y], alpha=0.3, color=ARCO_COLORS[0])
            
            ax.set_title(title)
            ax.set_xlabel(x)
            ax.set_ylabel(y if isinstance(y, str) else "Value")
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "line_chart",
                "backend": backend,
                "metadata": {"x": x, "y": y, "group": group, "markers": markers, "fill_area": fill_area}
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
    """面积图"""
    try:
        if interactive:
            # 使用plotly
            if isinstance(y, list):
                fig = px.area(
                    data, x=x, y=y,
                    title=title,
                    color_discrete_sequence=ARCO_COLORS,
                    facet_col_wrap=1
                )
            else:
                fig = px.area(
                    data, x=x, y=y,
                    title=title,
                    color_discrete_sequence=ARCO_COLORS
                )
            
            if stacked:
                fig.update_layout(barmode="stack")
            
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            if isinstance(y, list):
                if stacked:
                    ax.stackplot(data[x], *[data[col] for col in y], labels=y, colors=ARCO_COLORS[:len(y)])
                else:
                    for i, y_col in enumerate(y):
                        ax.fill_between(data[x], data[y_col], alpha=0.6, label=y_col, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                ax.legend()
            else:
                ax.fill_between(data[x], data[y], alpha=0.6, color=ARCO_COLORS[0])
            
            ax.set_title(title)
            ax.set_xlabel(x)
            ax.set_ylabel(y if isinstance(y, str) else "Value")
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "area_chart",
                "backend": backend,
                "metadata": {"x": x, "y": y, "stacked": stacked}
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
    """箱线图"""
    try:
        if interactive:
            # 使用plotly
            fig = px.box(
                data, x=x, y=y, color=group,
                title=title,
                color_discrete_sequence=ARCO_COLORS,
                notch=notch
            )
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            if x:
                if group:
                    # 分组箱线图
                    groups = data[group].unique()
                    positions = []
                    labels = []
                    for i, group_val in enumerate(groups):
                        group_data = data[data[group] == group_val]
                        box_positions = np.arange(len(group_data[x].unique())) + i * (len(group_data[x].unique()) + 1)
                        positions.extend(box_positions)
                        labels.extend([f"{group_val}_{val}" for val in group_data[x].unique()])
                        ax.boxplot([group_data[group_data[x] == val][y] for val in group_data[x].unique()],
                                  positions=box_positions, notch=notch, patch_artist=True,
                                  boxprops={'facecolor': ARCO_COLORS[i % len(ARCO_COLORS)], 'alpha': 0.7})
                    ax.set_xticks(positions)
                    ax.set_xticklabels(labels, rotation=45)
                else:
                    # 简单箱线图
                    data.boxplot(column=y, by=x, ax=ax, notch=notch, patch_artist=True)
                    for patch in ax.patches:
                        patch.set_facecolor(ARCO_COLORS[0])
            else:
                # 单变量箱线图
                ax.boxplot(data[y], notch=notch, patch_artist=True)
                ax.set_xticklabels([y])
                for patch in ax.patches:
                    patch.set_facecolor(ARCO_COLORS[0])
            
            ax.set_title(title)
            ax.set_ylabel(y)
            if x:
                ax.set_xlabel(x)
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "box_plot",
                "backend": backend,
                "metadata": {"y": y, "x": x, "group": group, "notch": notch}
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
    """小提琴图"""
    try:
        if interactive:
            # 使用plotly
            fig = px.violin(
                data, x=x, y=y, color=group,
                title=title,
                color_discrete_sequence=ARCO_COLORS,
                box=inner == "box",
                points="all" if inner == "points" else None
            )
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            
            try:
                import seaborn as sns
                if x:
                    sns.violinplot(data=data, x=x, y=y, hue=group, split=split, inner=inner, ax=ax, palette=ARCO_COLORS)
                else:
                    sns.violinplot(data=data, y=y, hue=group, split=split, inner=inner, ax=ax, palette=ARCO_COLORS)
            except ImportError:
                # 回退到matplotlib
                if x:
                    groups = data[x].unique()
                    violin_data = [data[data[x] == val][y] for val in groups]
                    ax.violinplot(violin_data, showmedians=True)
                    ax.set_xticks(range(1, len(groups) + 1))
                    ax.set_xticklabels(groups)
                else:
                    ax.violinplot(data[y], showmedians=True)
            
            ax.set_title(title)
            ax.set_ylabel(y)
            if x:
                ax.set_xlabel(x)
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "violin_plot",
                "backend": backend,
                "metadata": {"y": y, "x": x, "group": group, "split": split, "inner": inner}
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
    """误差条图"""
    try:
        # 计算误差
        if yerr is None:
            # 计算置信区间
            grouped = data.groupby(x).agg({y: ['mean', 'std', 'count']}).reset_index()
            grouped.columns = ['x', 'mean', 'std', 'count']
            grouped['se'] = grouped['std'] / np.sqrt(grouped['count'])
            grouped['yerr'] = grouped['se'] * stats.t.ppf((1 + ci) / 2, grouped['count'] - 1)
            
            x_values = grouped['x']
            y_values = grouped['mean']
            error_values = grouped['yerr']
        elif isinstance(yerr, str):
            x_values = data[x]
            y_values = data[y]
            error_values = data[yerr]
        else:
            x_values = data[x]
            y_values = data[y]
            error_values = yerr
        
        if interactive:
            # 使用plotly
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=x_values,
                y=y_values,
                error_y=dict(
                    type="data",
                    array=error_values,
                    visible=True
                ),
                marker_color=ARCO_COLORS[0]
            ))
            fig.update_layout(title=title)
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme("arco")
            fig, ax = plt.subplots(figsize=figsize)
            ax.bar(x_values, y_values, yerr=error_values, color=ARCO_COLORS[0], capsize=5)
            ax.set_title(title)
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "error_bar_chart",
                "backend": backend,
                "metadata": {"x": x, "y": y, "yerr": yerr, "ci": ci}
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

# 导入stats模块
import scipy.stats as stats
