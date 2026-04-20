import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List, Optional


def descriptive_stats(
    data: pd.DataFrame,
    vars: list[str] = None,
    statistics: list[str] = None
) -> dict:
    """
    描述性统计
    
    Args:
        data: 输入数据
        vars: 目标变量列表，None 则分析全部数值列
        statistics: 统计量列表
    
    Returns:
        描述性统计结果
    """
    try:
        # 确定分析变量
        if vars is None:
            analysis_vars = data.select_dtypes(include=[np.number]).columns.tolist()
        else:
            analysis_vars = vars
        
        # 确定统计量
        default_stats = ['mean', 'median', 'mode', 'std', 'variance', 'min', 'max', 'range',
                        'skewness', 'kurtosis', 'sum', 'count', 'sem', 'cv', 'percentiles']
        if statistics is None:
            analysis_stats = default_stats
        else:
            analysis_stats = statistics
        
        # 计算统计量
        results = {}
        for var in analysis_vars:
            var_data = data[var].dropna()
            var_stats = {}
            
            if 'mean' in analysis_stats:
                var_stats['mean'] = var_data.mean()
            if 'median' in analysis_stats:
                var_stats['median'] = var_data.median()
            if 'mode' in analysis_stats:
                mode_result = var_data.mode()
                var_stats['mode'] = mode_result.iloc[0] if not mode_result.empty else None
            if 'std' in analysis_stats:
                var_stats['std'] = var_data.std()
            if 'variance' in analysis_stats:
                var_stats['variance'] = var_data.var()
            if 'min' in analysis_stats:
                var_stats['min'] = var_data.min()
            if 'max' in analysis_stats:
                var_stats['max'] = var_data.max()
            if 'range' in analysis_stats:
                var_stats['range'] = var_data.max() - var_data.min()
            if 'skewness' in analysis_stats:
                var_stats['skewness'] = var_data.skew()
            if 'kurtosis' in analysis_stats:
                var_stats['kurtosis'] = var_data.kurtosis()
            if 'sum' in analysis_stats:
                var_stats['sum'] = var_data.sum()
            if 'count' in analysis_stats:
                var_stats['count'] = var_data.count()
            if 'sem' in analysis_stats:
                var_stats['sem'] = stats.sem(var_data)
            if 'cv' in analysis_stats:
                mean = var_data.mean()
                std = var_data.std()
                var_stats['cv'] = std / mean if mean != 0 else 0
            if 'percentiles' in analysis_stats:
                var_stats['percentiles'] = {
                    '5%': np.percentile(var_data, 5),
                    '25%': np.percentile(var_data, 25),
                    '50%': np.percentile(var_data, 50),
                    '75%': np.percentile(var_data, 75),
                    '95%': np.percentile(var_data, 95)
                }
            
            results[var] = var_stats
        
        # 构建返回结果
        table = pd.DataFrame(results).T
        
        return {
            "success": True,
            "results": {
                "table": table,
                "variables": analysis_vars,
                "statistics": analysis_stats,
                "n_cases": len(data)
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


def frequency_table(
    data: pd.DataFrame,
    var: str,
    sort: str = "value",
    cumulative: bool = True
) -> dict:
    """
    频数表
    
    Args:
        data: 输入数据
        var: 目标变量
        sort: 排序方式（value/frequency/descending）
        cumulative: 是否计算累积百分比
    
    Returns:
        频数表结果
    """
    try:
        # 计算频数
        freq = data[var].value_counts(dropna=False)
        
        # 排序
        if sort == "frequency":
            freq = freq.sort_values(ascending=False)
        elif sort == "descending":
            freq = freq.sort_index(ascending=False)
        # 默认按值排序
        
        # 计算百分比
        total = len(data)
        pct = (freq / total) * 100
        
        # 计算有效百分比（排除缺失值）
        valid_total = data[var].count()
        valid_pct = (freq / valid_total) * 100
        
        # 构建频数表
        frequencies = pd.DataFrame({
            'value': freq.index,
            'frequency': freq.values,
            'percentage': pct.values,
            'valid_percentage': valid_pct.values
        })
        
        # 计算累积频数和百分比
        if cumulative:
            cumulative_freq = freq.cumsum()
            cumulative_pct = (cumulative_freq / total) * 100
            cumulative_valid_pct = (cumulative_freq / valid_total) * 100
            
            cumulative = pd.DataFrame({
                'value': freq.index,
                'cumulative_frequency': cumulative_freq.values,
                'cumulative_percentage': cumulative_pct.values,
                'cumulative_valid_percentage': cumulative_valid_pct.values
            })
        else:
            cumulative = None
        
        # 计算统计量
        valid_n = valid_total
        missing_n = total - valid_total
        total_n = total
        n_categories = len(freq)
        
        return {
            "success": True,
            "results": {
                "frequencies": frequencies,
                "cumulative": cumulative,
                "valid_n": valid_n,
                "missing_n": missing_n,
                "total_n": total_n,
                "n_categories": n_categories
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


def cross_tabulation(
    data: pd.DataFrame,
    row_var: str,
    col_var: str,
    expected: bool = False,
    percentages: str = "none"
) -> dict:
    """
    交叉表
    
    Args:
        data: 输入数据
        row_var: 行变量
        col_var: 列变量
        expected: 是否计算期望频数
        percentages: 百分比类型（none/row/column/total）
    
    Returns:
        交叉表结果
    """
    try:
        # 处理列变量表达式
        if '>' in col_var or '<' in col_var or '==' in col_var:
            # 尝试评估表达式，处理带空格的列名
            # 构建一个安全的命名空间，将列名映射到数据
            namespace = {}
            for col in data.columns:
                # 为带空格的列名创建一个安全的变量名
                safe_name = col.replace(' ', '_').replace('(', '').replace(')', '').replace('.', '_')
                namespace[safe_name] = data[col]
                # 同时保留原始列名（如果没有特殊字符）
                try:
                    exec(f"{col} = data[col]", namespace)
                except:
                    pass
            
            # 替换表达式中的列名为安全变量名
            expr = col_var
            for col in data.columns:
                if col in expr:
                    safe_name = col.replace(' ', '_').replace('(', '').replace(')', '').replace('.', '_')
                    expr = expr.replace(col, safe_name)
            
            # 评估表达式
            col_data = eval(expr, {}, namespace)
        else:
            # 直接使用列名
            col_data = data[col_var]
        
        # 创建交叉表
        table = pd.crosstab(data[row_var], col_data)
        
        # 计算行总和和列总和
        row_totals = table.sum(axis=1)
        col_totals = table.sum(axis=0)
        
        # 计算卡方检验
        chi2, p_value, df, expected_freq = stats.chi2_contingency(table)
        
        # 计算期望频数
        if expected:
            expected_df = pd.DataFrame(expected_freq, index=table.index, columns=table.columns)
        else:
            expected_df = None
        
        # 计算百分比
        if percentages != "none":
            if percentages == "row":
                pct_table = table.div(row_totals, axis=0) * 100
            elif percentages == "column":
                pct_table = table.div(col_totals, axis=1) * 100
            elif percentages == "total":
                pct_table = table.div(len(data)) * 100
            else:
                pct_table = None
        else:
            pct_table = None
        
        return {
            "success": True,
            "results": {
                "table": table,
                "row_totals": row_totals,
                "col_totals": col_totals,
                "chi2": chi2,
                "df": df,
                "p_value": p_value,
                "expected": expected_df,
                "percentages": pct_table
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
