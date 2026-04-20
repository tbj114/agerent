import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy import stats
from typing import Dict, Any, List, Optional


def acf_pacf(
    data: pd.DataFrame,
    var: str,
    nlags: int = 40,
    alpha: float = 0.05
) -> dict:
    """
    自相关和偏自相关函数
    
    Args:
        data: 输入数据
        var: 时间序列变量
        nlags: 滞后阶数
        alpha: 显著性水平
    
    Returns:
        自相关和偏自相关分析结果
    """
    try:
        # 准备数据
        ts_data = data[var].dropna()
        
        # 计算自相关函数
        acf_values, acf_ci = acf(ts_data, nlags=nlags, alpha=alpha)
        
        # 计算偏自相关函数
        pacf_values, pacf_ci = pacf(ts_data, nlags=nlags, alpha=alpha)
        
        # 识别显著的滞后阶数
        significant_lags = {
            "acf": [i for i in range(len(acf_values)) if abs(acf_values[i]) > acf_ci[i, 1] - acf_values[i]],
            "pacf": [i for i in range(len(pacf_values)) if abs(pacf_values[i]) > pacf_ci[i, 1] - pacf_values[i]]
        }
        
        # 构建结果
        results = {
            "acf_values": acf_values.tolist(),
            "acf_ci": acf_ci.tolist(),
            "pacf_values": pacf_values.tolist(),
            "pacf_ci": pacf_ci.tolist(),
            "nlags": nlags,
            "significant_lags": significant_lags
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


def arima(
    data: pd.DataFrame,
    var: str,
    order: tuple = (1, 1, 1),
    seasonal_order: tuple = None,
    forecast_steps: int = 10
) -> dict:
    """
    ARIMA模型
    
    Args:
        data: 输入数据
        var: 时间序列变量
        order: ARIMA阶数 (p, d, q)
        seasonal_order: 季节性ARIMA阶数 (P, D, Q, s)，None表示非季节性
        forecast_steps: 预测步数
    
    Returns:
        ARIMA模型结果
    """
    try:
        # 准备数据
        ts_data = data[var].dropna()
        
        # 拟合ARIMA模型
        if seasonal_order:
            model = ARIMA(ts_data, order=order, seasonal_order=seasonal_order)
        else:
            model = ARIMA(ts_data, order=order)
        
        model_fit = model.fit()
        
        # 提取模型信息
        model_info = {
            "order": order,
            "aic": model_fit.aic,
            "bic": model_fit.bic,
            "hqic": model_fit.hqic
        }
        
        # 提取系数
        coefficients = model_fit.summary().tables[1]
        coefficients_df = pd.read_html(coefficients.as_html(), header=0, index_col=0)[0]
        
        # 计算残差
        residuals = model_fit.resid
        ljung_box = stats.lilliefors(residuals)
        
        residual_info = {
            "mean": residuals.mean(),
            "std": residuals.std(),
            "ljung_box": ljung_box[0],
            "p": ljung_box[1]
        }
        
        # 计算拟合值
        fitted_values = model_fit.fittedvalues
        
        # 预测
        forecast = model_fit.forecast(steps=forecast_steps)
        forecast_ci = model_fit.get_forecast(steps=forecast_steps).conf_int()
        
        forecast_info = {
            "values": forecast.tolist(),
            "ci_lower": forecast_ci.iloc[:, 0].tolist(),
            "ci_upper": forecast_ci.iloc[:, 1].tolist()
        }
        
        # 诊断信息
        diagnostics = {
            "converged": model_fit.mle_retvals["converged"],
            "n_iterations": model_fit.mle_retvals["iterations"]
        }
        
        # 构建结果
        results = {
            "model": model_info,
            "coefficients": coefficients_df,
            "residuals": residual_info,
            "fitted_values": fitted_values,
            "forecast": forecast_info,
            "diagnostics": diagnostics
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


def exponential_smoothing(
    data: pd.DataFrame,
    var: str,
    trend: str = "add",
    seasonal: str = None,
    seasonal_periods: int = None,
    damped_trend: bool = False,
    forecast_steps: int = 10
) -> dict:
    """
    指数平滑模型
    
    Args:
        data: 输入数据
        var: 时间序列变量
        trend: 趋势类型（add/mul/none）
        seasonal: 季节类型（add/mul/none）
        seasonal_periods: 季节周期
        damped_trend: 是否使用阻尼趋势
        forecast_steps: 预测步数
    
    Returns:
        指数平滑模型结果
    """
    try:
        # 准备数据
        ts_data = data[var].dropna()
        
        # 拟合指数平滑模型
        model = ExponentialSmoothing(
            ts_data,
            trend=trend,
            seasonal=seasonal,
            seasonal_periods=seasonal_periods,
            damped_trend=damped_trend
        )
        
        model_fit = model.fit()
        
        # 计算拟合值
        fitted = model_fit.fittedvalues
        
        # 预测
        forecast = model_fit.forecast(steps=forecast_steps)
        
        # 计算残差
        residuals = ts_data - fitted
        
        # 计算平滑参数
        smoothing_parameters = {
            "alpha": model_fit.params.get("smoothing_level", None),
            "beta": model_fit.params.get("smoothing_trend", None),
            "gamma": model_fit.params.get("smoothing_seasonal", None),
            "phi": model_fit.params.get("damping_trend", None)
        }
        
        # 计算评估指标
        def mean_absolute_percentage_error(y_true, y_pred):
            return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        def mean_absolute_scaled_error(y_true, y_pred):
            naive_pred = y_true.shift(1)
            mae = np.mean(np.abs(y_true - y_pred))
            mae_naive = np.mean(np.abs(y_true[1:] - naive_pred[1:]))
            return mae / mae_naive
        
        mape = mean_absolute_percentage_error(ts_data, fitted)
        mase = mean_absolute_scaled_error(ts_data, fitted)
        
        # 构建结果
        results = {
            "fitted": fitted,
            "forecast": forecast,
            "residuals": residuals,
            "smoothing_parameters": smoothing_parameters,
            "aic": model_fit.aic,
            "bic": model_fit.bic,
            "mape": mape,
            "mase": mase
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


def decompose(
    data: pd.DataFrame,
    var: str,
    period: int,
    model: str = "additive"
) -> dict:
    """
    时间序列分解
    
    Args:
        data: 输入数据
        var: 时间序列变量
        period: 周期长度
        model: 分解模型（additive/multiplicative）
    
    Returns:
        时间序列分解结果
    """
    try:
        # 准备数据
        ts_data = data[var].dropna()
        
        # 执行分解
        decomposition = seasonal_decompose(ts_data, period=period, model=model)
        
        # 提取分解结果
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid
        observed = decomposition.observed
        
        # 构建绘图数据
        plot_data = {
            "observed": observed.tolist(),
            "trend": trend.tolist(),
            "seasonal": seasonal.tolist(),
            "residual": residual.tolist(),
            "index": observed.index.tolist()
        }
        
        # 构建结果
        results = {
            "trend": trend,
            "seasonal": seasonal,
            "residual": residual,
            "observed": observed,
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
