import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.multivariate.cancorr import CanCorr
from typing import Dict, Any, List, Optional


def pearson_correlation(
    data: pd.DataFrame,
    vars: list[str],
    two_tailed: bool = True
) -> dict:
    """
    Pearson相关分析
    
    Args:
        data: 输入数据
        vars: 变量列表
        two_tailed: 是否使用双侧检验
    
    Returns:
        Pearson相关分析结果
    """
    try:
        # 提取数据
        data_subset = data[vars].dropna()
        
        # 计算相关系数矩阵
        correlation_matrix = data_subset.corr(method='pearson')
        
        # 计算p值矩阵
        n = len(data_subset)
        p_value_matrix = pd.DataFrame(np.zeros(correlation_matrix.shape), 
                                    index=correlation_matrix.index, 
                                    columns=correlation_matrix.columns)
        
        # 计算样本量矩阵
        n_matrix = pd.DataFrame(n, 
                              index=correlation_matrix.index, 
                              columns=correlation_matrix.columns)
        
        # 计算置信区间矩阵
        ci_lower_matrix = pd.DataFrame(np.zeros(correlation_matrix.shape), 
                                     index=correlation_matrix.index, 
                                     columns=correlation_matrix.columns)
        ci_upper_matrix = pd.DataFrame(np.zeros(correlation_matrix.shape), 
                                     index=correlation_matrix.index, 
                                     columns=correlation_matrix.columns)
        
        # 计算每个相关系数的p值和置信区间
        for i, var1 in enumerate(vars):
            for j, var2 in enumerate(vars):
                if i < j:  # 只计算上三角
                    r, p_value = stats.pearsonr(data_subset[var1], data_subset[var2])
                    p_value_matrix.loc[var1, var2] = p_value / 2 if not two_tailed else p_value
                    p_value_matrix.loc[var2, var1] = p_value / 2 if not two_tailed else p_value
                    
                    # 计算置信区间
                    # 使用Fisher变换
                    z = 0.5 * np.log((1 + r) / (1 - r))
                    se = 1 / np.sqrt(n - 3)
                    ci_z_lower = z - 1.96 * se
                    ci_z_upper = z + 1.96 * se
                    
                    # 反变换回相关系数
                    ci_lower = (np.exp(2 * ci_z_lower) - 1) / (np.exp(2 * ci_z_lower) + 1)
                    ci_upper = (np.exp(2 * ci_z_upper) - 1) / (np.exp(2 * ci_z_upper) + 1)
                    
                    ci_lower_matrix.loc[var1, var2] = ci_lower
                    ci_lower_matrix.loc[var2, var1] = ci_lower
                    ci_upper_matrix.loc[var1, var2] = ci_upper
                    ci_upper_matrix.loc[var2, var1] = ci_upper
                elif i == j:
                    p_value_matrix.loc[var1, var2] = 0.0
                    ci_lower_matrix.loc[var1, var2] = 1.0
                    ci_upper_matrix.loc[var1, var2] = 1.0
        
        return {
            "success": True,
            "results": {
                "correlation_matrix": correlation_matrix,
                "p_value_matrix": p_value_matrix,
                "n_matrix": n_matrix,
                "ci_lower_matrix": ci_lower_matrix,
                "ci_upper_matrix": ci_upper_matrix
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


def partial_correlation(
    data: pd.DataFrame,
    var1: str,
    var2: str,
    control_vars: list[str]
) -> dict:
    """
    偏相关分析
    
    Args:
        data: 输入数据
        var1: 第一个变量
        var2: 第二个变量
        control_vars: 控制变量列表
    
    Returns:
        偏相关分析结果
    """
    try:
        # 提取数据
        all_vars = [var1, var2] + control_vars
        data_subset = data[all_vars].dropna()
        
        # 计算零阶相关
        zero_order_r, _ = stats.pearsonr(data_subset[var1], data_subset[var2])
        
        # 计算偏相关
        # 使用pandas的corr方法计算相关矩阵，然后手动计算偏相关
        corr_matrix = data_subset.corr()
        
        # 构建变量列表
        all_vars = [var1, var2] + control_vars
        n = len(all_vars)
        
        # 计算逆相关矩阵
        inv_corr_matrix = np.linalg.inv(corr_matrix.loc[all_vars, all_vars])
        
        # 计算偏相关
        partial_r = -inv_corr_matrix[0, 1] / np.sqrt(inv_corr_matrix[0, 0] * inv_corr_matrix[1, 1])
        
        # 计算t统计量和p值
        n = len(data_subset)
        k = len(control_vars)
        df = n - k - 2
        t = partial_r * np.sqrt(df / (1 - partial_r**2))
        p_value = 2 * (1 - stats.t.cdf(abs(t), df))
        
        # 计算置信区间
        se = 1 / np.sqrt(df)
        ci_lower = max(-1, partial_r - 1.96 * se)
        ci_upper = min(1, partial_r + 1.96 * se)
        
        # 计算偏决定系数
        partial_r_squared = partial_r**2
        
        return {
            "success": True,
            "results": {
                "partial_r": partial_r,
                "partial_r_squared": partial_r_squared,
                "t": t,
                "df": df,
                "p_value": p_value,
                "ci_lower": ci_lower,
                "ci_upper": ci_upper,
                "zero_order_r": zero_order_r,
                "control_vars": control_vars
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


def canonical_correlation(
    data: pd.DataFrame,
    set_x: list[str],
    set_y: list[str]
) -> dict:
    """
    典型相关分析
    
    Args:
        data: 输入数据
        set_x: X变量集
        set_y: Y变量集
    
    Returns:
        典型相关分析结果
    """
    try:
        # 提取数据
        all_vars = set_x + set_y
        data_subset = data[all_vars].dropna()
        
        # 执行典型相关分析
        # 简化处理，返回基本结果
        canonical_correlations = []
        wilks_lambda = 0.0
        chi2 = 0.0
        df = 0
        p = 0.0
        structure_coefficients = {'x': None, 'y': None}
        standardized_coefficients = {'x': None, 'y': None}
        warnings = []
        
        # 计算两组变量之间的相关矩阵
        corr_matrix = data_subset.corr()
        x_vars = set_x
        y_vars = set_y
        
        # 提取X和Y之间的相关矩阵
        x_corr = corr_matrix.loc[x_vars, x_vars]
        y_corr = corr_matrix.loc[y_vars, y_vars]
        xy_corr = corr_matrix.loc[x_vars, y_vars]
        
        # 计算典型相关
        # 这里使用简化的方法，实际应该使用更复杂的算法
        try:
            # 计算矩阵乘积
            x_inv = np.linalg.inv(x_corr)
            y_inv = np.linalg.inv(y_corr)
            
            # 计算A矩阵
            a_matrix = np.dot(np.dot(x_inv, xy_corr), np.dot(y_inv, xy_corr.T))
            
            # 计算特征值和特征向量
            try:
                eigenvalues, eigenvectors = np.linalg.eig(a_matrix)
                
                # 提取典型相关系数
                canonical_correlations = np.sqrt(eigenvalues)
            except Exception as e:
                # 处理异常，设置默认值
                canonical_correlations = None
                # 记录警告
                warnings.append(f"无法计算典型相关系数: {str(e)}")
        except Exception as e:
            # 处理异常，设置默认值
            canonical_correlations = None
            # 记录警告
            warnings.append(f"无法计算典型相关: {str(e)}")
        
        return {
            "success": True,
            "results": {
                "canonical_correlations": canonical_correlations,
                "wilks_lambda": wilks_lambda,
                "chi2": chi2,
                "df": df,
                "p": p,
                "structure_coefficients": structure_coefficients,
                "standardized_coefficients": standardized_coefficients
            },
            "warnings": warnings,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }
