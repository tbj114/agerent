import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List, Optional


def means(
    data: pd.DataFrame,
    dependent_vars: list[str],
    independent_var: str,
    statistics: list[str] = None
) -> dict:
    """
    均值比较
    
    Args:
        data: 输入数据
        dependent_vars: 因变量列表
        independent_var: 自变量（分组变量）
        statistics: 统计量（mean/std/variance/n/min/max/kurtosis/skewness/se）
    
    Returns:
        均值比较结果
    """
    try:
        # 确定统计量
        default_stats = ['mean', 'std', 'variance', 'n', 'min', 'max', 'kurtosis', 'skewness', 'se']
        if statistics is None:
            analysis_stats = default_stats
        else:
            analysis_stats = statistics
        
        # 计算分组统计量
        group_stats = {}
        for var in dependent_vars:
            grouped = data.groupby(independent_var)[var]
            stats_dict = {}
            
            if 'mean' in analysis_stats:
                stats_dict['mean'] = grouped.mean()
            if 'std' in analysis_stats:
                stats_dict['std'] = grouped.std()
            if 'variance' in analysis_stats:
                stats_dict['variance'] = grouped.var()
            if 'n' in analysis_stats:
                stats_dict['n'] = grouped.count()
            if 'min' in analysis_stats:
                stats_dict['min'] = grouped.min()
            if 'max' in analysis_stats:
                stats_dict['max'] = grouped.max()
            if 'kurtosis' in analysis_stats:
                stats_dict['kurtosis'] = grouped.apply(lambda x: x.kurtosis())
            if 'skewness' in analysis_stats:
                stats_dict['skewness'] = grouped.apply(lambda x: x.skew())
            if 'se' in analysis_stats:
                stats_dict['se'] = grouped.apply(lambda x: stats.sem(x))
            
            group_stats[var] = pd.DataFrame(stats_dict)
        
        # 计算单因素方差分析
        anova_table = {}
        eta_squared = {}
        omega_squared = {}
        
        for var in dependent_vars:
            # 获取各组数据
            groups = [group[var].values for name, group in data.groupby(independent_var)]
            
            # 方差分析
            f_stat, p_value = stats.f_oneway(*groups)
            
            # 计算自由度
            k = len(groups)
            n = sum(len(group) for group in groups)
            df_between = k - 1
            df_within = n - k
            
            # 计算平方和
            grand_mean = data[var].mean()
            ss_between = sum(len(group) * (group.mean() - grand_mean)**2 for group in groups)
            ss_within = sum(sum((x - group.mean())**2 for x in group) for group in groups)
            ss_total = ss_between + ss_within
            
            # 计算均方
            ms_between = ss_between / df_between
            ms_within = ss_within / df_within
            
            # 计算效应量
            eta_sq = ss_between / ss_total
            omega_sq = (ss_between - (df_between * ms_within)) / (ss_total + ms_within)
            
            anova_table[var] = {
                'ss_between': ss_between,
                'ss_within': ss_within,
                'ss_total': ss_total,
                'df_between': df_between,
                'df_within': df_within,
                'ms_between': ms_between,
                'ms_within': ms_within,
                'f': f_stat,
                'p': p_value
            }
            
            eta_squared[var] = eta_sq
            omega_squared[var] = omega_sq
        
        return {
            "success": True,
            "results": {
                "group_stats": group_stats,
                "anova_table": anova_table,
                "eta_squared": eta_squared,
                "omega_squared": omega_squared
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


def one_sample_t_test(
    data: pd.DataFrame,
    var: str,
    test_value: float = 0
) -> dict:
    """
    单样本t检验
    
    Args:
        data: 输入数据
        var: 检验变量
        test_value: 检验值
    
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
        ci = stats.t.interval(0.95, df, loc=mean_diff, scale=sem)
        ci_lower, ci_upper = ci
        
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
                "sample_mean": mean,
                "sample_std": std,
                "n": n
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


def independent_samples_t_test(
    data: pd.DataFrame,
    test_var: str,
    group_var: str,
    equal_variance: bool = True
) -> dict:
    """
    独立样本t检验
    
    Args:
        data: 输入数据
        test_var: 检验变量
        group_var: 分组变量
        equal_variance: 是否假设方差齐性
    
    Returns:
        独立样本t检验结果
    """
    try:
        # 提取两组数据
        groups = data[group_var].unique()
        if len(groups) < 2:
            raise ValueError("分组变量至少需要有两个水平")
        # 只使用前两个水平
        groups = groups[:2]
        
        group1_data = data[data[group_var] == groups[0]][test_var].dropna()
        group2_data = data[data[group_var] == groups[1]][test_var].dropna()
        
        # 计算组统计量
        n1 = len(group1_data)
        n2 = len(group2_data)
        s1_sq = group1_data.var()
        s2_sq = group2_data.var()
        
        group_stats = {
            groups[0]: {
                "n": n1,
                "mean": group1_data.mean(),
                "std": group1_data.std(),
                "se": stats.sem(group1_data)
            },
            groups[1]: {
                "n": n2,
                "mean": group2_data.mean(),
                "std": group2_data.std(),
                "se": stats.sem(group2_data)
            }
        }
        
        # 计算Levene检验（方差齐性检验）
        levene_stat, levene_p = stats.levene(group1_data, group2_data)
        
        # 执行t检验
        if equal_variance:
            t_stat, p_value = stats.ttest_ind(group1_data, group2_data, equal_var=True)
            df = n1 + n2 - 2
        else:
            t_stat, p_value = stats.ttest_ind(group1_data, group2_data, equal_var=False)
            # 计算Welch-Satterthwaite自由度
            df = (s1_sq/n1 + s2_sq/n2)**2 / ((s1_sq/n1)**2/(n1-1) + (s2_sq/n2)**2/(n2-1))
        
        # 计算均值差和标准误
        mean_diff = group1_data.mean() - group2_data.mean()
        if equal_variance:
            pooled_var = ((n1-1)*s1_sq + (n2-1)*s2_sq) / (n1 + n2 - 2)
            se_diff = np.sqrt(pooled_var * (1/n1 + 1/n2))
        else:
            se_diff = np.sqrt(s1_sq/n1 + s2_sq/n2)
        
        # 计算置信区间
        ci = stats.t.interval(0.95, df, loc=mean_diff, scale=se_diff)
        
        # 计算Cohen's d
        if equal_variance:
            cohens_d = mean_diff / np.sqrt(pooled_var)
        else:
            cohens_d = mean_diff / np.sqrt((s1_sq + s2_sq) / 2)
        
        return {
            "success": True,
            "results": {
                "group_stats": group_stats,
                "levene_test": {"f": levene_stat, "p": levene_p},
                "t_equal": {
                    "t": t_stat,
                    "df": df,
                    "p": p_value,
                    "mean_diff": mean_diff,
                    "se": se_diff,
                    "ci": ci
                },
                "t_unequal": {
                    "t": t_stat,
                    "df": df,
                    "p": p_value,
                    "mean_diff": mean_diff,
                    "se": se_diff,
                    "ci": ci
                },
                "cohens_d": cohens_d
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


def paired_samples_t_test(
    data: pd.DataFrame,
    var1: str,
    var2: str
) -> dict:
    """
    配对样本t检验
    
    Args:
        data: 输入数据
        var1: 第一个变量
        var2: 第二个变量
    
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
            var1: {
                "mean": var1_data.mean(),
                "std": var1_data.std(),
                "se": stats.sem(var1_data),
                "n": len(var1_data)
            },
            var2: {
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
        ci = stats.t.interval(0.95, df, loc=mean_diff, scale=se_diff)
        ci_lower, ci_upper = ci
        
        # 计算Cohen's d
        cohens_d = mean_diff / diff.std()
        
        return {
            "success": True,
            "results": {
                "pair_stats": pair_stats,
                "correlation": correlation,
                "t": t_stat,
                "df": df,
                "p_value": p_value,
                "mean_diff": mean_diff,
                "se": se_diff,
                "ci_lower": ci_lower,
                "ci_upper": ci_upper,
                "cohens_d": cohens_d
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
