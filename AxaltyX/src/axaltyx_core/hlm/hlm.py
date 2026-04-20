import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import stats

def hierarchical_linear_model(data: pd.DataFrame, dependent_var: str, level1_vars: list[str], level2_vars: list[str], group_var: str, random_intercept: bool = True, random_slope: list[str] = None) -> dict:
    try:
        # 检查变量是否存在
        for var in [dependent_var, group_var] + level1_vars + level2_vars:
            if var not in data.columns:
                raise ValueError(f"变量 {var} 不存在于数据中")
        
        # 准备数据
        groups = data[group_var].unique()
        n_groups = len(groups)
        n_obs = len(data)
        
        # 计算组内均值
        group_means = data.groupby(group_var)[level1_vars + level2_vars + [dependent_var]].mean().reset_index()
        group_means.columns = [group_var] + [f"{var}_mean" for var in level1_vars] + level2_vars + [f"{dependent_var}_mean"]
        
        # 合并组内均值到原始数据
        data_merged = data.merge(group_means, on=group_var, how='left')
        
        # 计算中心化变量
        for var in level1_vars:
            data_merged[f"{var}_centered"] = data_merged[var] - data_merged[f"{var}_mean"]
        
        # 第一阶段：组内回归
        level1_coefs = []
        level1_residuals = []
        
        for group in groups:
            group_data = data_merged[data_merged[group_var] == group]
            
            # 准备自变量（中心化的Level 1变量）
            X_level1 = group_data[[f"{var}_centered" for var in level1_vars]]
            X_level1['intercept'] = 1  # 添加截距
            y_level1 = group_data[dependent_var]
            
            # 拟合组内回归
            model = LinearRegression()
            model.fit(X_level1, y_level1)
            
            # 存储系数和残差
            coefs = {}
            coefs['intercept'] = model.intercept_
            for i, var in enumerate(level1_vars):
                coefs[var] = model.coef_[i]
            
            coefs[group_var] = group
            level1_coefs.append(coefs)
            
            # 计算残差
            residuals = y_level1 - model.predict(X_level1)
            level1_residuals.extend(residuals.tolist())
        
        # 转换为DataFrame
        level1_coefs_df = pd.DataFrame(level1_coefs)
        
        # 第二阶段：组间回归
        fixed_effects = {}
        random_effects = {}
        
        # 截距的组间回归
        if random_intercept:
            X_level2_intercept = group_means[level2_vars]
            X_level2_intercept['intercept'] = 1  # 添加截距
            y_level2_intercept = level1_coefs_df['intercept']
            
            model_intercept = LinearRegression()
            model_intercept.fit(X_level2_intercept, y_level2_intercept)
            
            # 固定效应
            fixed_effects['intercept'] = model_intercept.intercept_
            for i, var in enumerate(level2_vars):
                fixed_effects[f"intercept_{var}"] = model_intercept.coef_[i]
            
            # 随机效应（截距的残差）
            random_effects['intercept'] = (y_level2_intercept - model_intercept.predict(X_level2_intercept)).tolist()
        
        # 斜率的组间回归
        if random_slope:
            for var in random_slope:
                if var not in level1_vars:
                    raise ValueError(f"随机斜率变量 {var} 不在Level 1变量列表中")
                
                X_level2_slope = group_means[level2_vars]
                X_level2_slope['intercept'] = 1  # 添加截距
                y_level2_slope = level1_coefs_df[var]
                
                model_slope = LinearRegression()
                model_slope.fit(X_level2_slope, y_level2_slope)
                
                # 固定效应
                fixed_effects[f"{var}_slope"] = model_slope.intercept_
                for i, level2_var in enumerate(level2_vars):
                    fixed_effects[f"{var}_slope_{level2_var}"] = model_slope.coef_[i]
                
                # 随机效应（斜率的残差）
                random_effects[var] = (y_level2_slope - model_slope.predict(X_level2_slope)).tolist()
        
        # 计算方差成分
        level1_residuals = np.array(level1_residuals)
        var_level1 = np.var(level1_residuals)
        
        var_level2 = {}
        if random_intercept:
            var_level2['intercept'] = np.var(random_effects['intercept'])
        
        if random_slope:
            for var in random_slope:
                var_level2[var] = np.var(random_effects[var])
        
        # 计算ICC（组内相关系数）
        total_var = var_level1
        if random_intercept:
            total_var += var_level2['intercept']
        
        icc = var_level2.get('intercept', 0) / total_var if total_var > 0 else 0
        
        # 计算模型拟合指标
        # 简化版：使用组内回归的R平方
        level1_r2 = []
        for group in groups:
            group_data = data_merged[data_merged[group_var] == group]
            X_level1 = group_data[[f"{var}_centered" for var in level1_vars]]
            X_level1['intercept'] = 1
            y_level1 = group_data[dependent_var]
            
            model = LinearRegression()
            model.fit(X_level1, y_level1)
            r2 = model.score(X_level1, y_level1)
            level1_r2.append(r2)
        
        avg_r2 = np.mean(level1_r2)
        
        # 构建固定效应和随机效应的DataFrame
        fixed_effects_df = pd.DataFrame.from_dict(fixed_effects, orient='index', columns=['estimate'])
        
        random_effects_df = pd.DataFrame({
            group_var: groups,
            'intercept': random_effects.get('intercept', [0] * n_groups)
        })
        
        if random_slope:
            for var in random_slope:
                random_effects_df[var] = random_effects.get(var, [0] * n_groups)
        
        return {
            "success": True,
            "results": {
                "fixed_effects": fixed_effects_df,
                "random_effects": random_effects_df,
                "variance_components": {
                    "level1_residual": float(var_level1),
                    **{f"level2_{key}": float(value) for key, value in var_level2.items()}
                },
                "icc": float(icc),
                "model_fit": {
                    "aic": float(-2 * np.sum(np.log(1 - np.array(level1_r2))) + 2 * (len(fixed_effects) + len(var_level2))),
                    "bic": float(-2 * np.sum(np.log(1 - np.array(level1_r2))) + np.log(n_obs) * (len(fixed_effects) + len(var_level2))),
                    "log_likelihood": float(np.sum(np.log(1 - np.array(level1_r2)))),
                    "n_obs": n_obs,
                    "n_groups": n_groups
                },
                "reliability": {
                    "average_level1_r2": float(avg_r2)
                }
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
