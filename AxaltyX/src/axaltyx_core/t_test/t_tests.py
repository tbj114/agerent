import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List, Optional


def one_sample_t(
    data: pd.DataFrame,
    var: str,
    test_value: float = 0,
    ci_level: float = 0.95
) -> dict:
    """
    单样本t检验（详细版）
    
    Args:
        data: 输入数据
        var: 检验变量
        test_value: 检验值
        ci_level: 置信水平
    
    Returns:
        单样本t检验结果
    """
    try:
        # 提取数据
        values = data[var].dropna()
        n = len(values)
        mean = values.mean()
        std = values.std()
        sem = stats.sem(values)
        mean_diff = mean - test_value
        
        # 计算t统计量
        t_stat, p_value = stats.ttest_1samp(values, test_value)
        
        # 计算自由度
        df = n - 1
        
        # 计算置信区间
        ci = stats.t.interval(ci_level, df, loc=mean_diff, scale=sem)
        ci_lower, ci_upper = ci
        
        # 计算Cohen's d
        cohens_d = mean_diff / std if std != 0 else 0
        
        return {
            "success": True,
            "results": {
                "t": t_stat,
                "df": df,
                "p_value": p_value,
                "mean_diff": mean_diff,
                "se": sem,
                "ci_lower": ci_lower,
                "ci_upper": ci_upper,
                "cohens_d": cohens_d,
                "sample_mean": mean,
                "sample_std": std,
                "n": n,
                "ci_level": ci_level
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


def independent_t(
    data: pd.DataFrame,
    test_var: str,
    group_var: str,
    group1: str = None,
    group2: str = None,
    equal_var: bool = True,
    ci_level: float = 0.95
) -> dict:
    """
    独立样本t检验（详细版）
    
    Args:
        data: 输入数据
        test_var: 检验变量
        group_var: 分组变量
        group1: 第一组值（None 取前两个唯一值）
        group2: 第二组值
        equal_var: 是否假设方差齐性
        ci_level: 置信水平
    
    Returns:
        独立样本t检验结果
    """
    try:
        # 提取分组值
        groups = data[group_var].unique()
        if len(groups) < 2:
            raise ValueError("分组变量至少需要有两个水平")
        # 只使用前两个水平
        groups = groups[:2]
        
        # 确定两组值
        if group1 is None and group2 is None:
            group1 = groups[0]
            group2 = groups[1]
        elif group1 is None:
            group1 = groups[0]
        elif group2 is None:
            group2 = groups[1]
        
        # 提取两组数据
        group1_data = data[data[group_var] == group1][test_var].dropna()
        group2_data = data[data[group_var] == group2][test_var].dropna()
        
        # 计算组统计量
        n1 = len(group1_data)
        n2 = len(group2_data)
        s1_sq = group1_data.var()
        s2_sq = group2_data.var()
        
        group_stats = {
            "group1": {
                "n": n1,
                "mean": group1_data.mean(),
                "std": group1_data.std(),
                "se": stats.sem(group1_data)
            },
            "group2": {
                "n": n2,
                "mean": group2_data.mean(),
                "std": group2_data.std(),
                "se": stats.sem(group2_data)
            }
        }
        
        # 计算Levene检验（方差齐性检验）
        levene_stat, levene_p = stats.levene(group1_data, group2_data)
        
        # 执行t检验
        if equal_var:
            t_stat, p_value = stats.ttest_ind(group1_data, group2_data, equal_var=True)
            df = n1 + n2 - 2
        else:
            t_stat, p_value = stats.ttest_ind(group1_data, group2_data, equal_var=False)
            # 计算Welch-Satterthwaite自由度
            df = (s1_sq/n1 + s2_sq/n2)**2 / ((s1_sq/n1)**2/(n1-1) + (s2_sq/n2)**2/(n2-1))
        
        # 计算均值差和标准误
        mean_diff = group1_data.mean() - group2_data.mean()
        if equal_var:
            pooled_var = ((n1-1)*s1_sq + (n2-1)*s2_sq) / (n1 + n2 - 2)
            se_diff = np.sqrt(pooled_var * (1/n1 + 1/n2))
        else:
            se_diff = np.sqrt(s1_sq/n1 + s2_sq/n2)
        
        # 计算置信区间
        ci = stats.t.interval(ci_level, df, loc=mean_diff, scale=se_diff)
        ci_lower, ci_upper = ci
        
        # 计算效应量
        if equal_var:
            cohens_d = mean_diff / np.sqrt(pooled_var)
        else:
            cohens_d = mean_diff / np.sqrt((s1_sq + s2_sq) / 2)
        
        # 计算Hedges' g
        hedges_g = cohens_d * (1 - 3 / (4 * (n1 + n2) - 9))
        
        # 计算Glass's delta
        glass_delta = mean_diff / group1_data.std() if group1_data.std() != 0 else 0
        
        return {
            "success": True,
            "results": {
                "group_stats": group_stats,
                "levene_test": {
                    "f": levene_stat,
                    "df1": 1,
                    "df2": n1 + n2 - 2,
                    "p": levene_p
                },
                "t_test": {
                    "t": t_stat,
                    "df": df,
                    "p_value": p_value,
                    "mean_diff": mean_diff,
                    "se_diff": se_diff,
                    "ci_lower": ci_lower,
                    "ci_upper": ci_upper,
                    "equal_variance_assumed": equal_var
                },
                "effect_size": {
                    "cohens_d": cohens_d,
                    "hedges_g": hedges_g,
                    "glass_delta": glass_delta
                },
                "ci_level": ci_level
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


def paired_t(
    data: pd.DataFrame,
    var1: str,
    var2: str,
    ci_level: float = 0.95
) -> dict:
    """
    配对样本t检验（详细版）
    
    Args:
        data: 输入数据
        var1: 第一个变量
        var2: 第二个变量
        ci_level: 置信水平
    
    Returns:
        配对样本t检验结果
    """
    try:
        # 提取配对数据
        paired_data = data[[var1, var2]].dropna()
        var1_data = paired_data[var1]
        var2_data = paired_data[var2]
        
        # 计算差值
        diff = var1_data - var2_data
        
        # 计算配对统计量
        pair_stats = {
            "var1": {
                "mean": var1_data.mean(),
                "std": var1_data.std(),
                "se": stats.sem(var1_data),
                "n": len(var1_data)
            },
            "var2": {
                "mean": var2_data.mean(),
                "std": var2_data.std(),
                "se": stats.sem(var2_data),
                "n": len(var2_data)
            },
            "diff": {
                "mean": diff.mean(),
                "std": diff.std(),
                "se": stats.sem(diff),
                "n": len(diff)
            }
        }
        
        # 计算相关系数
        correlation, corr_p = stats.pearsonr(var1_data, var2_data)
        
        # 执行配对t检验
        t_stat, p_value = stats.ttest_rel(var1_data, var2_data)
        
        # 计算自由度
        df = len(diff) - 1
        
        # 计算均值差和标准误
        mean_diff = diff.mean()
        se_diff = stats.sem(diff)
        
        # 计算置信区间
        ci = stats.t.interval(ci_level, df, loc=mean_diff, scale=se_diff)
        ci_lower, ci_upper = ci
        
        # 计算Cohen's d
        cohens_d = mean_diff / diff.std() if diff.std() != 0 else 0
        
        return {
            "success": True,
            "results": {
                "pair_stats": pair_stats,
                "correlation": {
                    "r": correlation,
                    "p": corr_p
                },
                "t_test": {
                    "t": t_stat,
                    "df": df,
                    "p_value": p_value,
                    "mean_diff": mean_diff,
                    "se_diff": se_diff,
                    "ci_lower": ci_lower,
                    "ci_upper": ci_upper
                },
                "effect_size": {
                    "cohens_d": cohens_d
                },
                "ci_level": ci_level
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
