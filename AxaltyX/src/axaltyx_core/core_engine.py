import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional

# 导入数据分析模块
from .descriptive.stats import descriptive_stats, frequency_table, cross_tabulation
from .correlation.correlation import correlation_analysis, partial_correlation, spearman_correlation
from .t_test.t_tests import one_sample_t_test, independent_samples_t_test, paired_samples_t_test
from .anova.anova import one_way_anova, two_way_anova
from .regression.regression import linear_regression, logistic_regression
from .clustering.clustering import kmeans_clustering, hierarchical_clustering
from .factor_analysis.factor_analysis import factor_analysis
from .nonparametric.nonparametric import mann_whitney_u_test, wilcoxon_signed_rank_test, kruskal_wallis_test, friedman_test
from .data_management.io import load_data as load_data_file, save_data as save_data_file


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
            'nonparametric': {'params_schema': {'variables': {'type': 'list', 'required': True}}}
        }

    def load_data(self, path: str, file_type: str) -> dict:
        """加载数据"""
        try:
            # 使用data_management.io模块加载数据
            data = load_data_file(path, file_type)
            self.current_data = data
            
            return {
                "success": True,
                "data": data.values.tolist(),
                "columns": data.columns.tolist(),
                "rows": len(data),
                "columns_count": len(data.columns)
            }
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
                # 使用data_management.io模块保存数据
                save_data_file(self.current_data, path, file_type, encoding)
                return {
                    "success": True,
                    "path": path,
                    "file_type": file_type,
                    "encoding": encoding
                }
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

    def run_frequency_analysis(self, variable: str, sort: str = "value", cumulative: bool = True) -> dict:
        """运行频数分析"""
        if self.current_data is not None:
            return frequency_table(self.current_data, variable, sort, cumulative)
        else:
            return {"success": False, "error": "No data available"}

    def run_crosstab_analysis(self, row_var: str, col_var: str, expected: bool = False, percentages: str = "none") -> dict:
        """运行交叉表分析"""
        if self.current_data is not None:
            return cross_tabulation(self.current_data, row_var, col_var, expected, percentages)
        else:
            return {"success": False, "error": "No data available"}

    def run_correlation_analysis(self, variables: list, method: str = "pearson") -> dict:
        """运行相关分析"""
        if self.current_data is not None:
            if method == "pearson":
                return correlation_analysis(self.current_data, variables)
            elif method == "spearman":
                return spearman_correlation(self.current_data, variables)
            else:
                return {"success": False, "error": "Invalid correlation method"}
        else:
            return {"success": False, "error": "No data available"}

    def run_t_test(self, test_type: str, **kwargs) -> dict:
        """运行t检验"""
        if self.current_data is not None:
            if test_type == "one_sample":
                return one_sample_t_test(self.current_data, **kwargs)
            elif test_type == "independent":
                return independent_samples_t_test(self.current_data, **kwargs)
            elif test_type == "paired":
                return paired_samples_t_test(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid t-test type"}
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
            else:
                return {"success": False, "error": "Invalid clustering type"}
        else:
            return {"success": False, "error": "No data available"}

    def run_factor_analysis(self, **kwargs) -> dict:
        """运行因子分析"""
        if self.current_data is not None:
            return factor_analysis(self.current_data, **kwargs)
        else:
            return {"success": False, "error": "No data available"}

    def run_nonparametric_test(self, test_type: str, **kwargs) -> dict:
        """运行非参数检验"""
        if self.current_data is not None:
            if test_type == "mann_whitney":
                return mann_whitney_u_test(self.current_data, **kwargs)
            elif test_type == "wilcoxon":
                return wilcoxon_signed_rank_test(self.current_data, **kwargs)
            elif test_type == "kruskal_wallis":
                return kruskal_wallis_test(self.current_data, **kwargs)
            elif test_type == "friedman":
                return friedman_test(self.current_data, **kwargs)
            else:
                return {"success": False, "error": "Invalid nonparametric test type"}
        else:
            return {"success": False, "error": "No data available"}
