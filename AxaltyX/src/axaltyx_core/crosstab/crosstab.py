import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List, Optional


def crosstabs(
    data: pd.DataFrame,
    row_var: str,
    col_var: str,
    layer_var: str = None,
    statistics: list[str] = None
) -> dict:
    """
    交叉表分析
    
    Args:
        data: 输入数据
        row_var: 行变量
        col_var: 列变量
        layer_var: 分层变量
        statistics: 统计量（chi2/phi/cramer_v/lambda/uncertainty/contingency/gamma/kappa/risk/odds_ratio）
    
    Returns:
        交叉表分析结果
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
        if layer_var:
            # 分层分析
            layers = data[layer_var].unique()
            tables = {}
            for layer in layers:
                layer_data = data[data[layer_var] == layer]
                layer_col_data = eval(col_var, {}, {col: layer_data[col] for col in layer_data.columns}) if '>' in col_var or '<' in col_var or '==' in col_var else layer_data[col_var]
                table = pd.crosstab(layer_data[row_var], layer_col_data)
                tables[layer] = table
            # 使用第一个层的数据进行统计计算
            table = tables[layers[0]]
        else:
            # 普通交叉表
            table = pd.crosstab(data[row_var], col_data)
        
        # 计算基本统计量
        chi2, p_value, df, expected = stats.chi2_contingency(table)
        
        # 计算百分比
        row_totals = table.sum(axis=1)
        col_totals = table.sum(axis=0)
        total = table.sum().sum()
        
        row_pct = table.div(row_totals, axis=0) * 100
        col_pct = table.div(col_totals, axis=1) * 100
        total_pct = table.div(total) * 100
        
        percentages = {
            'row': row_pct,
            'column': col_pct,
            'total': total_pct
        }
        
        # 计算其他统计量
        results = {
            "table": table,
            "expected": pd.DataFrame(expected, index=table.index, columns=table.columns),
            "percentages": percentages,
            "chi2": {"value": chi2, "df": df, "p": p_value}
        }
        
        # 计算phi系数（适用于2x2表）
        if table.shape == (2, 2):
            phi = np.sqrt(chi2 / total)
            results["phi"] = phi
            
            # 计算优势比
            if table.iloc[0, 0] * table.iloc[1, 1] != 0 and table.iloc[0, 1] * table.iloc[1, 0] != 0:
                odds_ratio = (table.iloc[0, 0] * table.iloc[1, 1]) / (table.iloc[0, 1] * table.iloc[1, 0])
                # 计算优势比的置信区间
                import math
                se_log_or = math.sqrt(1/table.iloc[0, 0] + 1/table.iloc[0, 1] + 1/table.iloc[1, 0] + 1/table.iloc[1, 1])
                ci_lower = math.exp(math.log(odds_ratio) - 1.96 * se_log_or)
                ci_upper = math.exp(math.log(odds_ratio) + 1.96 * se_log_or)
                results["odds_ratio"] = {"value": odds_ratio, "ci_lower": ci_lower, "ci_upper": ci_upper}
        
        # 计算Cramer's V
        min_dim = min(table.shape)
        cramer_v = np.sqrt(chi2 / (total * (min_dim - 1)))
        results["cramer_v"] = cramer_v
        
        # 计算列联系数
        contingency_coefficient = np.sqrt(chi2 / (chi2 + total))
        results["contingency_coefficient"] = contingency_coefficient
        
        # 计算Lambda
        # 对称Lambda
        max_row = table.max(axis=1).sum()
        max_col = table.max(axis=0).sum()
        lambda_sym = (max_row + max_col - (max(table.sum(axis=1)) + max(table.sum(axis=0)))) / (2 * total - (max(table.sum(axis=1)) + max(table.sum(axis=0))))
        # 行到列Lambda
        lambda_row = (max_row - max(table.sum(axis=1))) / (total - max(table.sum(axis=1)))
        # 列到行Lambda
        lambda_col = (max_col - max(table.sum(axis=0))) / (total - max(table.sum(axis=0)))
        results["lambda"] = {"symmetric": lambda_sym, "row": lambda_row, "col": lambda_col}
        
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


def chi_square_test(
    data: pd.DataFrame,
    row_var: str,
    col_var: str
) -> dict:
    """
    卡方检验
    
    Args:
        data: 输入数据
        row_var: 行变量
        col_var: 列变量
    
    Returns:
        卡方检验结果
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
        
        # 计算卡方检验
        chi2, p_value, df, expected = stats.chi2_contingency(table)
        
        # 计算残差
        observed = table.values
        residuals = observed - expected
        standardized_residuals = residuals / np.sqrt(expected)
        
        # 计算统计量
        cells = observed.size
        min_expected = expected.min()
        warning_small_expected = min_expected < 5
        
        return {
            "success": True,
            "results": {
                "chi2": chi2,
                "df": df,
                "p_value": p_value,
                "expected": pd.DataFrame(expected, index=table.index, columns=table.columns),
                "residuals": pd.DataFrame(residuals, index=table.index, columns=table.columns),
                "standardized_residuals": pd.DataFrame(standardized_residuals, index=table.index, columns=table.columns),
                "cells": cells,
                "min_expected": min_expected,
                "warning_small_expected": warning_small_expected
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


def mcnemar_test(data: pd.DataFrame, var1: str, var2: str, exact: bool = False) -> dict:
    """
    McNemar检验
    
    Args:
        data: 输入数据
        var1: 第一个变量
        var2: 第二个变量
        exact: 是否使用精确检验
    
    Returns:
        McNemar检验结果
    """
    try:
        # 创建列联表
        table = pd.crosstab(data[var1], data[var2])
        
        # 确保是2x2表
        if table.shape != (2, 2):
            raise ValueError("McNemar test requires 2x2 contingency table")
        
        # 提取b和c值（不一致的单元格）
        b = table.iloc[0, 1]
        c = table.iloc[1, 0]
        
        # 计算检验统计量
        if exact:
            # 精确检验（二项分布）
            from scipy.stats import binom
            n = b + c
            p_value = 2 * binom.cdf(min(b, c), n, 0.5)
            statistic = min(b, c)
        else:
            # 卡方近似
            if b + c == 0:
                chi2 = 0
                p_value = 1.0
            else:
                chi2 = (abs(b - c) - 1)**2 / (b + c)
                p_value = stats.chi2.sf(chi2, 1)
            statistic = chi2
        
        # 计算不一致对数
        n_discordant = b + c
        
        return {
            "success": True,
            "results": {
                "statistic": statistic,
                "p_value": p_value,
                "table": table,
                "n_discordant": n_discordant
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


def cochran_q_test(data: pd.DataFrame, vars: list[str]) -> dict:
    """
    Cochran Q检验
    
    Args:
        data: 输入数据
        vars: 变量列表（多个相关的二分类变量）
    
    Returns:
        Cochran Q检验结果
    """
    try:
        # 确保所有变量都是二分类的
        for var in vars:
            unique_vals = data[var].dropna().unique()
            if len(unique_vals) > 2:
                raise ValueError(f"Variable {var} is not binary")
        
        # 将数据转换为0和1
        binary_data = data[vars].copy()
        for var in vars:
            binary_data[var] = binary_data[var].astype(bool).astype(int)
        
        # 计算统计量
        n = len(binary_data)
        k = len(vars)
        
        # 每行的和（每个被试的阳性数）
        row_sums = binary_data.sum(axis=1)
        # 每列的和（每个变量的阳性数）
        col_sums = binary_data.sum(axis=0)
        
        # 计算Q统计量
        total = col_sums.sum()
        Q = (k * (k - 1) * (col_sums.pow(2).sum() - (total ** 2) / k)) / ((k * total) - row_sums.pow(2).sum())
        
        # 计算p值
        df = k - 1
        p_value = stats.chi2.sf(Q, df)
        
        # 计算Kendall's W
        W = Q / (k * (n - 1)) if n > 1 else 0
        
        return {
            "success": True,
            "results": {
                "q_statistic": Q,
                "df": df,
                "p_value": p_value,
                "n": n,
                "k": k,
                "table": binary_data,
                "kendall_w": W
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
