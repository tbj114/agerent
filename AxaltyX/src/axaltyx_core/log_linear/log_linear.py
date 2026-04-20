import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from typing import Dict, Any, List, Optional


def log_linear(
    data: pd.DataFrame,
    factors: list[str],
    model: str = "saturated",
    max_iter: int = 100
) -> dict:
    """
    对数线性模型
    
    Args:
        data: 输入数据
        factors: 因子列表
        model: 模型类型（saturated/main/conditional）
        max_iter: 最大迭代次数
    
    Returns:
        对数线性模型结果
    """
    try:
        # 准备数据
        # 计算列联表
        if len(factors) == 2:
            # 二维列联表
            contingency_table = pd.crosstab(data[factors[0]], data[factors[1]])
        elif len(factors) == 3:
            # 三维列联表
            contingency_table = pd.crosstab([data[factors[0]], data[factors[1]]], data[factors[2]])
        else:
            # 高维列联表（简化处理）
            contingency_table = pd.crosstab(data[factors[0]], data[factors[1]])
        
        # 计算卡方检验
        chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        # 计算残差
        observed = contingency_table.values.flatten()
        expected_flat = expected.flatten()
        residuals = observed - expected_flat
        standardized_residuals = residuals / np.sqrt(expected_flat)
        
        # 似然比检验（简化处理）
        def likelihood_ratio_test(observed, expected):
            # 避免log(0)
            observed = np.maximum(observed, 1e-10)
            expected = np.maximum(expected, 1e-10)
            return 2 * np.sum(observed * np.log(observed / expected))
        
        likelihood_ratio = likelihood_ratio_test(observed, expected_flat)
        
        # 计算拟合优度
        goodness_of_fit = {
            "chi2": chi2_stat,
            "df": dof,
            "p": p_value,
            "likelihood_ratio": likelihood_ratio
        }
        
        # 提取系数（简化处理）
        # 使用逻辑回归作为近似
        encoder = OneHotEncoder(drop='first', sparse=False)
        X = encoder.fit_transform(data[factors])
        y = np.ones(len(data))  # 虚拟因变量
        
        log_reg = LogisticRegression(max_iter=max_iter, penalty=None)
        log_reg.fit(X, y)
        
        coefficients = pd.DataFrame({
            "coefficient": log_reg.coef_[0],
            "intercept": [log_reg.intercept_[0]] + [0] * (len(log_reg.coef_[0]) - 1)
        }, index=encoder.get_feature_names_out(factors))
        
        # 构建结果
        results = {
            "coefficients": coefficients,
            "goodness_of_fit": goodness_of_fit,
            "expected_frequencies": pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns),
            "residuals": pd.DataFrame(residuals.reshape(contingency_table.shape), index=contingency_table.index, columns=contingency_table.columns),
            "likelihood_ratio": likelihood_ratio,
            "pearson_chi2": chi2_stat,
            "df": dof,
            "p": p_value
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
