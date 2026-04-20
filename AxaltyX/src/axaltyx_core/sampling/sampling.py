import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression

def complex_survey_analysis(data: pd.DataFrame, design_vars: dict, analysis_type: str, analysis_vars: dict) -> dict:
    try:
        # 检查设计变量
        weights = design_vars.get('weights')
        strata = design_vars.get('strata')
        clusters = design_vars.get('clusters')
        ids = design_vars.get('ids')
        
        # 检查分析变量
        if analysis_type == 'mean':
            if 'variable' not in analysis_vars:
                raise ValueError("分析类型为mean时，需要指定variable")
            var = analysis_vars['variable']
            if var not in data.columns:
                raise ValueError(f"变量 {var} 不存在于数据中")
        elif analysis_type == 'proportion':
            if 'variable' not in analysis_vars:
                raise ValueError("分析类型为proportion时，需要指定variable")
            var = analysis_vars['variable']
            if var not in data.columns:
                raise ValueError(f"变量 {var} 不存在于数据中")
        elif analysis_type == 'total':
            if 'variable' not in analysis_vars:
                raise ValueError("分析类型为total时，需要指定variable")
            var = analysis_vars['variable']
            if var not in data.columns:
                raise ValueError(f"变量 {var} 不存在于数据中")
        elif analysis_type == 'ratio':
            if 'numerator' not in analysis_vars or 'denominator' not in analysis_vars:
                raise ValueError("分析类型为ratio时，需要指定numerator和denominator")
            numerator_var = analysis_vars['numerator']
            denominator_var = analysis_vars['denominator']
            if numerator_var not in data.columns:
                raise ValueError(f"变量 {numerator_var} 不存在于数据中")
            if denominator_var not in data.columns:
                raise ValueError(f"变量 {denominator_var} 不存在于数据中")
        elif analysis_type == 'logistic_regression':
            if 'dependent_var' not in analysis_vars or 'independent_vars' not in analysis_vars:
                raise ValueError("分析类型为logistic_regression时，需要指定dependent_var和independent_vars")
            dependent_var = analysis_vars['dependent_var']
            independent_vars = analysis_vars['independent_vars']
            if dependent_var not in data.columns:
                raise ValueError(f"变量 {dependent_var} 不存在于数据中")
            for var in independent_vars:
                if var not in data.columns:
                    raise ValueError(f"变量 {var} 不存在于数据中")
        else:
            raise ValueError(f"不支持的分析类型: {analysis_type}")
        
        # 计算权重（如果提供）
        if weights:
            if weights not in data.columns:
                raise ValueError(f"权重变量 {weights} 不存在于数据中")
            survey_weights = data[weights].values
        else:
            survey_weights = np.ones(len(data))
        
        # 计算有效样本量
        effective_n = np.sum(survey_weights) ** 2 / np.sum(survey_weights ** 2)
        
        # 计算设计效应
        deff = len(data) / effective_n if effective_n > 0 else 1
        
        if analysis_type == 'mean':
            # 计算加权均值
            weighted_mean = np.sum(data[var] * survey_weights) / np.sum(survey_weights)
            
            # 计算标准误（简化版）
            variance = np.sum(survey_weights * (data[var] - weighted_mean) ** 2) / (np.sum(survey_weights) - 1)
            se = np.sqrt(variance / effective_n)
            
            # 计算置信区间
            ci = weighted_mean + np.array([-1, 1]) * 1.96 * se
            
            estimate = float(weighted_mean)
            
        elif analysis_type == 'proportion':
            # 计算加权比例
            weighted_count = np.sum(data[var] * survey_weights)
            weighted_total = np.sum(survey_weights)
            weighted_prop = weighted_count / weighted_total
            
            # 计算标准误（简化版）
            variance = weighted_prop * (1 - weighted_prop) / effective_n
            se = np.sqrt(variance)
            
            # 计算置信区间
            ci = weighted_prop + np.array([-1, 1]) * 1.96 * se
            
            estimate = float(weighted_prop)
            
        elif analysis_type == 'total':
            # 计算加权总和
            weighted_total = np.sum(data[var] * survey_weights)
            
            # 计算标准误（简化版）
            variance = np.sum(survey_weights ** 2 * data[var] ** 2)
            se = np.sqrt(variance)
            
            # 计算置信区间
            ci = weighted_total + np.array([-1, 1]) * 1.96 * se
            
            estimate = float(weighted_total)
            
        elif analysis_type == 'ratio':
            # 计算加权分子和分母
            weighted_numerator = np.sum(data[numerator_var] * survey_weights)
            weighted_denominator = np.sum(data[denominator_var] * survey_weights)
            ratio = weighted_numerator / weighted_denominator if weighted_denominator > 0 else 0
            
            # 计算标准误（简化版）
            variance = (np.sum(survey_weights * (data[numerator_var] - ratio * data[denominator_var]) ** 2) / np.sum(survey_weights) ** 2)
            se = np.sqrt(variance)
            
            # 计算置信区间
            ci = ratio + np.array([-1, 1]) * 1.96 * se
            
            estimate = float(ratio)
            
        elif analysis_type == 'logistic_regression':
            # 拟合加权逻辑回归
            X = data[independent_vars]
            y = data[dependent_var]
            
            model = LogisticRegression(random_state=42)
            model.fit(X, y, sample_weight=survey_weights)
            
            # 获取系数
            coefficients = {}
            coefficients['intercept'] = float(model.intercept_[0])
            for i, var in enumerate(independent_vars):
                coefficients[var] = float(model.coef_[0][i])
            
            estimate = coefficients
            se = None
            ci = None
        
        return {
            "success": True,
            "results": {
                "estimate": estimate,
                "se": float(se) if se is not None else None,
                "ci": [float(ci[0]), float(ci[1])] if ci is not None else None,
                "deff": float(deff),
                "design_effect": float(deff),
                "effective_n": float(effective_n)
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
