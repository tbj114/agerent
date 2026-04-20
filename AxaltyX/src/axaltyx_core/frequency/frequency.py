import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


def frequencies(
    data: pd.DataFrame,
    vars: list[str],
    format: str = "table",
    order: str = "ascending",
    multiple_responses: bool = False
) -> dict:
    """
    频数分析
    
    Args:
        data: 输入数据
        vars: 分析变量列表
        format: 输出格式（table/chart）
        order: 排序方式
        multiple_responses: 是否为多重响应集
    
    Returns:
        频数分析结果
    """
    try:
        tables = {}
        charts_data = {}
        summary = {}
        
        for var in vars:
            # 计算频数
            freq = data[var].value_counts(dropna=False)
            
            # 排序
            if order == "ascending":
                freq = freq.sort_index(ascending=True)
            elif order == "descending":
                freq = freq.sort_index(ascending=False)
            
            # 计算百分比
            total = len(data)
            pct = (freq / total) * 100
            valid_total = data[var].count()
            valid_pct = (freq / valid_total) * 100 if valid_total > 0 else 0
            
            # 构建频数表
            frequency_table = pd.DataFrame({
                'value': freq.index,
                'frequency': freq.values,
                'percentage': pct.values,
                'valid_percentage': valid_pct.values
            })
            
            # 计算累积频数和百分比
            cumulative_freq = freq.cumsum()
            cumulative_pct = (cumulative_freq / total) * 100
            cumulative_valid_pct = (cumulative_freq / valid_total) * 100 if valid_total > 0 else 0
            
            cumulative_table = pd.DataFrame({
                'value': freq.index,
                'cumulative_frequency': cumulative_freq.values,
                'cumulative_percentage': cumulative_pct.values,
                'cumulative_valid_percentage': cumulative_valid_pct.values
            })
            
            # 存储结果
            tables[var] = {
                'frequencies': frequency_table,
                'cumulative': cumulative_table,
                'valid_n': valid_total,
                'missing_n': total - valid_total,
                'total_n': total,
                'n_categories': len(freq)
            }
            
            # 准备图表数据
            if format == "chart":
                charts_data[var] = {
                    'values': freq.index.tolist(),
                    'frequencies': freq.values.tolist(),
                    'percentages': pct.values.tolist()
                }
        
        # 生成汇总信息
        summary['n_variables'] = len(vars)
        summary['n_cases'] = len(data)
        
        return {
            "success": True,
            "results": {
                "tables": tables,
                "charts_data": charts_data,
                "summary": summary
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


def multiple_response_frequencies(
    data: pd.DataFrame,
    var_sets: dict,
    dichotomies: dict = None
) -> dict:
    """
    多重响应频数分析
    
    Args:
        data: 输入数据
        var_sets: 多重响应集定义 `{集名: [变量列表]}`
        dichotomies: 二分变量定义 `{变量名: 计数值}`
    
    Returns:
        多重响应频数分析结果
    """
    try:
        tables = {}
        response_rates = {}
        total_responses = {}
        
        for set_name, variables in var_sets.items():
            # 计算每个响应集的频数
            set_data = data[variables]
            
            # 处理二分变量
            if dichotomies:
                for var in variables:
                    if var in dichotomies:
                        set_data[var] = (set_data[var] == dichotomies[var]).astype(int)
            
            # 计算每个变量的响应数
            response_counts = set_data.sum()
            total_responses_in_set = response_counts.sum()
            n_cases = len(data)
            
            # 计算响应率
            response_rate = (response_counts > 0).sum() / n_cases * 100 if n_cases > 0 else 0
            
            # 构建频数表
            frequency_table = pd.DataFrame({
                'variable': response_counts.index,
                'frequency': response_counts.values,
                'percentage': (response_counts / total_responses_in_set) * 100 if total_responses_in_set > 0 else 0,
                'response_rate': (response_counts / n_cases) * 100 if n_cases > 0 else 0
            })
            
            # 存储结果
            tables[set_name] = frequency_table
            response_rates[set_name] = response_rate
            total_responses[set_name] = total_responses_in_set
        
        return {
            "success": True,
            "results": {
                "tables": tables,
                "response_rates": response_rates,
                "total_responses": total_responses
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
