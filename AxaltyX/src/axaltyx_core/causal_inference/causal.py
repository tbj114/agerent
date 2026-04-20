import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression, QuantileRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from scipy import stats

def propensity_score_matching(data: pd.DataFrame, treatment_var: str, outcome_var: str, covariates: list[str], method: str = "nearest", caliper: float = 0.2, ratio: int = 1) -> dict:
    try:
        # 检查变量是否存在
        for var in [treatment_var, outcome_var] + covariates:
            if var not in data.columns:
                raise ValueError(f"变量 {var} 不存在于数据中")
        
        # 准备数据
        X = data[covariates]
        y = data[treatment_var]
        
        # 训练逻辑回归模型估计倾向得分
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = LogisticRegression(random_state=42)
        model.fit(X_scaled, y)
        
        # 计算倾向得分
        propensity_scores = model.predict_proba(X_scaled)[:, 1]
        data['propensity_score'] = propensity_scores
        
        # 匹配处理
        treated = data[data[treatment_var] == 1]
        control = data[data[treatment_var] == 0]
        
        matched_indices = []
        for i, treated_row in treated.iterrows():
            treated_score = treated_row['propensity_score']
            
            # 计算与所有控制组的距离
            control['distance'] = abs(control['propensity_score'] - treated_score)
            
            # 应用卡尺
            valid_controls = control[control['distance'] <= caliper]
            
            if len(valid_controls) > 0:
                # 选择最近的控制组
                if method == "nearest":
                    selected = valid_controls.nsmallest(ratio, 'distance')
                    matched_indices.extend(selected.index.tolist())
        
        # 构建匹配数据集
        matched_control = data.loc[matched_indices]
        matched_data = pd.concat([treated, matched_control])
        
        # 计算平衡表
        balance_table = []
        for covar in covariates:
            treated_mean = treated[covar].mean()
            control_mean = matched_control[covar].mean()
            std_diff = (treated_mean - control_mean) / np.sqrt((treated[covar].var() + matched_control[covar].var()) / 2)
            balance_table.append({
                'variable': covar,
                'treated_mean': treated_mean,
                'control_mean': control_mean,
                'standardized_difference': abs(std_diff)
            })
        balance_table = pd.DataFrame(balance_table)
        
        # 计算处理效应
        ate = matched_data.groupby(treatment_var)[outcome_var].mean().diff().iloc[-1]
        att = treated[outcome_var].mean() - matched_control[outcome_var].mean()
        atc = (matched_data[outcome_var].mean() - (att * treated.shape[0] / matched_data.shape[0])) - control[outcome_var].mean()
        
        return {
            "success": True,
            "results": {
                "matched_data": matched_data,
                "balance_table": balance_table,
                "treatment_effect": {"ate": float(ate), "att": float(att), "atc": float(atc)},
                "propensity_scores": data['propensity_score'],
                "n_matched": len(matched_data),
                "quality_metrics": {"mean_std_diff": float(balance_table['standardized_difference'].mean())}
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

def difference_in_differences(data: pd.DataFrame, outcome_var: str, group_var: str, time_var: str, covariates: list[str] = None) -> dict:
    try:
        # 检查变量是否存在
        for var in [outcome_var, group_var, time_var]:
            if var not in data.columns:
                raise ValueError(f"变量 {var} 不存在于数据中")
        
        # 确保时间变量是二分的（0=前，1=后）
        if not set(data[time_var].unique()).issubset({0, 1}):
            raise ValueError("时间变量必须是二分的（0=前，1=后）")
        
        # 确保分组变量是二分的（0=控制组，1=处理组）
        if not set(data[group_var].unique()).issubset({0, 1}):
            raise ValueError("分组变量必须是二分的（0=控制组，1=处理组）")
        
        # 准备数据
        if covariates:
            X = data[[group_var, time_var, group_var + "_" + time_var] + covariates]
            # 创建交互项
            data[group_var + "_" + time_var] = data[group_var] * data[time_var]
        else:
            X = data[[group_var, time_var, group_var + "_" + time_var]]
            data[group_var + "_" + time_var] = data[group_var] * data[time_var]
        
        y = data[outcome_var]
        
        # 拟合线性回归
        model = LinearRegression()
        model.fit(X, y)
        
        # 获取DID估计
        did_estimate = model.coef_[-1]
        
        # 计算标准误
        y_pred = model.predict(X)
        residuals = y - y_pred
        n = len(data)
        k = X.shape[1]
        se = np.sqrt(np.sum(residuals**2) / (n - k) * np.linalg.inv(X.T @ X)[-1, -1])
        
        # 计算置信区间
        ci = did_estimate + np.array([-1, 1]) * 1.96 * se
        
        # 计算p值
        t_stat = did_estimate / se
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n - k))
        
        # 平行趋势检验
        pre_data = data[data[time_var] == 0]
        pre_model = LinearRegression()
        pre_model.fit(pre_data[[group_var]], pre_data[outcome_var])
        pre_trend = pre_model.coef_[0]
        
        post_data = data[data[time_var] == 1]
        post_model = LinearRegression()
        post_model.fit(post_data[[group_var]], post_data[outcome_var])
        post_trend = post_model.coef_[0]
        
        return {
            "success": True,
            "results": {
                "did_estimate": float(did_estimate),
                "se": float(se),
                "ci": [float(ci[0]), float(ci[1])],
                "p_value": float(p_value),
                "parallel_trend_test": {"pre_trend": float(pre_trend), "post_trend": float(post_trend)},
                "pre_trend": float(pre_trend),
                "post_trend": float(post_trend),
                "plot_data": {
                    "control_pre": float(data[(data[group_var] == 0) & (data[time_var] == 0)][outcome_var].mean()),
                    "control_post": float(data[(data[group_var] == 0) & (data[time_var] == 1)][outcome_var].mean()),
                    "treatment_pre": float(data[(data[group_var] == 1) & (data[time_var] == 0)][outcome_var].mean()),
                    "treatment_post": float(data[(data[group_var] == 1) & (data[time_var] == 1)][outcome_var].mean())
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

def instrumental_variable(data: pd.DataFrame, outcome_var: str, endogenous_var: str, instrument_vars: list[str], control_vars: list[str] = None) -> dict:
    try:
        # 检查变量是否存在
        for var in [outcome_var, endogenous_var] + instrument_vars:
            if var not in data.columns:
                raise ValueError(f"变量 {var} 不存在于数据中")
        
        if control_vars:
            for var in control_vars:
                if var not in data.columns:
                    raise ValueError(f"变量 {var} 不存在于数据中")
        
        # 第一阶段回归：内生变量对工具变量和控制变量
        X_first = data[instrument_vars]
        if control_vars:
            X_first = pd.concat([X_first, data[control_vars]], axis=1)
        
        y_first = data[endogenous_var]
        
        first_stage = LinearRegression()
        first_stage.fit(X_first, y_first)
        y_first_pred = first_stage.predict(X_first)
        
        # 计算第一阶段F统计量
        ssr_reg = np.sum((y_first_pred - y_first.mean())**2)
        ssr_res = np.sum((y_first - y_first_pred)**2)
        n = len(data)
        k = X_first.shape[1]
        f_stat = (ssr_reg / k) / (ssr_res / (n - k - 1))
        p_value = 1 - stats.f.cdf(f_stat, k, n - k - 1)
        
        # 第二阶段回归：结果变量对预测的内生变量和控制变量
        X_second = pd.DataFrame({'endogenous_pred': y_first_pred})
        if control_vars:
            X_second = pd.concat([X_second, data[control_vars]], axis=1)
        
        y_second = data[outcome_var]
        
        second_stage = LinearRegression()
        second_stage.fit(X_second, y_second)
        iv_estimate = second_stage.coef_[0]
        
        # OLS回归作为比较
        X_ols = data[[endogenous_var]]
        if control_vars:
            X_ols = pd.concat([X_ols, data[control_vars]], axis=1)
        
        ols_model = LinearRegression()
        ols_model.fit(X_ols, y_second)
        ols_estimate = ols_model.coef_[0]
        
        # 豪斯曼检验
        residuals = y_second - second_stage.predict(X_second)
        X_hausman = pd.concat([X_ols, data[instrument_vars]], axis=1)
        hausman_model = LinearRegression()
        hausman_model.fit(X_hausman, residuals)
        hausman_stat = len(data) * hausman_model.score(X_hausman, residuals)
        hausman_p = 1 - stats.chi2.cdf(hausman_stat, len(instrument_vars))
        
        return {
            "success": True,
            "results": {
                "iv_estimate": float(iv_estimate),
                "first_stage_f": float(f_stat),
                "first_stage_p": float(p_value),
                "weak_instrument_test": {"f_stat": float(f_stat), "p_value": float(p_value)},
                "overid_test": {"statistic": float(hausman_stat), "p_value": float(hausman_p)},
                "ols_estimate": float(ols_estimate),
                "hausman_test": {"statistic": float(hausman_stat), "p_value": float(hausman_p)}
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

def regression_discontinuity(data: pd.DataFrame, outcome_var: str, running_var: str, cutoff: float, bandwidth: float = None, kernel: str = "triangular") -> dict:
    try:
        # 检查变量是否存在
        for var in [outcome_var, running_var]:
            if var not in data.columns:
                raise ValueError(f"变量 {var} 不存在于数据中")
        
        # 计算带宽（如果未提供）
        if bandwidth is None:
            # 使用Imbens-Kalyanaraman带宽
            h = 1.84 * np.std(data[running_var]) * len(data)**(-1/5)
        else:
            h = bandwidth
        
        # 筛选带宽内的数据
        data_bandwidth = data[abs(data[running_var] - cutoff) <= h]
        
        # 创建处理变量
        data_bandwidth['treatment'] = (data_bandwidth[running_var] >= cutoff).astype(int)
        
        # 创建多项式项
        data_bandwidth['running_var_centered'] = data_bandwidth[running_var] - cutoff
        data_bandwidth['running_var_squared'] = data_bandwidth['running_var_centered'] ** 2
        data_bandwidth['interaction'] = data_bandwidth['treatment'] * data_bandwidth['running_var_centered']
        data_bandwidth['interaction_squared'] = data_bandwidth['treatment'] * data_bandwidth['running_var_squared']
        
        # 拟合模型
        X = data_bandwidth[['treatment', 'running_var_centered', 'running_var_squared', 'interaction', 'interaction_squared']]
        y = data_bandwidth[outcome_var]
        
        model = LinearRegression()
        model.fit(X, y)
        
        # 获取RD估计
        rd_estimate = model.coef_[0]
        
        # 计算标准误
        y_pred = model.predict(X)
        residuals = y - y_pred
        n = len(data_bandwidth)
        k = X.shape[1]
        se = np.sqrt(np.sum(residuals**2) / (n - k) * np.linalg.inv(X.T @ X)[0, 0])
        
        # 计算置信区间
        ci = rd_estimate + np.array([-1, 1]) * 1.96 * se
        
        # 计算p值
        t_stat = rd_estimate / se
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n - k))
        
        # 操纵检验（McCrary检验的简化版本）
        density_test = stats.ttest_ind(
            data_bandwidth[data_bandwidth['treatment'] == 0]['running_var_centered'],
            data_bandwidth[data_bandwidth['treatment'] == 1]['running_var_centered']
        )
        
        return {
            "success": True,
            "results": {
                "rd_estimate": float(rd_estimate),
                "se": float(se),
                "ci": [float(ci[0]), float(ci[1])],
                "p_value": float(p_value),
                "bandwidth_optimal": float(h),
                "manipulation_test": {"t_stat": float(density_test.statistic), "p_value": float(density_test.pvalue)},
                "plot_data": {
                    "running_var": data_bandwidth[running_var].tolist(),
                    "outcome_var": data_bandwidth[outcome_var].tolist(),
                    "treatment": data_bandwidth['treatment'].tolist(),
                    "cutoff": cutoff
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

def quantile_regression(data: pd.DataFrame, dependent_var: str, independent_vars: list[str], quantiles: list[float] = None) -> dict:
    try:
        # 检查变量是否存在
        for var in [dependent_var] + independent_vars:
            if var not in data.columns:
                raise ValueError(f"变量 {var} 不存在于数据中")
        
        # 默认分位数
        if quantiles is None:
            quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]
        
        # 准备数据
        X = data[independent_vars]
        y = data[dependent_var]
        
        # 拟合不同分位数的回归
        coefficients_by_quantile = {}
        predictions = {}
        
        for q in quantiles:
            model = QuantileRegressor(quantile=q, solver='highs')
            model.fit(X, y)
            
            coefficients = {}
            coefficients['intercept'] = float(model.intercept_)
            for i, var in enumerate(independent_vars):
                coefficients[var] = float(model.coef_[i])
            
            coefficients_by_quantile[q] = coefficients
            predictions[q] = model.predict(X).tolist()
        
        return {
            "success": True,
            "results": {
                "coefficients_by_quantile": coefficients_by_quantile,
                "predictions": predictions,
                "plot_data": {
                    "quantiles": quantiles,
                    "coefficients": {var: [coefficients_by_quantile[q][var] for q in quantiles] for var in ['intercept'] + independent_vars}
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
