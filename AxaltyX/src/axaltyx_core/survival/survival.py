import pandas as pd
import numpy as np
from scipy import stats
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test
from typing import Dict, Any, List, Optional


def kaplan_meier(
    data: pd.DataFrame,
    time_var: str,
    event_var: str,
    group_var: str = None,
    conf_level: float = 0.95
) -> dict:
    """
    Kaplan-Meier生存分析
    
    Args:
        data: 输入数据
        time_var: 时间变量
        event_var: 事件变量
        group_var: 分组变量（可选）
        conf_level: 置信水平
    
    Returns:
        Kaplan-Meier生存分析结果
    """
    try:
        # 准备数据
        survival_data = data[[time_var, event_var]].dropna()
        if group_var:
            survival_data[group_var] = data.loc[survival_data.index, group_var]
        
        # 计算生存曲线
        if group_var:
            # 按组计算
            groups = survival_data[group_var].unique()
            km_fitters = {}
            survival_tables = {}
            median_survival = {}
            plot_data = {}
            
            for group in groups:
                group_data = survival_data[survival_data[group_var] == group]
                kmf = KaplanMeierFitter()
                kmf.fit(group_data[time_var], group_data[event_var], alpha=1-conf_level)
                km_fitters[group] = kmf
                
                # 生成生存表
                event_table = kmf.event_table
                # 计算标准误差（简化处理）
                se = np.sqrt(kmf.survival_function_['KM_estimate'] * (1 - kmf.survival_function_['KM_estimate']) / event_table['at_risk'])
                
                # 获取置信区间列名
                ci_columns = list(kmf.confidence_interval_.columns)
                lower_ci_col = ci_columns[0] if ci_columns else 'KM_estimate_lower_95'
                upper_ci_col = ci_columns[1] if len(ci_columns) > 1 else 'KM_estimate_upper_95'
                
                survival_table = pd.DataFrame({
                    "Time": kmf.timeline,
                    "At Risk": event_table['at_risk'],
                    "Events": event_table['observed'],
                    "Survival Probability": kmf.survival_function_['KM_estimate'],
                    "Standard Error": se,
                    "Lower CI": kmf.confidence_interval_[lower_ci_col] if lower_ci_col in kmf.confidence_interval_ else kmf.survival_function_['KM_estimate'],
                    "Upper CI": kmf.confidence_interval_[upper_ci_col] if upper_ci_col in kmf.confidence_interval_ else kmf.survival_function_['KM_estimate']
                })
                survival_tables[group] = survival_table
                
                # 计算中位生存时间
                median_survival[group] = kmf.median_survival_time_
                
                # 构建绘图数据
                plot_data[group] = {
                    "time": kmf.timeline.tolist(),
                    "survival": kmf.survival_function_['KM_estimate'].tolist(),
                    "ci_lower": kmf.confidence_interval_[lower_ci_col].tolist(),
                    "ci_upper": kmf.confidence_interval_[upper_ci_col].tolist()
                }
            
            # 执行对数秩检验
            groups_data = [survival_data[survival_data[group_var] == group] for group in groups]
            times = [group[time_var].values for group in groups_data]
            events = [group[event_var].values for group in groups_data]
            log_rank = logrank_test(times, events)
            log_rank_test_result = {
                "chi2": log_rank.test_statistic,
                "df": log_rank.degrees_of_freedom,
                "p": log_rank.p_value
            }
            
            # 合并生存表
            combined_survival_table = pd.concat(survival_tables, names=[group_var, "Index"])
        else:
            # 整体计算
            kmf = KaplanMeierFitter()
            kmf.fit(survival_data[time_var], survival_data[event_var], alpha=1-conf_level)
            
            # 生成生存表
            event_table = kmf.event_table
            # 计算标准误差（简化处理）
            se = np.sqrt(kmf.survival_function_['KM_estimate'] * (1 - kmf.survival_function_['KM_estimate']) / event_table['at_risk'])
            
            # 获取置信区间列名
            ci_columns = list(kmf.confidence_interval_.columns)
            lower_ci_col = ci_columns[0] if ci_columns else 'KM_estimate_lower_95'
            upper_ci_col = ci_columns[1] if len(ci_columns) > 1 else 'KM_estimate_upper_95'
            
            survival_table = pd.DataFrame({
                "Time": kmf.timeline,
                "At Risk": event_table['at_risk'],
                "Events": event_table['observed'],
                "Survival Probability": kmf.survival_function_['KM_estimate'],
                "Standard Error": se,
                "Lower CI": kmf.confidence_interval_[lower_ci_col] if lower_ci_col in kmf.confidence_interval_ else kmf.survival_function_['KM_estimate'],
                "Upper CI": kmf.confidence_interval_[upper_ci_col] if upper_ci_col in kmf.confidence_interval_ else kmf.survival_function_['KM_estimate']
            })
            combined_survival_table = survival_table
            
            # 计算中位生存时间
            median_survival = {"Overall": kmf.median_survival_time_}
            
            # 对数秩检验为None
            log_rank_test_result = None
            
            # 构建绘图数据
            plot_data = {
                "Overall": {
                    "time": kmf.timeline.tolist(),
                    "survival": kmf.survival_function_['KM_estimate'].tolist(),
                    "ci_lower": kmf.confidence_interval_[lower_ci_col].tolist(),
                    "ci_upper": kmf.confidence_interval_[upper_ci_col].tolist()
                }
            }
        
        # 构建结果
        results = {
            "survival_table": combined_survival_table,
            "median_survival": median_survival,
            "log_rank_test": log_rank_test_result,
            "plot_data": plot_data,
            "conf_level": conf_level
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


def cox_regression(
    data: pd.DataFrame,
    time_var: str,
    event_var: str,
    covariates: list[str],
    method: str = "enter",
    ci_level: float = 0.95
) -> dict:
    """
    Cox比例风险回归
    
    Args:
        data: 输入数据
        time_var: 时间变量
        event_var: 事件变量
        covariates: 协变量列表
        method: 变量进入方法（enter/stepwise）
        ci_level: 置信水平
    
    Returns:
        Cox比例风险回归结果
    """
    try:
        # 准备数据
        cox_data = data[[time_var, event_var] + covariates].dropna()
        
        # 拟合Cox模型
        cph = CoxPHFitter()
        cph.fit(cox_data, duration_col=time_var, event_col=event_var, show_progress=False)
        
        # 提取模型摘要
        model_summary = {
            "n": len(cox_data),
            "events": cox_data[event_var].sum(),
            "log_likelihood": cph.log_likelihood_,
            "overall_chi2": cph.test_statistic_,
            "df": cph.df_model_,
            "p": cph.p_value_
        }
        
        # 提取系数
        coefficients = cph.summary
        
        # 计算风险比（HR）
        hr = np.exp(coefficients['coef'])
        coefficients['HR'] = hr
        
        # 计算置信区间
        ci = cph.confidence_intervals(alpha=1-ci_level)
        coefficients['CI Lower'] = ci['lower bound']
        coefficients['CI Upper'] = ci['upper bound']
        
        # 拟合优度检验
        omnibus_test = {
            "chi2": cph.test_statistic_,
            "df": cph.df_model_,
            "p": cph.p_value_
        }
        
        # 变量列表
        variables_in_model = covariates
        
        # 基线生存函数
        baseline_survival = cph.baseline_survival_ 
        
        # 比例风险假设检验（简化处理）
        proportional_hazards_test = {
            "test_type": "Schoenfeld residuals",
            "p_values": {}
        }
        
        # 构建结果
        results = {
            "model_summary": model_summary,
            "coefficients": coefficients,
            "omnibus_test": omnibus_test,
            "variables_in_model": variables_in_model,
            "baseline_survival": baseline_survival,
            "proportional_hazards_test": proportional_hazards_test
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
