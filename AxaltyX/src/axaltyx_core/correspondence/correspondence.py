import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from scipy.stats import chi2_contingency
from typing import Dict, Any, List, Optional


def simple_correspondence(
    data: pd.DataFrame,
    row_var: str,
    col_var: str,
    n_dimensions: int = 2,
    standardization: str = "principal"
) -> dict:
    """
    简单对应分析
    
    Args:
        data: 输入数据
        row_var: 行变量
        col_var: 列变量
        n_dimensions: 维度数
        standardization: 标准化方法（principal/burt）
    
    Returns:
        简单对应分析结果
    """
    try:
        # 计算列联表
        contingency_table = pd.crosstab(data[row_var], data[col_var])
        
        # 计算总频数
        total = contingency_table.sum().sum()
        
        # 计算行和列的边缘概率
        row_margins = contingency_table.sum(axis=1) / total
        col_margins = contingency_table.sum(axis=0) / total
        
        # 计算期望频数
        expected = np.outer(row_margins, col_margins) * total
        
        # 计算卡方统计量
        chi2_stat, p_value, _, _ = chi2_contingency(contingency_table)
        
        # 计算残差矩阵
        residuals = (contingency_table - expected) / np.sqrt(expected)
        
        # 计算惯性
        inertia = np.sum(residuals.values ** 2) / total
        
        # 标准化残差矩阵
        standardized_residuals = residuals / np.sqrt(np.outer(row_margins, col_margins))
        
        # 使用PCA进行维度约简
        pca = PCA(n_components=n_dimensions)
        row_scores = pca.fit_transform(standardized_residuals)
        col_scores = pca.transform(standardized_residuals.T)
        
        # 计算奇异值
        singular_values = pca.singular_values_
        
        # 构建结果
        row_scores_df = pd.DataFrame(
            row_scores,
            index=contingency_table.index,
            columns=[f"Dim {i+1}" for i in range(n_dimensions)]
        )
        
        col_scores_df = pd.DataFrame(
            col_scores,
            index=contingency_table.columns,
            columns=[f"Dim {i+1}" for i in range(n_dimensions)]
        )
        
        # 计算行和列的轮廓
        row_profiles = contingency_table.div(contingency_table.sum(axis=1), axis=0)
        col_profiles = contingency_table.div(contingency_table.sum(axis=0), axis=1)
        
        # 构建绘图数据
        plot_data = {
            "row_scores": row_scores.tolist(),
            "col_scores": col_scores.tolist(),
            "row_labels": contingency_table.index.tolist(),
            "col_labels": contingency_table.columns.tolist()
        }
        
        results = {
            "row_scores": row_scores_df,
            "col_scores": col_scores_df,
            "singular_values": singular_values.tolist(),
            "inertia": inertia,
            "chi2": chi2_stat,
            "row_profiles": row_profiles,
            "col_profiles": col_profiles,
            "plot_data": plot_data
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


def multiple_correspondence(
    data: pd.DataFrame,
    vars: list[str],
    n_dimensions: int = 2
) -> dict:
    """
    多重对应分析
    
    Args:
        data: 输入数据
        vars: 变量列表
        n_dimensions: 维度数
    
    Returns:
        多重对应分析结果
    """
    try:
        # 对每个变量进行独热编码
        dummies = []
        variable_names = []
        
        for var in vars:
            dummy = pd.get_dummies(data[var], prefix=var, drop_first=True)
            dummies.append(dummy)
            variable_names.extend(dummy.columns.tolist())
        
        # 合并独热编码后的变量
        X = pd.concat(dummies, axis=1)
        
        # 计算 Burt矩阵
        burt_matrix = X.T @ X
        
        # 计算总惯性
        total_inertia = np.trace(burt_matrix) / len(X)
        
        # 使用PCA进行维度约简
        pca = PCA(n_components=n_dimensions)
        category_scores = pca.fit_transform(X)
        
        # 计算特征值
        eigenvalues = pca.explained_variance_
        
        # 计算贡献率
        contribution = pca.explained_variance_ratio_ * 100
        
        # 构建结果
        category_scores_df = pd.DataFrame(
            category_scores,
            index=data.index,
            columns=[f"Dim {i+1}" for i in range(n_dimensions)]
        )
        
        # 构建绘图数据
        plot_data = {
            "category_scores": category_scores.tolist(),
            "labels": data.index.tolist()
        }
        
        results = {
            "category_scores": category_scores_df,
            "inertia": total_inertia,
            "eigenvalues": eigenvalues.tolist(),
            "contribution": contribution.tolist(),
            "plot_data": plot_data
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
