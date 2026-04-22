import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional

# 导入数据分析模块
from .descriptive.stats import descriptive_stats, frequency_table, cross_tabulation
from .correlation.correlation import pearson_correlation, partial_correlation, canonical_correlation
from .t_test.t_tests import one_sample_t, independent_t, paired_t
from .anova.anova import one_way_anova, two_way_anova
from .regression.regression import linear_regression, logistic_regression, multiple_linear_regression, ordinal_regression, nonlinear_regression, curve_estimation
from .clustering.clustering import kmeans_clustering, hierarchical_clustering, two_step_clustering, dbscan_clustering
from .factor_analysis.factor_analysis import exploratory_factor_analysis, confirmatory_factor_analysis
from .nonparametric.nonparametric import (
    mann_whitney_u, wilcoxon_signed_rank, kruskal_wallis, friedman_test,
    chi_square_goodness_of_fit, kolmogorov_smirnov_test, shapiro_wilk_test,
    runs_test, binomial_test, moses_extreme_reactions, spearman_rank, kendall_tau
)
from .data_management.io import (
    load_csv, load_excel, load_sav, load_dta, load_json,
    save_csv, save_excel, save_sav
)
from .data_management.manipulation import (
    merge_datasets, sort_data, filter_data, aggregate_data, transpose_data,
    reshape_wide, reshape_long, compute_variable, recode_variable, detect_missing,
    weight_data, create_dataset
)
from .frequency.frequency import frequencies, multiple_response_frequencies
from .crosstab.crosstab import crosstabs, chi_square_test, mcnemar_test, cochran_q_test
from .bayesian.bayesian import bayesian_t_test, bayesian_linear_regression, bayesian_anova
from .causal_inference.causal import (
    propensity_score_matching, difference_in_differences, instrumental_variable,
    regression_discontinuity, quantile_regression
)
from .correspondence.correspondence import simple_correspondence, multiple_correspondence
from .discriminant.discriminant import discriminant_analysis
from .hlm.hlm import hierarchical_linear_model
from .log_linear.log_linear import log_linear
from .machine_learning.ml import (
    random_forest, support_vector_machine, gradient_boosting, neural_network,
    lasso_regression, ridge_regression, elastic_net
)
from .means_comparison.means import means
from .meta_analysis.meta_analysis import meta_analysis
from .missing_data.missing import missing_pattern, em_imputation, multiple_imputation
from .network.network import network_analysis
from .pca.pca import principal_component_analysis
from .probit.probit import probit_analysis
from .reliability.reliability import cronbach_alpha, split_half_reliability, test_retest_reliability, validity_analysis
from .sampling.sampling import complex_survey_analysis
from .sem.sem import sem_analysis
from .spatial.spatial import moran_i
from .survival.survival import kaplan_meier, cox_regression
from .text_mining.text_mining import sentiment_analysis, text_preprocessing
from .time_series.time_series import acf_pacf, arima, exponential_smoothing, decompose


class CoreEngine:
    """核心引擎，提供数据操作和分析功能"""

    def __init__(self):
        """初始化核心引擎"""
        self.current_data = None
        self.analysis_registry = {
            'descriptive': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'frequency': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'crosstab': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'correlation': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'ttest': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'anova': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'regression': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'clustering': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'factor': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'nonparametric': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'data_manipulation': {'params_schema': {'operation': {'type': 'string', 'required': True}}},
            'bayesian': {'params_schema': {'model': {'type': 'string', 'required': True}}},
            'causal': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'correspondence': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'discriminant': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'hlm': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'log_linear': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'machine_learning': {'params_schema': {'model': {'type': 'string', 'required': True}}},
            'means_comparison': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'meta_analysis': {'params_schema': {'studies': {'type': 'list', 'required': True}}},
            'missing_data': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'network': {'params_schema': {'nodes': {'type': 'list', 'required': True}}},
            'pca': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'probit': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'reliability': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'sampling': {'params_schema': {'method': {'type': 'string', 'required': True}}},
            'sem': {'params_schema': {'model': {'type': 'string', 'required': True}}},
            'spatial': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'survival': {'params_schema': {'variables': {'type': 'list', 'required': True}}},
            'text_mining': {'params_schema': {'text_column': {'type': 'string', 'required': True}}},
            'time_series': {'params_schema': {'variables': {'type': 'list', 'required': True}}}
        }

    def load_data(self, path: str, file_type: str) -> dict:
        """加载数据"""
        try:
            # 根据文件类型调用相应的加载函数
            if file_type == "csv":
                result = load_csv(path)
            elif file_type == "excel":
                result = load_excel(path)
            elif file_type == "sav":
                result = load_sav(path)
            elif file_type == "dta":
                result = load_dta(path)
            elif file_type == "json":
                result = load_json(path)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported file type: {file_type}"
                }
            
            if result["success"]:
                # 提取数据
                if "data" in result["results"]:
                    self.current_data = result["results"]["data"]
                elif "sheets" in result["results"]:
                    # 多表情况，取第一个表
                    first_sheet_name = list(result["results"]["sheets"].keys())[0]
                    self.current_data = result["results"]["sheets"][first_sheet_name]
                else:
                    return {
                        "success": False,
                        "error": "No data found in the file"
                    }
                
                data = self.current_data
                return {
                    "success": True,
                    "data": data.values.tolist(),
                    "columns": data.columns.tolist(),
                    "rows": len(data),
                    "columns_count": len(data.columns)
                }
            else:
                return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": path,
                "file_type": file_type
            }

    def save_data(self, path: str, file_type: str, encoding: str) -> dict:
        """保存数据"""
        try:
            if self.current_data is not None:
                # 根据文件类型调用相应的保存函数
                if file_type == "csv":
                    result = save_csv(self.current_data, path, encoding=encoding)
                elif file_type == "excel":
                    result = save_excel(self.current_data, path)
                elif file_type == "sav":
                    result = save_sav(self.current_data, path)
                else:
                    return {
                        "success": False,
                        "error": f"Unsupported file type: {file_type}"
                    }
                
                return result
            else:
                return {
                    "success": False,
                    "error": "No data to save"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": path,
                "file_type": file_type,
                "encoding": encoding
            }

    def create_new_data(self, rows: int, cols: int) -> dict:
        """创建新数据集"""
        try:
            data = pd.DataFrame(np.random.rand(rows, cols))
            data.columns = [f"col{i+1}" for i in range(cols)]
            self.current_data = data
            
            return {
                "success": True,
                "data": data.values.tolist(),
                "columns": data.columns.tolist(),
                "rows": rows,
                "columns_count": cols
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "rows": rows,
                "cols": cols
            }

    def update_data(self, change_info: dict) -> None:
        """更新数据"""
        if self.current_data is not None:
            # 实现数据更新逻辑
            pass

    def update_variable_metadata(self, var_name: str, metadata: dict) -> None:
        """更新变量元数据"""
        if self.current_data is not None and var_name in self.current_data.columns:
            # 实现变量元数据更新逻辑
            pass

    def get_current_data(self):
        """获取当前数据"""
        return self.current_data

    def set_current_data(self, data) -> None:
        """设置当前数据"""
        self.current_data = data

    def get_analysis_registry(self):
        """获取分析注册表"""
        return self.analysis_registry

    # 分析方法
    def run_descriptive_analysis(self, variables: list, statistics: list = None) -> dict:
        """运行描述性统计分析"""
        if self.current_data is not None:
            return descriptive_stats(self.current_data, variables, statistics)
        else:
            return {"success": False, "error": "No data available"}

    def run_frequency_analysis(self, variables: list, **kwargs) -> dict:
        """运行频数分析"""
        if self.current_data is not None:
            return frequencies(self.current_data, variables, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_multiple_response_frequency_analysis(self, var_sets: dict, **kwargs) -> dict:
        """运行多重响应频数分析"""
        if self.current_data is not None:
            return multiple_response_frequencies(self.current_data, var_sets, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_crosstab_analysis(self, row_var: str, col_var: str, **kwargs) -> dict:
        """运行交叉表分析"""
        if self.current_data is not None:
            return crosstabs(self.current_data, row_var, col_var, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_chi_square_test(self, row_var: str, col_var: str) -> dict:
        """运行卡方检验"""
        if self.current_data is not None:
            return chi_square_test(self.current_data, row_var, col_var)
        else:
            return {"success": False, "error": "No data available"}

    def run_mcnemar_test(self, var1: str, var2: str, **kwargs) -> dict:
        """运行McNemar检验"""
        if self.current_data is not None:
            return mcnemar_test(self.current_data, var1, var2, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_cochran_q_test(self, vars: list[str]) -> dict:
        """运行Cochran Q检验"""
        if self.current_data is not None:
            return cochran_q_test(self.current_data, vars)
        else:
            return {"success": False, "error": "No data available"}

    def run_correlation_analysis(self, variables: list, method: str = "pearson") -> dict:
        """运行相关分析"""
        if self.current_data is not None:
            if method == "pearson":
                return pearson_correlation(self.current_data, variables)
            else:
                return {"success": False, "error": "Invalid correlation method"}
        else:
            return {"success": False, "error": "No data available"}

    def run_t_test(self, test_type: str, **kwargs) -> dict:
        """运行t检验"""
        if self.current_data is not None:
            if test_type == "one_sample":
                return one_sample_t(self.current_data, **kwargs)
            elif test_type == "independent":
                return independent_t(self.current_data, **kwargs)
            elif test_type == "paired":
                return paired_t(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid t-test type"}
        else:
            return {"success": False, "error": "No data available"}

    # 数据管理方法
    def run_data_manipulation(self, operation: str, **kwargs) -> dict:
        """运行数据操作"""
        if self.current_data is not None:
            if operation == "filter":
                result = filter_data(self.current_data, **kwargs)
                if result["success"]:
                    self.current_data = result["results"]["data"]
                return result
            elif operation == "sort":
                result = sort_data(self.current_data, **kwargs)
                if result["success"]:
                    self.current_data = result["results"]["data"]
                return result
            elif operation == "aggregate":
                result = aggregate_data(self.current_data, **kwargs)
                if result["success"]:
                    self.current_data = result["results"]["data"]
                return result
            elif operation == "transpose":
                result = transpose_data(self.current_data, **kwargs)
                if result["success"]:
                    self.current_data = result["results"]["data"]
                return result
            elif operation == "reshape_wide":
                result = reshape_wide(self.current_data, **kwargs)
                if result["success"]:
                    self.current_data = result["results"]["data"]
                return result
            elif operation == "reshape_long":
                result = reshape_long(self.current_data, **kwargs)
                if result["success"]:
                    self.current_data = result["results"]["data"]
                return result
            elif operation == "compute":
                result = compute_variable(self.current_data, **kwargs)
                if result["success"]:
                    self.current_data = result["results"]["data"]
                return result
            elif operation == "recode":
                result = recode_variable(self.current_data, **kwargs)
                if result["success"]:
                    self.current_data = result["results"]["data"]
                return result
            elif operation == "detect_missing":
                return detect_missing(self.current_data, **kwargs)
            elif operation == "weight":
                result = weight_data(self.current_data, **kwargs)
                if result["success"]:
                    self.current_data = result["results"]["data"]
                return result
            else:
                return {"success": False, "error": "Invalid data manipulation operation"}
        else:
            return {"success": False, "error": "No data available"}

    # 其他分析方法
    def run_bayesian_analysis(self, analysis_type: str = "t_test", **kwargs) -> dict:
        """运行贝叶斯分析"""
        if self.current_data is not None:
            if analysis_type == "t_test":
                return bayesian_t_test(self.current_data, **kwargs)
            elif analysis_type == "linear_regression":
                return bayesian_linear_regression(self.current_data, **kwargs)
            elif analysis_type == "anova":
                return bayesian_anova(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid Bayesian analysis type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_causal_inference(self, method: str = "propensity_score_matching", **kwargs) -> dict:
        """运行因果推断"""
        if self.current_data is not None:
            if method == "propensity_score_matching":
                return propensity_score_matching(self.current_data, **kwargs)
            elif method == "difference_in_differences":
                return difference_in_differences(self.current_data, **kwargs)
            elif method == "instrumental_variable":
                return instrumental_variable(self.current_data, **kwargs)
            elif method == "regression_discontinuity":
                return regression_discontinuity(self.current_data, **kwargs)
            elif method == "quantile_regression":
                return quantile_regression(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid causal inference method"}
        else:
            return {"success": False, "error": "No data available"}

    def run_correspondence_analysis(self, analysis_type: str = "simple", **kwargs) -> dict:
        """运行对应分析"""
        if self.current_data is not None:
            if analysis_type == "simple":
                return simple_correspondence(self.current_data, **kwargs)
            elif analysis_type == "multiple":
                return multiple_correspondence(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid correspondence analysis type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_discriminant_analysis(self, **kwargs) -> dict:
        """运行判别分析"""
        if self.current_data is not None:
            return discriminant_analysis(self.current_data, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_hierarchical_linear_model(self, **kwargs) -> dict:
        """运行分层线性模型"""
        if self.current_data is not None:
            return hierarchical_linear_model(self.current_data, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_log_linear_analysis(self, **kwargs) -> dict:
        """运行对数线性分析"""
        if self.current_data is not None:
            return log_linear(self.current_data, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_machine_learning_analysis(self, model_type: str = "random_forest", **kwargs) -> dict:
        """运行机器学习分析"""
        if self.current_data is not None:
            if model_type == "random_forest":
                return random_forest(self.current_data, **kwargs)
            elif model_type == "support_vector_machine":
                return support_vector_machine(self.current_data, **kwargs)
            elif model_type == "gradient_boosting":
                return gradient_boosting(self.current_data, **kwargs)
            elif model_type == "neural_network":
                return neural_network(self.current_data, **kwargs)
            elif model_type == "lasso_regression":
                return lasso_regression(self.current_data, **kwargs)
            elif model_type == "ridge_regression":
                return ridge_regression(self.current_data, **kwargs)
            elif model_type == "elastic_net":
                return elastic_net(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid machine learning model type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_means_comparison(self, **kwargs) -> dict:
        """运行均值比较"""
        if self.current_data is not None:
            return means(self.current_data, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_meta_analysis(self, **kwargs) -> dict:
        """运行元分析"""
        if self.current_data is not None:
            return meta_analysis(self.current_data, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_missing_data_analysis(self, analysis_type: str = "pattern", **kwargs) -> dict:
        """运行缺失数据分析"""
        if self.current_data is not None:
            if analysis_type == "pattern":
                return missing_pattern(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid missing data analysis type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_impute_missing(self, impute_type: str = "em", **kwargs) -> dict:
        """运行缺失值插补"""
        if self.current_data is not None:
            if impute_type == "em":
                result = em_imputation(self.current_data, **kwargs)
                if result["success"]:
                    self.current_data = result["results"]["imputed_data"]
                return result
            elif impute_type == "multiple":
                result = multiple_imputation(self.current_data, **kwargs)
                # 多重插补返回多个数据集，这里使用第一个作为当前数据
                if result["success"] and result["results"]["imputed_datasets"]:
                    self.current_data = result["results"]["imputed_datasets"][0]
                return result
            else:
                return {"success": False, "error": "Invalid imputation type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_network_analysis(self, **kwargs) -> dict:
        """运行网络分析"""
        if self.current_data is not None:
            return network_analysis(self.current_data, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_principal_component_analysis(self, **kwargs) -> dict:
        """运行主成分分析"""
        if self.current_data is not None:
            return principal_component_analysis(self.current_data, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_probit_analysis(self, **kwargs) -> dict:
        """运行Probit分析"""
        if self.current_data is not None:
            return probit_analysis(self.current_data, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_reliability_analysis(self, analysis_type: str = "cronbach_alpha", **kwargs) -> dict:
        """运行信度分析"""
        if self.current_data is not None:
            if analysis_type == "cronbach_alpha":
                return cronbach_alpha(self.current_data, **kwargs)
            elif analysis_type == "split_half":
                return split_half_reliability(self.current_data, **kwargs)
            elif analysis_type == "test_retest":
                return test_retest_reliability(self.current_data, **kwargs)
            elif analysis_type == "validity":
                return validity_analysis(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid reliability analysis type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_sampling(self, **kwargs) -> dict:
        """运行抽样方法"""
        if self.current_data is not None:
            return complex_survey_analysis(self.current_data, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_structural_equation_modeling(self, **kwargs) -> dict:
        """运行结构方程模型"""
        if self.current_data is not None:
            return sem_analysis(self.current_data, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_spatial_analysis(self, analysis_type: str = "moran_i", **kwargs) -> dict:
        """运行空间分析"""
        if self.current_data is not None:
            if analysis_type == "moran_i":
                return moran_i(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid spatial analysis type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_survival_analysis(self, analysis_type: str = "kaplan_meier", **kwargs) -> dict:
        """运行生存分析"""
        if self.current_data is not None:
            if analysis_type == "kaplan_meier":
                return kaplan_meier(self.current_data, **kwargs)
            elif analysis_type == "cox_regression":
                return cox_regression(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid survival analysis type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_text_mining_analysis(self, analysis_type: str = "sentiment", **kwargs) -> dict:
        """运行文本挖掘分析"""
        if self.current_data is not None:
            if analysis_type == "sentiment":
                return sentiment_analysis(self.current_data, **kwargs)
            elif analysis_type == "preprocessing":
                return text_preprocessing(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid text mining analysis type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_time_series_analysis(self, analysis_type: str = "acf_pacf", **kwargs) -> dict:
        """运行时间序列分析"""
        if self.current_data is not None:
            if analysis_type == "acf_pacf":
                return acf_pacf(self.current_data, **kwargs)
            elif analysis_type == "arima":
                return arima(self.current_data, **kwargs)
            elif analysis_type == "exponential_smoothing":
                return exponential_smoothing(self.current_data, **kwargs)
            elif analysis_type == "decompose":
                return decompose(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid time series analysis type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_anova(self, anova_type: str, **kwargs) -> dict:
        """运行方差分析"""
        if self.current_data is not None:
            if anova_type == "one_way":
                return one_way_anova(self.current_data, **kwargs)
            elif anova_type == "two_way":
                return two_way_anova(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid ANOVA type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_regression(self, regression_type: str, **kwargs) -> dict:
        """运行回归分析"""
        if self.current_data is not None:
            if regression_type == "linear":
                return linear_regression(self.current_data, **kwargs)
            elif regression_type == "logistic":
                return logistic_regression(self.current_data, **kwargs)
            elif regression_type == "multiple":
                return multiple_linear_regression(self.current_data, **kwargs)
            elif regression_type == "ordinal":
                return ordinal_regression(self.current_data, **kwargs)
            elif regression_type == "nonlinear":
                return nonlinear_regression(self.current_data, **kwargs)
            elif regression_type == "curve":
                return curve_estimation(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid regression type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_clustering(self, clustering_type: str, **kwargs) -> dict:
        """运行聚类分析"""
        if self.current_data is not None:
            if clustering_type == "kmeans":
                return kmeans_clustering(self.current_data, **kwargs)
            elif clustering_type == "hierarchical":
                return hierarchical_clustering(self.current_data, **kwargs)
            elif clustering_type == "two_step":
                return two_step_clustering(self.current_data, **kwargs)
            elif clustering_type == "dbscan":
                return dbscan_clustering(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid clustering type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_factor_analysis(self, analysis_type: str = "exploratory", **kwargs) -> dict:
        """运行因子分析"""
        if self.current_data is not None:
            if analysis_type == "exploratory":
                return exploratory_factor_analysis(self.current_data, **kwargs)
            elif analysis_type == "confirmatory":
                return confirmatory_factor_analysis(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid factor analysis type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_nonparametric_test(self, test_type: str, **kwargs) -> dict:
        """运行非参数检验"""
        if self.current_data is not None:
            if test_type == "mann_whitney":
                return mann_whitney_u(self.current_data, **kwargs)
            elif test_type == "wilcoxon":
                return wilcoxon_signed_rank(self.current_data, **kwargs)
            elif test_type == "kruskal_wallis":
                return kruskal_wallis(self.current_data, **kwargs)
            elif test_type == "friedman":
                return friedman_test(self.current_data, **kwargs)
            elif test_type == "chi_square_goodness_of_fit":
                return chi_square_goodness_of_fit(self.current_data, **kwargs)
            elif test_type == "kolmogorov_smirnov":
                return kolmogorov_smirnov_test(self.current_data, **kwargs)
            elif test_type == "shapiro_wilk":
                return shapiro_wilk_test(self.current_data, **kwargs)
            elif test_type == "runs":
                return runs_test(self.current_data, **kwargs)
            elif test_type == "binomial":
                return binomial_test(self.current_data, **kwargs)
            elif test_type == "moses_extreme_reactions":
                return moses_extreme_reactions(self.current_data, **kwargs)
            elif test_type == "spearman_rank":
                return spearman_rank(self.current_data, **kwargs)
            elif test_type == "kendall_tau":
                return kendall_tau(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid nonparametric test type"}
        else:
            return {"success": False, "error": "No data available"}
