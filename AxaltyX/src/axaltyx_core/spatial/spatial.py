import pandas as pd
import numpy as np
from scipy import stats

def moran_i(data: pd.DataFrame, var: str, weights_matrix: np.ndarray) -> dict:
    try:
        # 检查变量是否存在
        if var not in data.columns:
            raise ValueError(f"变量 {var} 不存在于数据中")
        
        # 检查权重矩阵维度
        n = len(data)
        if weights_matrix.shape != (n, n):
            raise ValueError(f"权重矩阵维度 ({weights_matrix.shape}) 与数据长度 ({n}) 不匹配")
        
        # 提取变量值
        x = data[var].values
        
        # 计算均值
        x_mean = np.mean(x)
        
        # 计算偏差
        x_dev = x - x_mean
        
        # 计算权重矩阵的行和
        weights_sum = np.sum(weights_matrix)
        
        # 计算分子
        numerator = np.sum(weights_matrix * np.outer(x_dev, x_dev))
        
        # 计算分母
        denominator = np.sum(x_dev ** 2)
        
        # 计算Moran's I
        if denominator > 0:
            moran_i = (n / weights_sum) * (numerator / denominator)
        else:
            moran_i = 0
        
        # 计算期望Moran's I
        expected_i = -1 / (n - 1)
        
        # 计算方差
        # 简化版方差计算
        s1 = 0.5 * np.sum((weights_matrix + weights_matrix.T) ** 2)
        s2 = np.sum((np.sum(weights_matrix, axis=1) + np.sum(weights_matrix, axis=0)) ** 2)
        
        k = (np.sum(x_dev ** 4) / n) / (np.sum(x_dev ** 2) / n) ** 2
        
        variance = ((n ** 2 * s1 - n * s2 + 3 * weights_sum ** 2) / (weights_sum ** 2 * (n ** 2 - 1)))
        variance -= (k * (n ** 2 * s1 - 2 * n * s2 + 6 * weights_sum ** 2)) / (weights_sum ** 2 * (n ** 2 - 1))
        
        # 计算Z得分
        if variance > 0:
            z_score = (moran_i - expected_i) / np.sqrt(variance)
        else:
            z_score = 0
        
        # 计算p值
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        
        # 简单的置换检验
        n_permutations = 999
        permuted_moran = []
        
        for _ in range(n_permutations):
            x_permuted = np.random.permutation(x)
            x_permuted_dev = x_permuted - np.mean(x_permuted)
            numerator_permuted = np.sum(weights_matrix * np.outer(x_permuted_dev, x_permuted_dev))
            denominator_permuted = np.sum(x_permuted_dev ** 2)
            
            if denominator_permuted > 0:
                moran_permuted = (n / weights_sum) * (numerator_permuted / denominator_permuted)
                permuted_moran.append(moran_permuted)
        
        # 计算置换检验的p值
        if permuted_moran:
            permutation_p = (np.sum(np.abs(permuted_moran) >= np.abs(moran_i)) + 1) / (n_permutations + 1)
        else:
            permutation_p = 1.0
        
        return {
            "success": True,
            "results": {
                "moran_i": float(moran_i),
                "expected_i": float(expected_i),
                "variance": float(variance),
                "z_score": float(z_score),
                "p_value": float(p_value),
                "permutation_p": float(permutation_p)
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
