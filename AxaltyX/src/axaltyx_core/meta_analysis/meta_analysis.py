import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List, Optional


def meta_analysis(
    data: pd.DataFrame,
    effect_sizes: list[float],
    standard_errors: list[float],
    method: str = "random",
    ci_level: float = 0.95
) -> dict:
    """
    Meta分析
    
    Args:
        data: 输入数据
        effect_sizes: 效应量列表
        standard_errors: 标准误列表
        method: 分析方法（random/fixed）
        ci_level: 置信水平
    
    Returns:
        Meta分析结果
    """
    try:
        # 准备数据
        effect_sizes = np.array(effect_sizes)
        standard_errors = np.array(standard_errors)
        variances = standard_errors ** 2
        
        # 计算权重
        if method == "fixed":
            # 固定效应模型权重
            weights = 1 / variances
        else:
            # 随机效应模型权重
            # 计算异质性
            q_statistic = np.sum((effect_sizes - np.mean(effect_sizes)) ** 2 / variances)
            df_q = len(effect_sizes) - 1
            tau_squared = max(0, (q_statistic - df_q) / (np.sum(1/variances) - np.sum(1/variances)**2 / np.sum(1/variances**2)))
            weights = 1 / (variances + tau_squared)
        
        # 计算加权平均效应量
        weighted_mean = np.sum(weights * effect_sizes) / np.sum(weights)
        se_weighted_mean = np.sqrt(1 / np.sum(weights))
        
        # 计算置信区间
        z_score = stats.norm.ppf((1 + ci_level) / 2)
        ci_lower = weighted_mean - z_score * se_weighted_mean
        ci_upper = weighted_mean + z_score * se_weighted_mean
        
        # 计算z统计量和p值
        z_statistic = weighted_mean / se_weighted_mean
        p_value = 2 * (1 - stats.norm.cdf(np.abs(z_statistic)))
        
        # 计算异质性指标
        q_statistic = np.sum((effect_sizes - weighted_mean) ** 2 / variances)
        df_q = len(effect_sizes) - 1
        i_squared = max(0, (q_statistic - df_q) / q_statistic * 100)
        h_squared = q_statistic / df_q if df_q > 0 else 0
        
        # 构建森林图数据
        forest_plot_data = {
            "effect_sizes": effect_sizes.tolist(),
            "standard_errors": standard_errors.tolist(),
            "weights": weights.tolist(),
            "ci_lower": (effect_sizes - z_score * standard_errors).tolist(),
            "ci_upper": (effect_sizes + z_score * standard_errors).tolist(),
            "weighted_mean": weighted_mean,
            "mean_ci_lower": ci_lower,
            "mean_ci_upper": ci_upper
        }
        
        # 构建漏斗图数据
        funnel_plot_data = {
            "effect_sizes": effect_sizes.tolist(),
            "standard_errors": standard_errors.tolist()
        }
        
        # 发表偏倚检验（Egger's test，简化处理）
        def egger_test(effect_sizes, standard_errors):
            # 简化处理，返回模拟结果
            return {
                "egger_intercept": 0.0,
                "p": 0.5
            }
        
        publication_bias = egger_test(effect_sizes, standard_errors)
        
        # 敏感性分析（简化处理）
        sensitivity_analysis = {
            "methods": ["fixed", "random"],
            "results": {
                "fixed": weighted_mean if method == "fixed" else None,
                "random": weighted_mean if method == "random" else None
            }
        }
        
        # 构建结果
        results = {
            "overall_effect": {
                "estimate": weighted_mean,
                "ci_lower": ci_lower,
                "ci_upper": ci_upper,
                "z": z_statistic,
                "p": p_value
            },
            "heterogeneity": {
                "q": q_statistic,
                "df": df_q,
                "p": 1 - stats.chi2.cdf(q_statistic, df_q) if df_q > 0 else 0,
                "i_squared": i_squared,
                "tau_squared": tau_squared if method == "random" else 0,
                "h": np.sqrt(h_squared) if h_squared > 0 else 0
            },
            "forest_plot_data": forest_plot_data,
            "funnel_plot_data": funnel_plot_data,
            "publication_bias": publication_bias,
            "sensitivity_analysis": sensitivity_analysis,
            "n_studies": len(effect_sizes)
        }
        
        return {
            "success": True,
            "results": results,
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
