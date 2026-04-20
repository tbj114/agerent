import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy.cluster.hierarchy import dendrogram as scipy_dendrogram
from scipy.spatial.distance import pdist, squareform
from axaltyx_plot.themes.arco_theme import ARCO_COLORS, get_arco_theme, MATPLOTLIB_CMAPS


def _apply_theme():
    """应用主题"""
    plt.style.use(get_arco_theme())


def heatmap(
    data: Union[pd.DataFrame, np.ndarray],
    annotation: bool = True,
    cmap: str = "arco_blue",
    cluster_rows: bool = False,
    cluster_cols: bool = False,
    title: str = "",
    figsize: tuple = (10, 8),
    interactive: bool = False
) -> dict:
    """热力图"""
    try:
        if interactive:
            # 使用plotly
            if isinstance(data, np.ndarray):
                data = pd.DataFrame(data)
            
            fig = px.imshow(
                data,
                title=title,
                color_continuous_scale=MATPLOTLIB_CMAPS.get(cmap, cmap),
                width=figsize[0] * 100,
                height=figsize[1] * 100
            )
            
            if annotation:
                fig.update_traces(text=data.values, texttemplate="%{text}")
            
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme()
            fig, ax = plt.subplots(figsize=figsize)
            
            if isinstance(data, pd.DataFrame):
                im = ax.imshow(data.values, cmap=MATPLOTLIB_CMAPS.get(cmap, cmap))
                ax.set_xticks(np.arange(len(data.columns)))
                ax.set_yticks(np.arange(len(data.index)))
                ax.set_xticklabels(data.columns, rotation=45, ha='right')
                ax.set_yticklabels(data.index)
            else:
                im = ax.imshow(data, cmap=MATPLOTLIB_CMAPS.get(cmap, cmap))
            
            if annotation:
                if isinstance(data, pd.DataFrame):
                    for i in range(len(data.index)):
                        for j in range(len(data.columns)):
                            text = ax.text(j, i, f"{data.iloc[i, j]:.2f}",
                                         ha="center", va="center", color="w" if data.iloc[i, j] > data.values.mean() else "k")
                else:
                    for i in range(data.shape[0]):
                        for j in range(data.shape[1]):
                            text = ax.text(j, i, f"{data[i, j]:.2f}",
                                         ha="center", va="center", color="w" if data[i, j] > data.mean() else "k")
            
            # 添加颜色条
            cbar = ax.figure.colorbar(im, ax=ax)
            
            ax.set_title(title)
            fig.tight_layout()
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "heatmap",
                "backend": backend,
                "metadata": {"annotation": annotation, "cmap": cmap, "cluster_rows": cluster_rows, "cluster_cols": cluster_cols}
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


def matrix_scatter_plot(
    data: pd.DataFrame,
    vars: list[str],
    diagonal: str = "histogram",
    title: str = "",
    figsize: tuple = (10, 10)
) -> dict:
    """矩阵散点图"""
    try:
        _apply_theme()
        
        n = len(vars)
        fig, axes = plt.subplots(n, n, figsize=figsize)
        
        for i in range(n):
            for j in range(n):
                ax = axes[i, j]
                if i == j:
                    # 对角线
                    if diagonal == "histogram":
                        ax.hist(data[vars[i]], color=ARCO_COLORS[0], alpha=0.6)
                    elif diagonal == "kde":
                        try:
                            import seaborn as sns
                            sns.kdeplot(data[vars[i]], ax=ax, color=ARCO_COLORS[0])
                        except ImportError:
                            ax.hist(data[vars[i]], color=ARCO_COLORS[0], alpha=0.6)
                    ax.set_title(vars[i])
                else:
                    # 非对角线
                    ax.scatter(data[vars[j]], data[vars[i]], color=ARCO_COLORS[0], alpha=0.6, s=20)
                    
                # 清理坐标轴
                if i < n - 1:
                    ax.set_xticks([])
                else:
                    ax.set_xlabel(vars[j])
                
                if j > 0:
                    ax.set_yticks([])
                else:
                    ax.set_ylabel(vars[i])
        
        fig.suptitle(title or "Matrix Scatter Plot", fontsize=16)
        fig.tight_layout(rect=[0, 0, 1, 0.96])
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "matrix_scatter_plot",
                "backend": "matplotlib",
                "metadata": {"vars": vars, "diagonal": diagonal, "n_vars": n}
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


def three_d_scatter(
    data: pd.DataFrame,
    x: str,
    y: str,
    z: str,
    color: str = None,
    title: str = "",
    figsize: tuple = (10, 8),
    interactive: bool = True
) -> dict:
    """3D散点图"""
    try:
        if interactive:
            # 使用plotly
            fig = px.scatter_3d(
                data, x=x, y=y, z=z, color=color,
                title=title,
                color_discrete_sequence=ARCO_COLORS,
                width=figsize[0] * 100,
                height=figsize[1] * 100
            )
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme()
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111, projection='3d')
            
            if color:
                groups = data[color].unique()
                for i, group in enumerate(groups):
                    group_data = data[data[color] == group]
                    ax.scatter(group_data[x], group_data[y], group_data[z], label=group, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                ax.legend()
            else:
                ax.scatter(data[x], data[y], data[z], color=ARCO_COLORS[0], alpha=0.6)
            
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_zlabel(z)
            ax.set_title(title)
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "three_d_scatter",
                "backend": backend,
                "metadata": {"x": x, "y": y, "z": z, "color": color}
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


def three_d_surface(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    cmap: str = "arco_gradient",
    title: str = "",
    figsize: tuple = (10, 8),
    interactive: bool = True
) -> dict:
    """3D曲面图"""
    try:
        if interactive:
            # 使用plotly
            fig = go.Figure(data=[go.Surface(
                x=x, y=y, z=z,
                colorscale=MATPLOTLIB_CMAPS.get(cmap, cmap)
            )])
            fig.update_layout(
                title=title,
                width=figsize[0] * 100,
                height=figsize[1] * 100
            )
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme()
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111, projection='3d')
            
            surf = ax.plot_surface(x, y, z, cmap=MATPLOTLIB_CMAPS.get(cmap, cmap), alpha=0.8)
            fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
            
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title(title)
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "three_d_surface",
                "backend": backend,
                "metadata": {"cmap": cmap, "shape": z.shape}
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


def radar_chart(
    data: pd.DataFrame,
    categories: list[str],
    values: Union[list[float], dict],
    group_var: str = None,
    fill: bool = True,
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict:
    """雷达图"""
    try:
        _apply_theme()
        fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))
        
        # 计算角度
        N = len(categories)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        angles += angles[:1]  # 闭合
        
        # 绘制网格
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 100)
        
        if group_var:
            # 多组数据
            groups = data[group_var].unique()
            for i, group in enumerate(groups):
                group_data = data[data[group_var] == group]
                group_values = [group_data[cat].mean() for cat in categories]
                group_values += group_values[:1]  # 闭合
                ax.plot(angles, group_values, linewidth=2, linestyle='solid', label=group, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                if fill:
                    ax.fill(angles, group_values, alpha=0.2, color=ARCO_COLORS[i % len(ARCO_COLORS)])
            ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        else:
            # 单组数据
            if isinstance(values, dict):
                plot_values = [values[cat] for cat in categories]
            else:
                plot_values = values
            plot_values += plot_values[:1]  # 闭合
            ax.plot(angles, plot_values, linewidth=2, linestyle='solid', color=ARCO_COLORS[0])
            if fill:
                ax.fill(angles, plot_values, alpha=0.2, color=ARCO_COLORS[0])
        
        ax.set_title(title, size=15, y=1.1)
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "radar_chart",
                "backend": "matplotlib",
                "metadata": {"categories": categories, "fill": fill, "group_var": group_var}
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


def population_pyramid(
    data: pd.DataFrame,
    age_group: str,
    male_var: str,
    female_var: str,
    title: str = "",
    figsize: tuple = (10, 8)
) -> dict:
    """人口金字塔"""
    try:
        _apply_theme()
        fig, ax = plt.subplots(figsize=figsize)
        
        # 计算男性和女性数据
        male_data = data[male_var].values
        female_data = data[female_var].values
        age_groups = data[age_group].values
        
        # 绘制男性条形图（左侧）
        ax.barh(age_groups, -male_data, color=ARCO_COLORS[0], label='Male')
        
        # 绘制女性条形图（右侧）
        ax.barh(age_groups, female_data, color=ARCO_COLORS[1], label='Female')
        
        # 设置坐标轴
        ax.set_xlabel('Population')
        ax.set_ylabel('Age Group')
        ax.set_title(title or "Population Pyramid")
        ax.legend()
        
        # 设置X轴范围
        max_val = max(max(male_data), max(female_data))
        ax.set_xlim(-max_val * 1.1, max_val * 1.1)
        
        # 格式化X轴标签
        ax.set_xticks(np.linspace(-max_val, max_val, 9))
        ax.set_xticklabels([f'{abs(int(x))}' for x in np.linspace(-max_val, max_val, 9)])
        
        ax.grid(True, alpha=0.3, axis='x')
        fig.tight_layout()
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "population_pyramid",
                "backend": "matplotlib",
                "metadata": {"age_group": age_group, "male_var": male_var, "female_var": female_var}
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


def dendrogram(
    linkage_matrix: np.ndarray,
    labels: list[str] = None,
    orientation: str = "top",
    title: str = "",
    figsize: tuple = (12, 8)
) -> dict:
    """树状图"""
    try:
        _apply_theme()
        fig, ax = plt.subplots(figsize=figsize)
        
        # 绘制树状图
        scipy_dendrogram(
            linkage_matrix,
            labels=labels,
            orientation=orientation,
            distance_sort='descending',
            show_leaf_counts=True,
            ax=ax,
            color_threshold=0.7 * np.max(linkage_matrix[:, 2])
        )
        
        ax.set_title(title or "Dendrogram")
        if orientation in ['top', 'bottom']:
            ax.set_xlabel('Samples')
            ax.set_ylabel('Distance')
        else:
            ax.set_xlabel('Distance')
            ax.set_ylabel('Samples')
        
        fig.tight_layout()
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "dendrogram",
                "backend": "matplotlib",
                "metadata": {"orientation": orientation, "n_samples": linkage_matrix.shape[0] + 1}
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


def correspondence_plot(
    row_scores: pd.DataFrame,
    col_scores: pd.DataFrame,
    title: str = "",
    figsize: tuple = (10, 8)
) -> dict:
    """对应分析图"""
    try:
        _apply_theme()
        fig, ax = plt.subplots(figsize=figsize)
        
        # 绘制行点
        ax.scatter(row_scores.iloc[:, 0], row_scores.iloc[:, 1], color=ARCO_COLORS[0], label='Rows')
        for i, (_, row) in enumerate(row_scores.iterrows()):
            ax.text(row.iloc[0], row.iloc[1], row.name, fontsize=8, ha='center', va='bottom')
        
        # 绘制列点
        ax.scatter(col_scores.iloc[:, 0], col_scores.iloc[:, 1], color=ARCO_COLORS[1], label='Columns')
        for i, (_, row) in enumerate(col_scores.iterrows()):
            ax.text(row.iloc[0], row.iloc[1], row.name, fontsize=8, ha='center', va='top')
        
        # 添加坐标轴和标题
        ax.set_xlabel('Dimension 1')
        ax.set_ylabel('Dimension 2')
        ax.set_title(title or "Correspondence Analysis Plot")
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 添加原点
        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.7)
        ax.axvline(x=0, color='gray', linestyle='--', alpha=0.7)
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "correspondence_plot",
                "backend": "matplotlib",
                "metadata": {"n_rows": len(row_scores), "n_cols": len(col_scores)}
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


def word_cloud(
    text_data: Union[str, list[str]],
    max_words: int = 200,
    width: int = 800,
    height: int = 400,
    background_color: str = "white",
    colormap: str = "arco",
    font_path: str = None
) -> dict:
    """词云"""
    try:
        from wordcloud import WordCloud
        
        # 处理文本数据
        if isinstance(text_data, list):
            text = ' '.join(text_data)
        else:
            text = text_data
        
        # 创建词云
        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color=background_color,
            max_words=max_words,
            font_path=font_path,
            colormap=MATPLOTLIB_CMAPS.get(colormap, colormap)
        ).generate(text)
        
        # 绘制词云
        _apply_theme()
        fig, ax = plt.subplots(figsize=(width/100, height/100))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "word_cloud",
                "backend": "matplotlib",
                "metadata": {"max_words": max_words, "width": width, "height": height, "background_color": background_color}
            },
            "warnings": [],
            "error": None
        }
    except ImportError:
        return {
            "success": False,
            "results": {},
            "warnings": ["wordcloud library not installed"],
            "error": "wordcloud library not installed"
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }


def ridge_plot(
    data: pd.DataFrame,
    value_var: str,
    group_var: str,
    title: str = "",
    figsize: tuple = (10, 8)
) -> dict:
    """山脊图"""
    try:
        _apply_theme()
        fig, ax = plt.subplots(figsize=figsize)
        
        # 按组获取数据
        groups = data[group_var].unique()
        n_groups = len(groups)
        
        # 计算每个组的密度
        for i, group in enumerate(groups):
            group_data = data[data[group_var] == group]
            
            # 计算核密度估计
            try:
                import seaborn as sns
                sns.kdeplot(
                    data=group_data[value_var],
                    ax=ax,
                    fill=True,
                    alpha=0.6,
                    color=ARCO_COLORS[i % len(ARCO_COLORS)],
                    label=group
                )
            except ImportError:
                # 回退到matplotlib
                counts, bin_edges = np.histogram(group_data[value_var], bins=30, density=True)
                pdf = counts / sum(counts)
                ax.plot(bin_edges[:-1], pdf + i * 0.1, label=group, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                ax.fill_between(bin_edges[:-1], pdf + i * 0.1, i * 0.1, alpha=0.6, color=ARCO_COLORS[i % len(ARCO_COLORS)])
        
        ax.set_title(title or "Ridge Plot")
        ax.set_xlabel(value_var)
        ax.set_ylabel(group_var)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='x')
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "ridge_plot",
                "backend": "matplotlib",
                "metadata": {"value_var": value_var, "group_var": group_var, "n_groups": n_groups}
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


def grouped_density_plot(
    data: pd.DataFrame,
    value_var: str,
    group_var: str,
    title: str = "",
    figsize: tuple = (10, 6)
) -> dict:
    """分组密度图"""
    try:
        _apply_theme()
        fig, ax = plt.subplots(figsize=figsize)
        
        # 按组绘制密度图
        groups = data[group_var].unique()
        for i, group in enumerate(groups):
            group_data = data[data[group_var] == group]
            
            try:
                import seaborn as sns
                sns.kdeplot(
                    data=group_data[value_var],
                    ax=ax,
                    fill=True,
                    alpha=0.6,
                    color=ARCO_COLORS[i % len(ARCO_COLORS)],
                    label=group
                )
            except ImportError:
                # 回退到matplotlib
                counts, bin_edges = np.histogram(group_data[value_var], bins=30, density=True)
                pdf = counts / sum(counts)
                ax.plot(bin_edges[:-1], pdf, label=group, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                ax.fill_between(bin_edges[:-1], pdf, alpha=0.6, color=ARCO_COLORS[i % len(ARCO_COLORS)])
        
        ax.set_title(title or f"Grouped Density Plot: {value_var} by {group_var}")
        ax.set_xlabel(value_var)
        ax.set_ylabel("Density")
        ax.legend(title=group_var)
        ax.grid(True, alpha=0.3)
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "grouped_density_plot",
                "backend": "matplotlib",
                "metadata": {"value_var": value_var, "group_var": group_var, "n_groups": len(groups)}
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


def survival_curve(
    survival_table: pd.DataFrame,
    group_var: str = None,
    ci: bool = True,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict:
    """生存曲线"""
    try:
        if interactive:
            # 使用plotly
            if group_var:
                fig = px.line(
                    survival_table,
                    x='Time',
                    y='Survival Probability',
                    color=group_var,
                    title=title,
                    color_discrete_sequence=ARCO_COLORS
                )
                if ci:
                    for group in survival_table[group_var].unique():
                        group_data = survival_table[survival_table[group_var] == group]
                        fig.add_trace(go.Scatter(
                            x=group_data['Time'],
                            y=group_data.get('Lower CI', group_data['Survival Probability']),
                            mode='lines',
                            line=dict(color=ARCO_COLORS[list(survival_table[group_var].unique()).index(group)], width=1, dash='dash'),
                            showlegend=False
                        ))
                        fig.add_trace(go.Scatter(
                            x=group_data['Time'],
                            y=group_data.get('Upper CI', group_data['Survival Probability']),
                            mode='lines',
                            line=dict(color=ARCO_COLORS[list(survival_table[group_var].unique()).index(group)], width=1, dash='dash'),
                            showlegend=False
                        ))
            else:
                fig = px.line(
                    survival_table,
                    x='Time',
                    y='Survival Probability',
                    title=title,
                    color_discrete_sequence=[ARCO_COLORS[0]]
                )
                if ci:
                    fig.add_trace(go.Scatter(
                        x=survival_table['Time'],
                        y=survival_table.get('Lower CI', survival_table['Survival Probability']),
                        mode='lines',
                        line=dict(color=ARCO_COLORS[0], width=1, dash='dash'),
                        showlegend=False
                    ))
                    fig.add_trace(go.Scatter(
                        x=survival_table['Time'],
                        y=survival_table.get('Upper CI', survival_table['Survival Probability']),
                        mode='lines',
                        line=dict(color=ARCO_COLORS[0], width=1, dash='dash'),
                        showlegend=False
                    ))
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme()
            fig, ax = plt.subplots(figsize=figsize)
            
            if group_var:
                for i, group in enumerate(survival_table[group_var].unique()):
                    group_data = survival_table[survival_table[group_var] == group]
                    ax.plot(group_data['Time'], group_data['Survival Probability'], label=group, color=ARCO_COLORS[i % len(ARCO_COLORS)])
                    if ci:
                        ax.fill_between(
                            group_data['Time'],
                            group_data.get('Lower CI', group_data['Survival Probability']),
                            group_data.get('Upper CI', group_data['Survival Probability']),
                            alpha=0.2, color=ARCO_COLORS[i % len(ARCO_COLORS)]
                        )
            else:
                ax.plot(survival_table['Time'], survival_table['Survival Probability'], color=ARCO_COLORS[0])
                if ci:
                    ax.fill_between(
                        survival_table['Time'],
                        survival_table.get('Lower CI', survival_table['Survival Probability']),
                        survival_table.get('Upper CI', survival_table['Survival Probability']),
                        alpha=0.2, color=ARCO_COLORS[0]
                    )
            
            ax.set_xlabel('Time')
            ax.set_ylabel('Survival Probability')
            ax.set_title(title or "Survival Curve")
            ax.set_ylim(0, 1.05)
            ax.legend()
            ax.grid(True, alpha=0.3)
            backend = "matplotlib"
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "survival_curve",
                "backend": backend,
                "metadata": {"group_var": group_var, "ci": ci}
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


def multi_panel(
    figures: list,
    rows: int = 1,
    cols: int = None,
    titles: list[str] = None,
    sharex: bool = False,
    sharey: bool = False,
    figsize: tuple = None,
    suptitle: str = ""
) -> dict:
    """多面板图"""
    try:
        n_figures = len(figures)
        if cols is None:
            cols = n_figures // rows + (n_figures % rows > 0)
        
        if figsize is None:
            figsize = (cols * 6, rows * 4)
        
        _apply_theme()
        fig, axes = plt.subplots(rows, cols, figsize=figsize, sharex=sharex, sharey=sharey)
        
        # 处理单轴情况
        if n_figures == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
        
        # 绘制每个子图
        for i, (ax, fig_obj) in enumerate(zip(axes, figures)):
            # 这里假设fig_obj是matplotlib的Figure对象
            # 我们需要提取其中的内容
            if hasattr(fig_obj, 'gca'):
                ax_original = fig_obj.gca()
                # 复制艺术家
                for artist in ax_original.lines + ax_original.patches + ax_original.collections:
                    ax.add_artist(artist)
                # 复制坐标轴设置
                ax.set_xlabel(ax_original.get_xlabel())
                ax.set_ylabel(ax_original.get_ylabel())
                if titles:
                    ax.set_title(titles[i])
            
        # 隐藏多余的轴
        for i in range(n_figures, len(axes)):
            axes[i].set_visible(False)
        
        if suptitle:
            fig.suptitle(suptitle, fontsize=16)
        
        fig.tight_layout(rect=[0, 0, 1, 0.96] if suptitle else None)
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "multi_panel",
                "backend": "matplotlib",
                "metadata": {"n_figures": n_figures, "rows": rows, "cols": cols}
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
