import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Union
from scipy import stats
from sklearn.metrics import roc_curve, auc
from axaltyx_plot.themes.arco_theme import ARCO_COLORS, get_arco_theme


def _apply_theme():
    """应用主题"""
    plt.style.use(get_arco_theme())


def pp_plot(
    data: pd.DataFrame,
    var: str,
    dist: str = "norm",
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict:
    """P-P图"""
    try:
        _apply_theme()
        fig, ax = plt.subplots(figsize=figsize)
        
        # 获取数据
        values = data[var].dropna()
        n = len(values)
        
        # 计算经验累积分布
        empirical = np.sort(values)
        empirical_cdf = (np.arange(n) + 0.5) / n
        
        # 计算理论分布
        if dist == "norm":
            # 正态分布
            mu, sigma = stats.norm.fit(values)
            theoretical = stats.norm.ppf(empirical_cdf, mu, sigma)
        elif dist == "expon":
            # 指数分布
            loc, scale = stats.expon.fit(values)
            theoretical = stats.expon.ppf(empirical_cdf, loc, scale)
        elif dist == "weibull":
            # 威布尔分布
            shape, loc, scale = stats.weibull_min.fit(values)
            theoretical = stats.weibull_min.ppf(empirical_cdf, shape, loc, scale)
        else:
            # 默认正态分布
            mu, sigma = stats.norm.fit(values)
            theoretical = stats.norm.ppf(empirical_cdf, mu, sigma)
        
        # 绘制P-P图
        ax.scatter(theoretical, empirical, color=ARCO_COLORS[0], alpha=0.6)
        
        # 添加参考线
        min_val = min(min(theoretical), min(empirical))
        max_val = max(max(theoretical), max(empirical))
        ax.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.7)
        
        ax.set_title(title or f"P-P Plot ({dist} distribution)")
        ax.set_xlabel("Theoretical Quantiles")
        ax.set_ylabel("Empirical Quantiles")
        ax.grid(True, alpha=0.3)
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "pp_plot",
                "backend": "matplotlib",
                "metadata": {"var": var, "dist": dist, "n": n}
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


def qq_plot(
    data: pd.DataFrame,
    var: str,
    dist: str = "norm",
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict:
    """Q-Q图"""
    try:
        _apply_theme()
        fig, ax = plt.subplots(figsize=figsize)
        
        # 获取数据
        values = data[var].dropna()
        n = len(values)
        
        # 计算理论分位数
        if dist == "norm":
            # 正态分布
            stats.probplot(values, dist="norm", plot=ax)
        elif dist == "expon":
            # 指数分布
            stats.probplot(values, dist="expon", plot=ax)
        elif dist == "weibull":
            # 威布尔分布
            stats.probplot(values, dist="weibull_min", plot=ax)
        else:
            # 默认正态分布
            stats.probplot(values, dist="norm", plot=ax)
        
        ax.set_title(title or f"Q-Q Plot ({dist} distribution)")
        ax.grid(True, alpha=0.3)
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "qq_plot",
                "backend": "matplotlib",
                "metadata": {"var": var, "dist": dist, "n": n}
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


def roc_curve(
    y_true: np.ndarray,
    y_scores: np.ndarray,
    title: str = "",
    figsize: tuple = (8, 8),
    interactive: bool = False
) -> dict:
    """ROC曲线"""
    try:
        # 计算ROC曲线
        fpr, tpr, thresholds = roc_curve(y_true, y_scores)
        roc_auc = auc(fpr, tpr)
        
        # 计算最佳阈值
        gmeans = np.sqrt(tpr * (1 - fpr))
        optimal_idx = np.argmax(gmeans)
        optimal_threshold = thresholds[optimal_idx]
        
        # 计算敏感性和特异性
        sensitivity = tpr[optimal_idx]
        specificity = 1 - fpr[optimal_idx]
        
        if interactive:
            # 使用plotly
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=fpr, y=tpr,
                mode='lines',
                name=f'ROC curve (AUC = {roc_auc:.3f})',
                line=dict(color=ARCO_COLORS[0], width=2)
            ))
            fig.add_trace(go.Scatter(
                x=[0, 1], y=[0, 1],
                mode='lines',
                name='Random chance',
                line=dict(color='gray', width=1, dash='dash')
            ))
            fig.add_trace(go.Scatter(
                x=[fpr[optimal_idx]], y=[tpr[optimal_idx]],
                mode='markers',
                name=f'Optimal threshold: {optimal_threshold:.3f}',
                marker=dict(color=ARCO_COLORS[1], size=8)
            ))
            fig.update_layout(
                title=title or "ROC Curve",
                xaxis_title="False Positive Rate",
                yaxis_title="True Positive Rate",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                width=figsize[0] * 100,
                height=figsize[1] * 100
            )
            backend = "plotly"
        else:
            # 使用matplotlib
            _apply_theme()
            fig, ax = plt.subplots(figsize=figsize)
            ax.plot(fpr, tpr, color=ARCO_COLORS[0], lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
            ax.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--', label='Random chance')
            ax.plot(fpr[optimal_idx], tpr[optimal_idx], 'o', color=ARCO_COLORS[1], label=f'Optimal threshold: {optimal_threshold:.3f}')
            ax.set_xlim([0.0, 1.0])
            ax.set_ylim([0.0, 1.05])
            ax.set_xlabel('False Positive Rate')
            ax.set_ylabel('True Positive Rate')
            ax.set_title(title or 'ROC Curve')
            ax.legend(loc="lower right")
            ax.grid(True, alpha=0.3)
            backend = "matplotlib"
        
        # 准备绘图数据
        plot_data = {
            "fpr": fpr.tolist(),
            "tpr": tpr.tolist(),
            "thresholds": thresholds.tolist()
        }
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "auc": float(roc_auc),
                "optimal_threshold": float(optimal_threshold),
                "sensitivity": float(sensitivity),
                "specificity": float(specificity),
                "plot_data": plot_data,
                "type": "roc_curve",
                "backend": backend,
                "metadata": {"n_samples": len(y_true)}
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


def interaction_plot(
    data: pd.DataFrame,
    x: str,
    trace: str,
    y: str,
    title: str = "",
    figsize: tuple = (10, 6)
) -> dict:
    """交互作用图"""
    try:
        _apply_theme()
        fig, ax = plt.subplots(figsize=figsize)
        
        # 按trace分组
        traces = data[trace].unique()
        x_values = data[x].unique()
        
        for i, trace_val in enumerate(traces):
            trace_data = data[data[trace] == trace_val]
            # 计算每个x值的均值
            means = trace_data.groupby(x)[y].mean()
            ax.plot(x_values, means, label=trace_val, color=ARCO_COLORS[i % len(ARCO_COLORS)], marker='o')
        
        ax.set_title(title or f"Interaction Plot: {y} by {x} and {trace}")
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.legend(title=trace)
        ax.grid(True, alpha=0.3)
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "interaction_plot",
                "backend": "matplotlib",
                "metadata": {"x": x, "trace": trace, "y": y, "n_traces": len(traces)}
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


def means_plot(
    data: pd.DataFrame,
    dependent_var: str,
    factor_var: str,
    error_bars: str = "ci",
    ci_level: float = 0.95,
    title: str = "",
    figsize: tuple = (10, 6)
) -> dict:
    """均值图"""
    try:
        _apply_theme()
        fig, ax = plt.subplots(figsize=figsize)
        
        # 计算均值和误差
        grouped = data.groupby(factor_var)[dependent_var].agg(['mean', 'std', 'count']).reset_index()
        
        if error_bars == "ci":
            # 计算置信区间
            grouped['error'] = grouped['std'] / np.sqrt(grouped['count']) * stats.t.ppf((1 + ci_level) / 2, grouped['count'] - 1)
        elif error_bars == "std":
            # 使用标准差
            grouped['error'] = grouped['std']
        elif error_bars == "se":
            # 使用标准误
            grouped['error'] = grouped['std'] / np.sqrt(grouped['count'])
        else:
            # 无误差条
            grouped['error'] = 0
        
        # 绘制均值图
        ax.bar(grouped[factor_var], grouped['mean'], yerr=grouped['error'], color=ARCO_COLORS[0], capsize=5)
        
        ax.set_title(title or f"Means Plot: {dependent_var} by {factor_var}")
        ax.set_xlabel(factor_var)
        ax.set_ylabel(dependent_var)
        ax.grid(True, alpha=0.3, axis='y')
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "means_plot",
                "backend": "matplotlib",
                "metadata": {"dependent_var": dependent_var, "factor_var": factor_var, "error_bars": error_bars, "ci_level": ci_level}
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


def stem_leaf_plot(
    data: Union[np.ndarray, pd.Series],
    title: str = ""
) -> dict:
    """茎叶图"""
    try:
        # 转换为数组
        if isinstance(data, pd.Series):
            data = data.values
        
        # 去除NA值
        data = data[~np.isnan(data)]
        n = len(data)
        
        # 计算茎叶
        stem_leaf_dict = {}
        for val in data:
            if val < 0:
                continue  # 只处理非负值
            stem = int(val // 10)
            leaf = int(val % 10)
            if stem not in stem_leaf_dict:
                stem_leaf_dict[stem] = []
            stem_leaf_dict[stem].append(leaf)
        
        # 排序
        for stem in stem_leaf_dict:
            stem_leaf_dict[stem].sort()
        
        # 生成文本表示
        text_repr = []
        for stem in sorted(stem_leaf_dict.keys()):
            leaves = ' '.join(map(str, stem_leaf_dict[stem]))
            text_repr.append(f"{stem} | {leaves}")
        text_repr = '\n'.join(text_repr)
        
        # 创建图形
        _apply_theme()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('off')
        ax.text(0.1, 0.9, title or "Stem-and-Leaf Plot", fontsize=14, fontweight='bold')
        ax.text(0.1, 0.85, f"n = {n}", fontsize=12)
        ax.text(0.1, 0.8, text_repr, fontfamily='monospace', fontsize=10, verticalalignment='top')
        
        return {
            "success": True,
            "results": {
                "text_representation": text_repr,
                "figure": fig,
                "stem_leaf_dict": stem_leaf_dict,
                "type": "stem_leaf_plot",
                "backend": "matplotlib",
                "metadata": {"n": n}
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


def pareto_chart(
    data: pd.DataFrame,
    category_var: str,
    count_var: str = None,
    title: str = "",
    figsize: tuple = (10, 6)
) -> dict:
    """帕累托图"""
    try:
        _apply_theme()
        fig, ax1 = plt.subplots(figsize=figsize)
        ax2 = ax1.twinx()
        
        # 计算频次
        if count_var:
            # 使用指定的计数变量
            grouped = data.groupby(category_var)[count_var].sum().reset_index()
            grouped = grouped.sort_values(count_var, ascending=False)
            counts = grouped[count_var]
        else:
            # 计算频次
            counts = data[category_var].value_counts().sort_values(ascending=False)
            grouped = counts.reset_index()
            grouped.columns = [category_var, 'count']
            counts = grouped['count']
        
        categories = grouped[category_var]
        n = len(categories)
        
        # 计算累积百分比
        cumulative = counts.cumsum() / counts.sum() * 100
        
        # 绘制柱状图
        ax1.bar(range(n), counts, color=ARCO_COLORS[0])
        ax1.set_xticks(range(n))
        ax1.set_xticklabels(categories, rotation=45, ha='right')
        ax1.set_ylabel('Count')
        ax1.set_ylim(0, counts.max() * 1.1)
        
        # 绘制累积百分比线
        ax2.plot(range(n), cumulative, color=ARCO_COLORS[1], marker='o', linewidth=2)
        ax2.set_ylabel('Cumulative %')
        ax2.set_ylim(0, 100)
        
        # 添加80%参考线
        ax2.axhline(y=80, color='gray', linestyle='--', alpha=0.7)
        
        ax1.set_title(title or "Pareto Chart")
        fig.tight_layout()
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "pareto_chart",
                "backend": "matplotlib",
                "metadata": {"category_var": category_var, "count_var": count_var, "n_categories": n}
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


def autocorrelation_plot(
    data: Union[pd.Series, np.ndarray],
    nlags: int = 40,
    alpha: float = 0.05,
    title: str = "",
    figsize: tuple = (10, 4)
) -> dict:
    """自相关图"""
    try:
        _apply_theme()
        fig, ax = plt.subplots(figsize=figsize)
        
        # 转换为Series
        if isinstance(data, np.ndarray):
            data = pd.Series(data)
        
        # 计算自相关
        acf_values = []
        for lag in range(nlags + 1):
            acf = data.autocorr(lag=lag)
            acf_values.append(acf)
        
        # 计算置信区间
        conf_interval = 1.96 / np.sqrt(len(data))
        
        # 绘制自相关图
        ax.stem(range(nlags + 1), acf_values, linefmt=f'{ARCO_COLORS[0]}-', markerfmt=f'{ARCO_COLORS[0]}o', basefmt='k-')
        ax.axhline(y=conf_interval, color='gray', linestyle='--', alpha=0.7)
        ax.axhline(y=-conf_interval, color='gray', linestyle='--', alpha=0.7)
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        
        ax.set_xlabel('Lag')
        ax.set_ylabel('Autocorrelation')
        ax.set_title(title or "Autocorrelation Plot")
        ax.set_xlim(-1, nlags + 1)
        ax.set_ylim(-1, 1)
        ax.grid(True, alpha=0.3, axis='y')
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "autocorrelation_plot",
                "backend": "matplotlib",
                "metadata": {"nlags": nlags, "alpha": alpha, "n_observations": len(data)}
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


def partial_autocorrelation_plot(
    data: Union[pd.Series, np.ndarray],
    nlags: int = 40,
    alpha: float = 0.05,
    title: str = "",
    figsize: tuple = (10, 4)
) -> dict:
    """偏自相关图"""
    try:
        _apply_theme()
        fig, ax = plt.subplots(figsize=figsize)
        
        # 转换为Series
        if isinstance(data, np.ndarray):
            data = pd.Series(data)
        
        # 计算偏自相关
        from statsmodels.tsa.stattools import pacf
        pacf_values, conf_int = pacf(data, nlags=nlags, alpha=alpha)
        
        # 计算置信区间
        conf_interval = conf_int[0, 1] - pacf_values[0]
        
        # 绘制偏自相关图
        ax.stem(range(nlags + 1), pacf_values, linefmt=f'{ARCO_COLORS[0]}-', markerfmt=f'{ARCO_COLORS[0]}o', basefmt='k-')
        ax.axhline(y=conf_interval, color='gray', linestyle='--', alpha=0.7)
        ax.axhline(y=-conf_interval, color='gray', linestyle='--', alpha=0.7)
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        
        ax.set_xlabel('Lag')
        ax.set_ylabel('Partial Autocorrelation')
        ax.set_title(title or "Partial Autocorrelation Plot")
        ax.set_xlim(-1, nlags + 1)
        ax.set_ylim(-1, 1)
        ax.grid(True, alpha=0.3, axis='y')
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "partial_autocorrelation_plot",
                "backend": "matplotlib",
                "metadata": {"nlags": nlags, "alpha": alpha, "n_observations": len(data)}
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


def forest_plot(
    estimates: list[float],
    ci_lower: list[float],
    ci_upper: list[float],
    labels: list[str] = None,
    overall: dict = None,
    title: str = "",
    figsize: tuple = (10, 8)
) -> dict:
    """森林图"""
    try:
        _apply_theme()
        fig, ax = plt.subplots(figsize=figsize)
        
        n = len(estimates)
        if labels is None:
            labels = [f'Study {i+1}' for i in range(n)]
        
        # 绘制置信区间
        y_pos = np.arange(n, 0, -1)
        ax.errorbar(estimates, y_pos, xerr=[(est - lower) for est, lower in zip(estimates, ci_lower)],
                   fmt='o', color=ARCO_COLORS[0], capsize=5, elinewidth=2, markersize=6)
        
        # 绘制总体效应
        if overall:
            ax.axvline(x=overall['estimate'], color=ARCO_COLORS[1], linestyle='--', linewidth=2)
            if 'ci_lower' in overall and 'ci_upper' in overall:
                ax.axvspan(overall['ci_lower'], overall['ci_upper'], color=ARCO_COLORS[1], alpha=0.2)
        
        # 绘制零效应线
        ax.axvline(x=0, color='gray', linestyle='-', linewidth=1, alpha=0.7)
        
        # 设置Y轴标签
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.set_ylim(0.5, n + 0.5)
        
        ax.set_xlabel('Effect Size')
        ax.set_title(title or "Forest Plot")
        ax.grid(True, alpha=0.3, axis='x')
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "forest_plot",
                "backend": "matplotlib",
                "metadata": {"n_estimates": n, "has_overall": overall is not None}
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


def funnel_plot(
    estimates: list[float],
    standard_errors: list[float],
    labels: list[str] = None,
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict:
    """漏斗图"""
    try:
        _apply_theme()
        fig, ax = plt.subplots(figsize=figsize)
        
        n = len(estimates)
        if labels is None:
            labels = [f'Study {i+1}' for i in range(n)]
        
        # 计算精度（1/SE）
        precision = [1 / se for se in standard_errors]
        
        # 绘制散点
        scatter = ax.scatter(estimates, precision, s=50, alpha=0.6, color=ARCO_COLORS[0])
        
        # 绘制漏斗轮廓
        x = np.linspace(min(estimates) - 1, max(estimates) + 1, 100)
        y = 1 / (1.96 * np.abs(x))  # 95% 置信区间
        ax.plot(x, y, 'k--', alpha=0.7)
        ax.plot(x, -y, 'k--', alpha=0.7)
        
        # 绘制零效应线
        ax.axvline(x=0, color='gray', linestyle='-', linewidth=1, alpha=0.7)
        
        ax.set_xlabel('Effect Size')
        ax.set_ylabel('Precision (1/SE)')
        ax.set_title(title or "Funnel Plot")
        ax.grid(True, alpha=0.3)
        
        return {
            "success": True,
            "results": {
                "figure": fig,
                "type": "funnel_plot",
                "backend": "matplotlib",
                "metadata": {"n_estimates": n}
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
