import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.datasets import load_iris

# 加载测试数据
def load_test_data():
    # 使用iris数据集
    iris = load_iris()
    data = pd.DataFrame(iris.data, columns=iris.feature_names)
    data['species'] = iris.target
    data['species'] = data['species'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})
    return data

# 测试descriptive模块
def test_descriptive():
    print("\n=== Testing descriptive module ===")
    data = load_test_data()
    
    from axaltyx_core.descriptive.stats import descriptive_stats, frequency_table, cross_tabulation
    
    # 测试descriptive_stats
    result = descriptive_stats(data, vars=['sepal length (cm)', 'sepal width (cm)'])
    print("descriptive_stats:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试frequency_table
    result = frequency_table(data, var='species')
    print("frequency_table:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试cross_tabulation
    result = cross_tabulation(data, row_var='species', col_var='sepal length (cm) > 5.0', 
                           expected=True, percentages='row')
    print("cross_tabulation:", result['success'])
    if not result['success']:
        print("Error:", result['error'])

# 测试frequency模块
def test_frequency():
    print("\n=== Testing frequency module ===")
    data = load_test_data()
    
    from axaltyx_core.frequency.frequency import frequencies, multiple_response_frequencies
    
    # 测试frequencies
    result = frequencies(data, vars=['species'])
    print("frequencies:", result['success'])
    
    # 测试multiple_response_frequencies
    var_sets = {'sepal': ['sepal length (cm)', 'sepal width (cm)']}
    result = multiple_response_frequencies(data, var_sets=var_sets)
    print("multiple_response_frequencies:", result['success'])

# 测试crosstab模块
def test_crosstab():
    print("\n=== Testing crosstab module ===")
    data = load_test_data()
    
    from axaltyx_core.crosstab.crosstab import crosstabs, chi_square_test, mcnemar_test, cochran_q_test
    
    # 测试crosstabs
    result = crosstabs(data, row_var='species', col_var='sepal length (cm) > 5.0')
    print("crosstabs:", result['success'])
    
    # 测试chi_square_test
    result = chi_square_test(data, row_var='species', col_var='sepal length (cm) > 5.0')
    print("chi_square_test:", result['success'])

# 测试means_comparison模块
def test_means_comparison():
    print("\n=== Testing means_comparison module ===")
    data = load_test_data()
    
    from axaltyx_core.means_comparison.means import means, one_sample_t_test, independent_samples_t_test, paired_samples_t_test
    
    # 测试means
    result = means(data, dependent_vars=['sepal length (cm)'], independent_var='species')
    print("means:", result['success'])
    
    # 测试one_sample_t_test
    result = one_sample_t_test(data, var='sepal length (cm)', test_value=5.0)
    print("one_sample_t_test:", result['success'])
    
    # 测试independent_samples_t_test
    result = independent_samples_t_test(data, test_var='sepal length (cm)', group_var='species')
    print("independent_samples_t_test:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试paired_samples_t_test
    result = paired_samples_t_test(data, var1='sepal length (cm)', var2='sepal width (cm)')
    print("paired_samples_t_test:", result['success'])
    if not result['success']:
        print("Error:", result['error'])

# 测试t_test模块
def test_t_test():
    print("\n=== Testing t_test module ===")
    data = load_test_data()
    
    from axaltyx_core.t_test.t_tests import one_sample_t, independent_t, paired_t
    
    # 测试one_sample_t
    result = one_sample_t(data, var='sepal length (cm)', test_value=5.0)
    print("one_sample_t:", result['success'])
    
    # 测试independent_t
    result = independent_t(data, test_var='sepal length (cm)', group_var='species')
    print("independent_t:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试paired_t
    result = paired_t(data, var1='sepal length (cm)', var2='sepal width (cm)')
    print("paired_t:", result['success'])
    if not result['success']:
        print("Error:", result['error'])

# 测试anova模块
def test_anova():
    print("\n=== Testing anova module ===")
    data = load_test_data()
    
    from axaltyx_core.anova.anova import one_way_anova, two_way_anova, repeated_measures_anova, ancova, manova
    
    # 测试one_way_anova
    result = one_way_anova(data, dependent_var='sepal length (cm)', factor_var='species')
    print("one_way_anova:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试two_way_anova
    result = two_way_anova(data, dependent_var='sepal length (cm)', 
                         factor_a='species', factor_b='sepal width (cm) > 3.0')
    print("two_way_anova:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试repeated_measures_anova
    result = repeated_measures_anova(data, dependent_vars=['sepal length (cm)', 'sepal width (cm)'])
    print("repeated_measures_anova:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试ancova
    result = ancova(data, dependent_var='sepal length (cm)', 
                  covariate_vars=['sepal width (cm)'], factor_var='species')
    print("ancova:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试manova
    result = manova(data, dependent_vars=['sepal length (cm)', 'sepal width (cm)'], 
                  factor_var='species')
    print("manova:", result['success'])
    if not result['success']:
        print("Error:", result['error'])

# 测试nonparametric模块
def test_nonparametric():
    print("\n=== Testing nonparametric module ===")
    data = load_test_data()
    
    from axaltyx_core.nonparametric.nonparametric import (
        mann_whitney_u, wilcoxon_signed_rank, kruskal_wallis, friedman_test,
        chi_square_goodness_of_fit, kolmogorov_smirnov_test, shapiro_wilk_test,
        runs_test, binomial_test, moses_extreme_reactions, spearman_rank, kendall_tau
    )
    
    # 测试mann_whitney_u
    result = mann_whitney_u(data, var='sepal length (cm)', group_var='species')
    print("mann_whitney_u:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试wilcoxon_signed_rank
    result = wilcoxon_signed_rank(data, var1='sepal length (cm)', var2='sepal width (cm)')
    print("wilcoxon_signed_rank:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试kruskal_wallis
    result = kruskal_wallis(data, var='sepal length (cm)', group_var='species')
    print("kruskal_wallis:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试friedman_test
    result = friedman_test(data, vars=['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)'])
    print("friedman_test:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试chi_square_goodness_of_fit
    result = chi_square_goodness_of_fit(data, var='species')
    print("chi_square_goodness_of_fit:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试kolmogorov_smirnov_test
    result = kolmogorov_smirnov_test(data, var='sepal length (cm)')
    print("kolmogorov_smirnov_test:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试shapiro_wilk_test
    result = shapiro_wilk_test(data, var='sepal length (cm)')
    print("shapiro_wilk_test:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试runs_test
    result = runs_test(data, var='sepal length (cm)')
    print("runs_test:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试binomial_test
    data['binary'] = (data['sepal length (cm)'] > 5.0).astype(int)
    result = binomial_test(data, var='binary')
    print("binomial_test:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试moses_extreme_reactions
    result = moses_extreme_reactions(data, var='sepal length (cm)', group_var='species')
    print("moses_extreme_reactions:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试spearman_rank
    result = spearman_rank(data, var1='sepal length (cm)', var2='sepal width (cm)')
    print("spearman_rank:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试kendall_tau
    result = kendall_tau(data, var1='sepal length (cm)', var2='sepal width (cm)')
    print("kendall_tau:", result['success'])
    if not result['success']:
        print("Error:", result['error'])

# 测试correlation模块
def test_correlation():
    print("\n=== Testing correlation module ===")
    data = load_test_data()
    
    from axaltyx_core.correlation.correlation import pearson_correlation, partial_correlation, canonical_correlation
    
    # 测试pearson_correlation
    result = pearson_correlation(data, vars=['sepal length (cm)', 'sepal width (cm)'])
    print("pearson_correlation:", result['success'])
    
    # 测试partial_correlation
    result = partial_correlation(data, var1='sepal length (cm)', var2='petal length (cm)', 
                               control_vars=['sepal width (cm)'])
    print("partial_correlation:", result['success'])
    if not result['success']:
        print("Error:", result['error'])
    
    # 测试canonical_correlation
    result = canonical_correlation(data, 
                                 set_x=['sepal length (cm)', 'sepal width (cm)'], 
                                 set_y=['petal length (cm)', 'petal width (cm)'])
    print("canonical_correlation:", result['success'])
    if not result['success']:
        print("Error:", result['error'])

if __name__ == "__main__":
    # 运行所有测试
    test_descriptive()
    test_frequency()
    test_crosstab()
    test_means_comparison()
    test_t_test()
    test_anova()
    test_nonparametric()
    test_correlation()
    print("\n=== All tests completed ===")
