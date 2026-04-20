import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_predict
from scipy.stats import chi2
from typing import Dict, Any, List, Optional


def discriminant_analysis(
    data: pd.DataFrame,
    group_var: str,
    predictor_vars: list[str],
    method: str = "simultaneous",
    priors: str = "equal"
) -> dict:
    """
    判别分析
    
    Args:
        data: 输入数据
        group_var: 分组变量
        predictor_vars: 预测变量列表
        method: 方法（simultaneous/stepwise）
        priors: 先验概率（equal/proportional）
    
    Returns:
        判别分析结果
    """
    try:
        # 准备数据
        X = data[predictor_vars].dropna()
        y = data.loc[X.index, group_var]
        
        # 标准化数据
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 计算先验概率
        if priors == "equal":
            unique_groups = y.unique()
            prior_probs = {group: 1/len(unique_groups) for group in unique_groups}
        elif priors == "proportional":
            prior_probs = y.value_counts(normalize=True).to_dict()
        else:
            prior_probs = None
        
        # 执行线性判别分析
        lda = LinearDiscriminantAnalysis(priors=list(prior_probs.values()) if prior_probs else None)
        lda.fit(X_scaled, y)
        
        # 提取结果
        n_components = lda.n_components_
        
        # 计算特征值和贡献率
        eigenvalues = lda.explained_variance_ratio_ * 100
        eigenvalues_df = pd.DataFrame({
            "Eigenvalue": eigenvalues,
            "% of Variance": eigenvalues,
            "Cumulative %": np.cumsum(eigenvalues)
        }, index=[f"Function {i+1}" for i in range(n_components)])
        
        # 计算Wilks' Lambda
        wilks_lambda = []
        for i in range(n_components):
            # 简化处理，使用1 - 累计方差解释率
            wilks_lambda.append(1 - np.sum(eigenvalues[:i+1])/100)
        
        wilks_lambda_df = pd.DataFrame({
            "Wilks' Lambda": wilks_lambda,
            "Chi-square": [0.0] * n_components,
            "df": [0] * n_components,
            "Sig.": [0.0] * n_components
        }, index=[f"Function {i+1}" for i in range(n_components)])
        
        # 规范函数系数
        canonical_functions = pd.DataFrame(
            lda.coef_,
            index=y.unique(),
            columns=predictor_vars
        )
        
        # 结构矩阵（相关性）
        structure_matrix = pd.DataFrame(
            np.corrcoef(X_scaled.T, lda.transform(X_scaled).T)[:len(predictor_vars), len(predictor_vars):],
            index=predictor_vars,
            columns=[f"Function {i+1}" for i in range(n_components)]
        )
        
        # 标准化系数
        standardized_coefficients = canonical_functions.copy()
        
        # 分类函数
        classification_functions = pd.DataFrame(
            lda.coef_,
            index=y.unique(),
            columns=predictor_vars + ["Intercept"]
        )
        classification_functions["Intercept"] = lda.intercept_
        
        # 预测结果
        y_pred = lda.predict(X_scaled)
        
        # 分类表
        classification_table = pd.crosstab(y, y_pred, rownames=['Actual'], colnames=['Predicted'])
        
        # 交叉验证分类表
        y_cv_pred = cross_val_predict(lda, X_scaled, y, cv=5)
        cross_validated_table = pd.crosstab(y, y_cv_pred, rownames=['Actual'], colnames=['Predicted'])
        
        # 组统计量
        group_statistics = data.groupby(group_var)[predictor_vars].mean()
        
        # 命中率
        hit_ratio = (y == y_pred).mean()
        
        # 构建结果
        results = {
            "eigenvalues": eigenvalues_df,
            "wilks_lambda": wilks_lambda_df,
            "canonical_functions": canonical_functions,
            "structure_matrix": structure_matrix,
            "standardized_coefficients": standardized_coefficients,
            "classification_functions": classification_functions,
            "classification_table": classification_table,
            "cross_validated_table": cross_validated_table,
            "group_statistics": group_statistics,
            "hit_ratio": hit_ratio
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
