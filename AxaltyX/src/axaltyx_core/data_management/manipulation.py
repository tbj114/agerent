
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Union, Optional


def merge_datasets(
    left: pd.DataFrame,
    right: pd.DataFrame,
    on: Union[str, list],
    how: str = "inner"
) -> dict:
    """合并数据集"""
    try:
        merged = left.merge(right, on=on, how=how)
        
        return {
            "success": True,
            "results": {
                "data": merged,
                "shape": merged.shape,
                "merge_keys": on if isinstance(on, list) else [on],
                "merged_rows": len(merged)
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
    """排序数据"""
    try:
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
    """过滤数据"""
    try:
        filtered = data.query(condition)
        
        return {
            "success": True,
            "results": {
                "data": filtered,
                "shape": filtered.shape,
                "condition": condition,
                "filtered_count": len(filtered)
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
    """聚合数据"""
    try:
        aggregated = data.groupby(group_by).agg(agg_func).reset_index()
        
        return {
            "success": True,
            "results": {
                "data": aggregated,
                "shape": aggregated.shape,
                "group_by": group_by if isinstance(group_by, list) else [group_by],
                "aggregations": list(agg_func.keys())
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
    """转置数据"""
    try:
        transposed = data.transpose()
        original_shape = data.shape
        new_shape = transposed.shape
        
        return {
            "success": True,
            "results": {
                "data": transposed,
                "original_shape": original_shape,
                "new_shape": new_shape
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
    """宽表转换"""
    try:
        wide = data.pivot(index=id_var, columns=time_var, values=var_name)
        wide = wide.rename_axis(None, axis=1).reset_index()
        
        return {
            "success": True,
            "results": {
                "data": wide,
                "shape": wide.shape,
                "id_var": id_var,
                "time_points": list(data[time_var].unique())
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
    """长表转换"""
    try:
        long = pd.wide_to_long(data, stubnames=stubnames, i=id_var, j=j)
        long = long.reset_index()
        
        return {
            "success": True,
            "results": {
                "data": long,
                "shape": long.shape,
                "id_var": id_var,
                "j_values": list(long[j].unique())
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
    """计算新变量"""
    try:
        data[new_var] = data.eval(expression)
        
        return {
            "success": True,
            "results": {
                "data": data,
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
    """重编码变量"""
    try:
        target_var = new_var if new_var else var
        
        # 创建映射函数
        def recode(value):
            for (min_val, max_val), new_val in rules.items():
                if min_val <= value <= max_val:
                    return new_val
            return value
        
        data[target_var] = data[var].apply(recode)
        
        return {
            "success": True,
            "results": {
                "data": data,
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
    """检测缺失值"""
    try:
        missing_counts = data.isnull().sum().to_dict()
        missing_pct = (data.isnull().sum() / len(data) * 100).round(2).to_dict()
        total_missing = data.isnull().sum().sum()
        total_cells = data.size
        missing_rate = (total_missing / total_cells) * 100 if total_cells > 0 else 0
        
        return {
            "success": True,
            "results": {
                "missing_counts": missing_counts,
                "missing_pct": missing_pct,
                "total_missing": total_missing,
                "total_cells": total_cells,
                "missing_rate": round(missing_rate, 2)
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
    """加权数据"""
    try:
        effective_n = data[weight_var].sum()
        design_effect = len(data) / effective_n if effective_n > 0 else 1
        
        return {
            "success": True,
            "results": {
                "data": data,
                "weight_var": weight_var,
                "effective_n": effective_n,
                "design_effect": round(design_effect, 4)
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
    """创建空数据集"""
    try:
        # 创建列名 VAR00001 ~ VAR00100
        columns = [f"VAR{str(i+1).zfill(5)}" for i in range(cols)]
        # 创建空 DataFrame
        data = pd.DataFrame(index=range(rows), columns=columns)
        # 填充 NaN
        data = data.fillna(np.nan)
        
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
