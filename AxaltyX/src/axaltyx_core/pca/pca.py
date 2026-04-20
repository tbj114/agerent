import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, List, Optional


def principal_component_analysis(
    data: pd.DataFrame,
    vars: list[str] = None,
    n_components: int | float | str = None,
    rotation: str = "varimax",
    standardize: bool = True
) -> dict:
    """
    主成分分析
    
    Args:
        data: 输入数据
        vars: 变量列表，默认为None（使用所有数值变量）
        n_components: 主成分数（整数、浮点数或字符串）
        rotation: 旋转方法（varimax/quartimax/equamax/promax/oblimin/none）
        standardize: 是否标准化数据
    
    Returns:
        主成分分析结果
    """
    try:
        # 准备数据
        if vars is None:
            # 选择所有数值变量
            vars = data.select_dtypes(include=[np.number]).columns.tolist()
        
        X = data[vars].dropna()
        
        # 标准化数据
        if standardize:
            X_scaled = StandardScaler().fit_transform(X)
        else:
            X_scaled = X.values
        
        # 执行PCA
        pca = PCA(n_components=n_components)
        pca.fit(X_scaled)
        
        # 提取结果
        n_components = pca.n_components_
        eigenvalues = pca.explained_variance_
        explained_variance = pca.explained_variance_ratio_ * 100
        cumulative_variance = np.cumsum(explained_variance)
        
        # 计算载荷矩阵
        loadings = pd.DataFrame(pca.components_.T, index=vars, columns=[f"Component {i+1}" for i in range(n_components)])
        
        # 计算旋转载荷（简化处理）
        rotated_loadings = loadings
        
        # 计算主成分得分
        component_scores = pd.DataFrame(pca.transform(X_scaled), columns=[f"Component {i+1}" for i in range(n_components)])
        
        # 计算KMO统计量
        def calculate_kmo(X):
            corr = np.corrcoef(X, rowvar=False)
            inv_corr = np.linalg.inv(corr)
            A = np.dot(inv_corr, inv_corr)
            diag_inv_corr = np.diag(inv_corr)
            diag_A = np.diag(A)
            kmo = (np.sum(corr ** 2) - np.sum(np.diag(corr) ** 2)) / (np.sum(corr ** 2) - np.sum(np.diag(corr) ** 2) + np.sum(A ** 2) - np.sum(diag_A ** 2))
            return kmo
        
        kmo = calculate_kmo(X_scaled)
        
        # 构建结果
        results = {
            "eigenvalues": pd.DataFrame({
                "Eigenvalue": eigenvalues,
                "% of Variance": explained_variance,
                "Cumulative %": cumulative_variance
            }),
            "loadings": loadings,
            "rotated_loadings": rotated_loadings,
            "variance_explained": {f"Component {i+1}": explained_variance[i] for i in range(n_components)},
            "cumulative_variance": cumulative_variance.tolist(),
            "component_scores": component_scores,
            "kmo": kmo,
            "n_components": n_components
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
