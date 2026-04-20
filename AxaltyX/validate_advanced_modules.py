import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np
from sklearn.datasets import load_iris, make_blobs, load_wine
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 导入所有高级统计模块
from axaltyx_core.regression.regression import linear_regression, multiple_linear_regression, logistic_regression, ordinal_regression, nonlinear_regression, curve_estimation
from axaltyx_core.factor_analysis.factor_analysis import exploratory_factor_analysis, confirmatory_factor_analysis
from axaltyx_core.pca.pca import principal_component_analysis
from axaltyx_core.clustering.clustering import hierarchical_clustering, kmeans_clustering, two_step_clustering, dbscan_clustering
from axaltyx_core.discriminant.discriminant import discriminant_analysis
from axaltyx_core.correspondence.correspondence import simple_correspondence, multiple_correspondence
from axaltyx_core.reliability.reliability import cronbach_alpha, split_half_reliability, test_retest_reliability, validity_analysis
from axaltyx_core.survival.survival import kaplan_meier, cox_regression
from axaltyx_core.time_series.time_series import acf_pacf, arima, exponential_smoothing, decompose
from axaltyx_core.missing_data.missing import missing_pattern, em_imputation, multiple_imputation
from axaltyx_core.log_linear.log_linear import log_linear
from axaltyx_core.probit.probit import probit_analysis
from axaltyx_core.meta_analysis.meta_analysis import meta_analysis
from axaltyx_core.sem.sem import sem_analysis
from axaltyx_core.bayesian.bayesian import bayesian_t_test, bayesian_linear_regression, bayesian_anova
from axaltyx_core.machine_learning.ml import random_forest, support_vector_machine, gradient_boosting, neural_network, lasso_regression, ridge_regression, elastic_net
from axaltyx_core.causal_inference.causal import propensity_score_matching, difference_in_differences, instrumental_variable, regression_discontinuity, quantile_regression
from axaltyx_core.hlm.hlm import hierarchical_linear_model
from axaltyx_core.text_mining.text_mining import sentiment_analysis, text_preprocessing
from axaltyx_core.spatial.spatial import moran_i
from axaltyx_core.network.network import network_analysis
from axaltyx_core.sampling.sampling import complex_survey_analysis

# 生成测试数据集
def generate_test_data():
    # 1. 回归分析数据
    iris = load_iris()
    iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    iris_df['target'] = iris.target
    
    # 2. 聚类分析数据
    X, y = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)
    cluster_df = pd.DataFrame(data=X, columns=['feature1', 'feature2'])
    
    # 3. 时间序列数据
    date_rng = pd.date_range(start='2020-01-01', end='2020-12-31', freq='D')
    time_series_df = pd.DataFrame(date_rng, columns=['date'])
    time_series_df['value'] = np.sin(np.arange(len(date_rng)) * 0.1) + np.random.normal(0, 0.1, len(date_rng))
    
    # 4. 文本分析数据
    text_df = pd.DataFrame({
        'text': [
            '这个产品非常好，我很喜欢',
            '服务质量很差，我很失望',
            '价格合理，性价比高',
            '包装精美，物流很快',
            '质量一般，不符合预期'
        ]
    })
    
    # 5. 网络分析数据
    network_df = pd.DataFrame({
        'source': ['A', 'A', 'B', 'B', 'C', 'C', 'D'],
        'target': ['B', 'C', 'C', 'D', 'D', 'E', 'E']
    })
    
    # 6. 因果推断数据
    causal_df = pd.DataFrame({
        'treatment': np.random.randint(0, 2, 100),
        'outcome': np.random.normal(0, 1, 100) + 0.5 * np.random.randint(0, 2, 100),
        'covariate1': np.random.normal(0, 1, 100),
        'covariate2': np.random.normal(0, 1, 100)
    })
    
    # 7. 分层线性模型数据
    hlm_df = pd.DataFrame({
        'group': np.repeat(range(10), 10),
        'level1_var1': np.random.normal(0, 1, 100),
        'level1_var2': np.random.normal(0, 1, 100),
        'level2_var1': np.repeat(np.random.normal(0, 1, 10), 10),
        'dependent_var': np.random.normal(0, 1, 100)
    })
    
    # 8. 缺失值数据
    missing_df = pd.DataFrame({
        'var1': np.random.normal(0, 1, 100),
        'var2': np.random.normal(0, 1, 100),
        'var3': np.random.normal(0, 1, 100)
    })
    # 随机添加缺失值
    missing_df.loc[np.random.choice(missing_df.index, 20), 'var1'] = np.nan
    missing_df.loc[np.random.choice(missing_df.index, 15), 'var2'] = np.nan
    
    return {
        'iris': iris_df,
        'cluster': cluster_df,
        'time_series': time_series_df,
        'text': text_df,
        'network': network_df,
        'causal': causal_df,
        'hlm': hlm_df,
        'missing': missing_df
    }

# 验证函数
def validate_module(module_name, test_func, **kwargs):
    print(f"\n=== 验证 {module_name} 模块 ===")
    try:
        result = test_func(**kwargs)
        if result['success']:
            print(f"✓ {module_name} 模块验证成功")
            # 打印部分结果
            if 'results' in result and result['results']:
                print(f"  结果类型: {type(result['results']).__name__}")
                if isinstance(result['results'], dict):
                    print(f"  结果键: {list(result['results'].keys())[:5]}")
        else:
            print(f"✗ {module_name} 模块验证失败: {result['error']}")
    except Exception as e:
        print(f"✗ {module_name} 模块验证失败: {str(e)}")

# 主验证函数
def main():
    print("开始验证高级统计模块...")
    
    # 生成测试数据
    data = generate_test_data()
    
    # 1. 验证回归模块
    validate_module('linear_regression', linear_regression, 
                   data=data['iris'], 
                   dependent_var='sepal length (cm)', 
                   independent_vars=['sepal width (cm)', 'petal length (cm)'])
    
    validate_module('multiple_linear_regression', multiple_linear_regression, 
                   data=data['iris'], 
                   dependent_var='sepal length (cm)', 
                   independent_vars=['sepal width (cm)', 'petal length (cm)', 'petal width (cm)'])
    
    validate_module('logistic_regression', logistic_regression, 
                   data=data['iris'], 
                   dependent_var='target', 
                   independent_vars=['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)'])
    
    # 2. 验证因子分析模块
    validate_module('exploratory_factor_analysis', exploratory_factor_analysis, 
                   data=data['iris'], 
                   vars=['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)'])
    
    # 3. 验证PCA模块
    validate_module('principal_component_analysis', principal_component_analysis, 
                   data=data['iris'], 
                   vars=['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)'])
    
    # 4. 验证聚类模块
    validate_module('kmeans_clustering', kmeans_clustering, 
                   data=data['cluster'], 
                   vars=['feature1', 'feature2'], 
                   n_clusters=4)
    
    # 5. 验证判别分析模块
    validate_module('discriminant_analysis', discriminant_analysis, 
                   data=data['iris'], 
                   group_var='target', 
                   predictor_vars=['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)'])
    
    # 6. 验证对应分析模块
    # 创建分类数据用于对应分析
    cat_df = pd.DataFrame({
        'cat1': np.random.choice(['A', 'B', 'C'], 100),
        'cat2': np.random.choice(['X', 'Y', 'Z'], 100)
    })
    validate_module('simple_correspondence', simple_correspondence, 
                   data=cat_df, 
                   row_var='cat1', 
                   col_var='cat2')
    
    # 7. 验证信度模块
    validate_module('cronbach_alpha', cronbach_alpha, 
                   data=data['iris'], 
                   vars=['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)'])
    
    # 8. 验证生存分析模块
    # 创建生存数据
    survival_df = pd.DataFrame({
        'time': np.random.exponential(1, 100),
        'event': np.random.randint(0, 2, 100),
        'covariate': np.random.normal(0, 1, 100)
    })
    validate_module('kaplan_meier', kaplan_meier, 
                   data=survival_df, 
                   time_var='time', 
                   event_var='event')
    
    # 9. 验证时间序列模块
    validate_module('acf_pacf', acf_pacf, 
                   data=data['time_series'], 
                   var='value')
    
    # 10. 验证缺失值模块
    validate_module('missing_pattern', missing_pattern, 
                   data=data['missing'])
    
    # 11. 验证对数线性模块
    validate_module('log_linear', log_linear, 
                   data=cat_df, 
                   factors=['cat1', 'cat2'])
    
    # 12. 验证Probit模块
    probit_df = pd.DataFrame({
        'response': np.random.randint(0, 2, 100),
        'dose': np.linspace(0, 10, 100)
    })
    validate_module('probit_analysis', probit_analysis, 
                   data=probit_df, 
                   response_var='response', 
                   dose_var='dose')
    
    # 13. 验证Meta分析模块
    meta_df = pd.DataFrame({
        'effect_size': np.random.normal(0, 0.5, 20),
        'standard_error': np.random.uniform(0.1, 0.3, 20)
    })
    validate_module('meta_analysis', meta_analysis, 
                   data=meta_df, 
                   effect_sizes=meta_df['effect_size'].tolist(), 
                   standard_errors=meta_df['standard_error'].tolist())
    
    # 14. 验证SEM模块
    validate_module('sem_analysis', sem_analysis, 
                   data=data['iris'], 
                   model_spec={'factor1': ['sepal length (cm)', 'sepal width (cm)'], 'factor2': ['petal length (cm)', 'petal width (cm)']})
    
    # 15. 验证贝叶斯模块
    validate_module('bayesian_t_test', bayesian_t_test, 
                   data=data['iris'], 
                   var='sepal length (cm)')
    
    # 16. 验证机器学习模块
    validate_module('random_forest', random_forest, 
                   data=data['iris'], 
                   target_var='target', 
                   feature_vars=['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)'])
    
    # 17. 验证因果推断模块
    validate_module('propensity_score_matching', propensity_score_matching, 
                   data=data['causal'], 
                   treatment_var='treatment', 
                   outcome_var='outcome', 
                   covariates=['covariate1', 'covariate2'])
    
    # 18. 验证HLM模块
    validate_module('hierarchical_linear_model', hierarchical_linear_model, 
                   data=data['hlm'], 
                   dependent_var='dependent_var', 
                   level1_vars=['level1_var1', 'level1_var2'], 
                   level2_vars=['level2_var1'], 
                   group_var='group')
    
    # 19. 验证文本挖掘模块
    validate_module('sentiment_analysis', sentiment_analysis, 
                   data=data['text'], 
                   text_var='text')
    
    # 20. 验证空间模块
    # 创建空间数据和权重矩阵
    spatial_df = pd.DataFrame({
        'value': np.random.normal(0, 1, 10)
    })
    weights = np.ones((10, 10)) - np.eye(10)  # 简单的邻接矩阵
    validate_module('moran_i', moran_i, 
                   data=spatial_df, 
                   var='value', 
                   weights_matrix=weights)
    
    # 21. 验证网络模块
    validate_module('network_analysis', network_analysis, 
                   data=data['network'], 
                   source_var='source', 
                   target_var='target')
    
    # 22. 验证抽样模块
    validate_module('complex_survey_analysis', complex_survey_analysis, 
                   data=data['iris'], 
                   design_vars={'weights': None}, 
                   analysis_type='mean', 
                   analysis_vars={'variable': 'sepal length (cm)'})
    
    print("\n=== 验证完成 ===")

if __name__ == "__main__":
    main()
