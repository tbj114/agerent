
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Union, Optional


def merge_datasets(
    left: pd.DataFrame,
    right: pd.DataFrame,
    on: Union[str, list],
    how: str = "inner"
) -> dict:
    """
    合并两个数据集
    
    Args:
        left: 左表
        right: 右表
        on: 合并键
        how: 合并方式（inner/left/right/outer）
    
    Returns:
        合并结果
    """
    try:
        # 合并数据
        merged = pd.merge(left, right, on=on, how=how)
        
        return {
            "success": True,
            "results": {
                "data": merged,
                "shape": merged.shape,
                "merge_keys": on,
                "merged_rows": merged.shape[0]
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


def sort_data(
    data: pd.DataFrame,
    by: Union[str, list],
    ascending: Union[bool, list] = True
) -> dict:
    """
    排序数据
    
    Args:
        data: 输入数据
        by: 排序字段
        ascending: 是否升序
    
    Returns:
        排序结果
    """
    try:
        # 排序
        sorted_data = data.sort_values(by=by, ascending=ascending)
        
        return {
            "success": True,
            "results": {
                "data": sorted_data,
                "shape": sorted_data.shape,
                "sort_columns": by if isinstance(by, list) else [by]
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


def filter_data(data: pd.DataFrame, condition: str) -> dict:
    """
    过滤数据
    
    Args:
        data: 原始数据
        condition: 过滤条件表达式（如 "age > 18 & score < 90"）
    
    Returns:
        过滤结果
    """
    try:
        # 执行过滤
        filtered = data.query(condition)
        
        return {
            "success": True,
            "results": {
                "data": filtered,
                "shape": filtered.shape,
                "condition": condition,
                "filtered_count": filtered.shape[0]
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


def aggregate_data(
    data: pd.DataFrame,
    group_by: Union[str, list],
    agg_func: dict
) -> dict:
    """
    聚合数据
    
    Args:
        data: 输入数据
        group_by: 分组变量
        agg_func: 聚合规则，如 {"score": ["mean", "std"]}
    
    Returns:
        聚合结果
    """
    try:
        # 执行聚合
        aggregated = data.groupby(group_by).agg(agg_func)
        
        return {
            "success": True,
            "results": {
                "data": aggregated,
                "shape": aggregated.shape,
                "group_by": group_by if isinstance(group_by, list) else [group_by],
                "aggregations": agg_func
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


def transpose_data(data: pd.DataFrame) -> dict:
    """
    转置数据
    
    Args:
        data: 输入数据
    
    Returns:
        转置结果
    """
    try:
        # 转置
        transposed = data.transpose()
        
        return {
            "success": True,
            "results": {
                "data": transposed,
                "original_shape": data.shape,
                "new_shape": transposed.shape
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


def reshape_wide(
    data: pd.DataFrame,
    id_var: str,
    time_var: str,
    var_name: str,
    value_name: str = "value"
) -> dict:
    """
    长格式转宽格式
    
    Args:
        data: 输入数据
        id_var: ID变量
        time_var: 时间变量
        var_name: 变量名
        value_name: 值列名
    
    Returns:
        转换结果
    """
    try:
        # 转换为宽格式
        wide = data.pivot(index=id_var, columns=time_var, values=var_name)
        wide.columns = [f"{var_name}_{col}" for col in wide.columns]
        wide.reset_index(inplace=True)
        
        return {
            "success": True,
            "results": {
                "data": wide,
                "shape": wide.shape,
                "id_var": id_var,
                "time_points": len(data[time_var].unique())
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


def reshape_long(
    data: pd.DataFrame,
    stubnames: list,
    id_var: str,
    j: str
) -> dict:
    """
    宽格式转长格式
    
    Args:
        data: 输入数据
        stubnames: 变量前缀列表
        id_var: ID变量
        j: 新变量名
    
    Returns:
        转换结果
    """
    try:
        # 转换为长格式
        long = pd.wide_to_long(data, stubnames=stubnames, i=id_var, j=j)
        long.reset_index(inplace=True)
        
        return {
            "success": True,
            "results": {
                "data": long,
                "shape": long.shape,
                "id_var": id_var,
                "j_values": long[j].unique().tolist()
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


def compute_variable(
    data: pd.DataFrame,
    expression: str,
    new_var: str
) -> dict:
    """
    计算新变量
    
    Args:
        data: 输入数据
        expression: 计算表达式（如 "log(income) + 1"）
        new_var: 新变量名
    
    Returns:
        计算结果
    """
    try:
        # 复制数据以避免修改原始数据
        result = data.copy()
        
        # 计算新变量
        result[new_var] = result.eval(expression)
        
        return {
            "success": True,
            "results": {
                "data": result,
                "new_var": new_var,
                "expression": expression
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


def recode_variable(
    data: pd.DataFrame,
    var: str,
    rules: dict,
    new_var: str = None
) -> dict:
    """
    重编码变量
    
    Args:
        data: 输入数据
        var: 原变量名
        rules: 重编码规则，如 {(0, 18): 1, (18, 60): 2, (60, 120): 3}
        new_var: 新变量名，None 则覆盖原变量
    
    Returns:
        重编码结果
    """
    try:
        # 复制数据以避免修改原始数据
        result = data.copy()
        
        # 确定目标变量名
        target_var = new_var if new_var is not None else var
        
        # 应用重编码规则
        def recode_value(x):
            for (lower, upper), value in rules.items():
                if lower <= x < upper:
                    return value
            return x
        
        result[target_var] = result[var].apply(recode_value)
        
        return {
            "success": True,
            "results": {
                "data": result,
                "var": var,
                "mapping": rules,
                "new_var": target_var
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


def detect_missing(data: pd.DataFrame) -> dict:
    """
    检测缺失值
    
    Args:
        data: 输入数据
    
    Returns:
        缺失值检测结果
    """
    try:
        # 计算缺失值
        missing_counts = data.isnull().sum().to_dict()
        missing_pct = (data.isnull().mean() * 100).to_dict()
        total_missing = data.isnull().sum().sum()
        total_cells = data.size
        missing_rate = total_missing / total_cells if total_cells > 0 else 0
        
        return {
            "success": True,
            "results": {
                "missing_counts": missing_counts,
                "missing_pct": missing_pct,
                "total_missing": total_missing,
                "total_cells": total_cells,
                "missing_rate": missing_rate
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


def weight_data(data: pd.DataFrame, weight_var: str) -> dict:
    """
    加权数据
    
    Args:
        data: 输入数据
        weight_var: 权重变量名
    
    Returns:
        加权结果
    """
    try:
        # 复制数据以避免修改原始数据
        result = data.copy()
        
        # 计算有效样本量和设计效应
        weights = result[weight_var]
        effective_n = (weights.sum())**2 / (weights**2).sum()
        design_effect = result.shape[0] / effective_n if effective_n > 0 else 1
        
        return {
            "success": True,
            "results": {
                "data": result,
                "weight_var": weight_var,
                "effective_n": effective_n,
                "design_effect": design_effect
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


def create_dataset(rows: int = 100, cols: int = 100) -> dict:
    """
    创建空数据集
    
    Args:
        rows: 行数
        cols: 列数
    
    Returns:
        创建的数据集
    """
    try:
        # 创建空DataFrame
        columns = [f"VAR{str(i+1).zfill(5)}" for i in range(cols)]
        data = pd.DataFrame(index=range(rows), columns=columns)
        
        return {
            "success": True,
            "results": {
                "data": data,
                "columns": columns,
                "shape": (rows, cols)
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

