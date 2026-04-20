import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, List, Optional


def cronbach_alpha(data: pd.DataFrame, vars: list[str]) -> dict:
    """
    克朗巴赫α系数
    
    Args:
        data: 输入数据
        vars: 变量列表
    
    Returns:
        克朗巴赫α系数结果
    """
    try:
        # 准备数据
        X = data[vars].dropna()
        n_items = len(vars)
        
        # 计算总分
        total_score = X.sum(axis=1)
        
        # 计算各项目的方差
        item_variances = X.var(axis=0, ddof=1)
        
        # 计算总分的方差
        total_variance = total_score.var(ddof=1)
        
        # 计算克朗巴赫α系数
        alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)
        
        # 计算标准化α系数
        X_scaled = StandardScaler().fit_transform(X)
        scaled_item_variances = np.var(X_scaled, axis=0, ddof=1)
        scaled_total_score = X_scaled.sum(axis=1)
        scaled_total_variance = np.var(scaled_total_score, ddof=1)
        standardized_alpha = (n_items / (n_items - 1)) * (1 - scaled_item_variances.sum() / scaled_total_variance)
        
        # 计算删除每个项目后的α系数
        alpha_if_deleted = {}
        item_total_correlations = {}
        
        for var in vars:
            # 删除当前项目
            remaining_vars = [v for v in vars if v != var]
            remaining_data = X[remaining_vars]
            remaining_total = remaining_data.sum(axis=1)
            
            # 计算删除后的α系数
            remaining_n = len(remaining_vars)
            remaining_item_variances = remaining_data.var(axis=0, ddof=1)
            remaining_total_variance = remaining_total.var(ddof=1)
            if remaining_total_variance > 0:
                alpha_if_deleted[var] = (remaining_n / (remaining_n - 1)) * (1 - remaining_item_variances.sum() / remaining_total_variance)
            else:
                alpha_if_deleted[var] = 0
            
            # 计算项目与总分的相关
            item_total_correlations[var] = X[var].corr(total_score - X[var])
        
        # 计算项目统计量
        item_statistics = pd.DataFrame({
            "Mean": X.mean(),
            "Variance": X.var(axis=0, ddof=1),
            "Item-Total Correlation": pd.Series(item_total_correlations),
            "Alpha if Deleted": pd.Series(alpha_if_deleted)
        })
        
        # 计算量表统计量
        scale_statistics = {
            "mean": total_score.mean(),
            "variance": total_variance,
            "std": np.sqrt(total_variance),
            "n": len(X)
        }
        
        # 构建结果
        results = {
            "alpha": alpha,
            "standardized_alpha": standardized_alpha,
            "n_items": n_items,
            "item_statistics": item_statistics,
            "item_total_correlations": item_total_correlations,
            "alpha_if_deleted": alpha_if_deleted,
            "scale_statistics": scale_statistics
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


def split_half_reliability(data: pd.DataFrame, vars: list[str]) -> dict:
    """
    分半信度
    
    Args:
        data: 输入数据
        vars: 变量列表
    
    Returns:
        分半信度结果
    """
    try:
        # 准备数据
        X = data[vars].dropna()
        n_items = len(vars)
        
        # 随机分为两半
        np.random.seed(42)
        half1_indices = np.random.choice(n_items, size=n_items//2, replace=False)
        half2_indices = [i for i in range(n_items) if i not in half1_indices]
        
        # 计算两半的得分
        half1 = X.iloc[:, half1_indices].sum(axis=1)
        half2 = X.iloc[:, half2_indices].sum(axis=1)
        
        # 计算两半的相关
        r_half = stats.pearsonr(half1, half2)[0]
        
        # 计算斯皮尔曼-布朗校正
        spearman_brown = 2 * r_half / (1 + r_half)
        
        # 计算古特曼分半信度
        guttman_split_half = 2 * (1 - (half1.var() + half2.var()) / X.sum(axis=1).var())
        
        # 构建结果
        results = {
            "spearman_brown": spearman_brown,
            "guttman_split_half": guttman_split_half,
            "r_half": r_half,
            "n_items": n_items
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


def test_retest_reliability(data: pd.DataFrame, var1: str, var2: str) -> dict:
    """
    重测信度
    
    Args:
        data: 输入数据
        var1: 第一次测量变量
        var2: 第二次测量变量
    
    Returns:
        重测信度结果
    """
    try:
        # 准备数据
        paired_data = data[[var1, var2]].dropna()
        
        # 计算皮尔逊相关
        pearson_r, p_value = stats.pearsonr(paired_data[var1], paired_data[var2])
        
        # 计算组内相关系数（ICC）
        def calculate_icc(data):
            # 简化处理，使用皮尔逊相关作为ICC的近似
            return pearson_r
        
        icc = calculate_icc(paired_data)
        
        # 计算置信区间
        # 简化处理，使用近似方法
        n = len(paired_data)
        t_value = stats.t.ppf(0.975, n-2)
        se = np.sqrt((1 - pearson_r**2) / (n-2))
        ci_lower = pearson_r - t_value * se
        ci_upper = pearson_r + t_value * se
        
        # 构建结果
        results = {
            "icc": icc,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "pearson_r": pearson_r,
            "p_value": p_value
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


def validity_analysis(
    data: pd.DataFrame,
    vars: list[str],
    construct_var: str = None
) -> dict:
    """
    效度分析
    
    Args:
        data: 输入数据
        vars: 变量列表
        construct_var: 构念变量（可选）
    
    Returns:
        效度分析结果
    """
    try:
        # 准备数据
        X = data[vars].dropna()
        
        # 内容效度（简化处理）
        content_validity = "Expert review required"
        
        # 效标效度（如果提供了构念变量）
        criterion_validity = None
        if construct_var:
            if construct_var in data.columns:
                criterion_scores = data.loc[X.index, construct_var]
                criterion_validity = X.corrwith(criterion_scores).mean()
        
        # 结构效度（使用因子分析）
        from sklearn.decomposition import FactorAnalysis
        fa = FactorAnalysis(n_components=1, random_state=42)
        fa.fit(X)
        factor_loadings = pd.DataFrame(fa.components_.T, index=vars, columns=["Factor 1"])
        
        # 收敛效度（平均方差提取）
        ave = np.mean(np.square(factor_loadings.values))
        
        # 区分效度（简化处理）
        discriminant_validity = "Requires multiple constructs"
        
        # 组合信度
        from scipy.stats import cronbach_alpha as scipy_cronbach
        cr = scipy_cronbach(X)[0]
        
        # 构建结果
        results = {
            "content_validity": content_validity,
            "criterion_validity": criterion_validity,
            "construct_validity": "Factor analysis completed",
            "convergent_validity": ave,
            "discriminant_validity": discriminant_validity,
            "factor_loadings": factor_loadings,
            "ave": ave,
            "cr": cr
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
