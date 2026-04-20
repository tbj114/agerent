# AxaltyX 统计核心库 API 文档（第二部分）

> 版本: 1.0.0 | 版权: TBJ114 | 模块: axaltyx_core（高级统计模块）

---

## 9. correlation -- 相关分析

文件路径: `src/axaltyx_core/correlation/`

### 9.1 pearson_correlation

```python
def pearson_correlation(
    data: pd.DataFrame,
    vars: list[str],
    two_tailed: bool = True
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "correlation_matrix": pd.DataFrame,   # 相关系数矩阵
        "p_value_matrix": pd.DataFrame,       # p值矩阵
        "n_matrix": pd.DataFrame,             # 样本量矩阵
        "ci_lower_matrix": pd.DataFrame,      # 置信区间下限
        "ci_upper_matrix": pd.DataFrame       # 置信区间上限
    },
    "warnings": [],
    "error": None
}
```

### 9.2 partial_correlation

```python
def partial_correlation(
    data: pd.DataFrame,
    var1: str,
    var2: str,
    control_vars: list[str]
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "partial_r": float,
        "partial_r_squared": float,
        "t": float,
        "df": int,
        "p_value": float,
        "ci_lower": float,
        "ci_upper": float,
        "zero_order_r": float,
        "control_vars": list[str]
    },
    "warnings": [],
    "error": None
}
```

### 9.3 canonical_correlation

```python
def canonical_correlation(
    data: pd.DataFrame,
    set_x: list[str],
    set_y: list[str]
) -> dict
```

**返回值**: `{success, results: {canonical_correlations, wilks_lambda, chi2, df, p, structure_coefficients, standardized_coefficients}, warnings, error}`

---

## 10. regression -- 回归分析

文件路径: `src/axaltyx_core/regression/`

### 10.1 linear_regression

```python
def linear_regression(
    data: pd.DataFrame,
    dependent_var: str,
    independent_vars: list[str],
    method: str = "enter",
    ci_level: float = 0.95
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| dependent_var | str | 必填 | 因变量 |
| independent_vars | list[str] | 必填 | 自变量列表 |
| method | str | "enter" | 变量进入方法（enter/stepwise/forward/backward） |
| ci_level | float | 0.95 | 置信水平 |

**返回值**:

```python
{
    "success": True,
    "results": {
        "model_summary": {
            "r": float,
            "r_squared": float,
            "adjusted_r_squared": float,
            "std_error": float,
            "f": float,
            "df1": int,
            "df2": int,
            "p_value": float,
            "n": int
        },
        "coefficients": pd.DataFrame,       # B, SE, Beta, t, p, CI
        "residuals": {
            "min": float, "max": float, "mean": float, "std": float,
            "durbin_watson": float
        },
        "collinearity": {
            "tolerance": dict,
            "vif": dict
        },
        "predictions": pd.DataFrame,       # 预测值、残差、标准化残差
        "ci_level": float
    },
    "warnings": [],
    "error": None
}
```

### 10.2 multiple_linear_regression

```python
def multiple_linear_regression(
    data: pd.DataFrame,
    dependent_var: str,
    independent_vars: list[str],
    method: str = "stepwise",
    selection_criteria: str = "aic",
    ci_level: float = 0.95
) -> dict
```

**返回值**: 同 linear_regression，额外包含 `model_selection_steps: list[dict]`

### 10.3 logistic_regression

```python
def logistic_regression(
    data: pd.DataFrame,
    dependent_var: str,
    independent_vars: list[str],
    method: str = "enter",
    ci_level: float = 0.95,
    classification_cutoff: float = 0.5
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "model_summary": {
            "n": int, "nagelkerke_r2": float, "cox_snell_r2": float,
            "log_likelihood_initial": float, "log_likelihood_final": float,
            "chi2": float, "df": int, "p_value": float
        },
        "coefficients": pd.DataFrame,       # B, SE, Wald, df, p, Exp(B), CI
        "classification_table": pd.DataFrame,
        "hosmer_lemeshow": {"chi2": float, "df": int, "p": float},
        "roc": {"auc": float, "optimal_cutoff": float},
        "odds_ratios": dict,
        "predictions": pd.DataFrame
    },
    "warnings": [],
    "error": None
}
```

### 10.4 ordinal_regression

```python
def ordinal_regression(
    data: pd.DataFrame,
    dependent_var: str,
    independent_vars: list[str],
    link: str = "logit"
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| link | str | 链接函数（logit/probit/cloglog/negative_log_log） |

**返回值**: `{success, results: {model_fit, coefficients, thresholds, pseudo_r2, test_of_parallel_lines, predictions}, warnings, error}`

### 10.5 nonlinear_regression

```python
def nonlinear_regression(
    data: pd.DataFrame,
    x_var: str,
    y_var: str,
    model: str = "polynomial",
    degree: int = 2,
    equation: str = None
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| model | str | 模型类型（polynomial/exponential/logarithmic/power/sine/custom） |
| degree | int | 多项式阶数 |
| equation | str | 自定义方程（仅 model="custom" 时） |

**返回值**: `{success, results: {parameters, r_squared, adjusted_r_squared, std_error, f, p, anova_table, residuals, predictions, equation_str}, warnings, error}`

### 10.6 curve_estimation

```python
def curve_estimation(
    data: pd.DataFrame,
    x_var: str,
    y_var: str,
    models: list[str] = None
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| models | list[str] | 拟合模型列表（linear/logarithmic/inverse/quadratic/cubic/power/compound/s/exponential/logistic/growth） |

**返回值**: `{success, results: {models: {model_name: {r_squared, f, p, parameters, equation}}, best_fit: str, comparison_table}, warnings, error}`

---

## 11. factor_analysis -- 因子分析

文件路径: `src/axaltyx_core/factor_analysis/`

### 11.1 exploratory_factor_analysis

```python
def exploratory_factor_analysis(
    data: pd.DataFrame,
    vars: list[str],
    n_factors: int | str = "kaiser",
    rotation: str = "varimax",
    extraction: str = "principal_axis",
    max_iter: int = 100
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| n_factors | int/str | "kaiser" | 因子数（整数或 "kaiser"/"parallel"/"scree"） |
| rotation | str | "varimax" | 旋转方法（varimax/quartimax/equamax/promax/oblimin/none） |
| extraction | str | "principal_axis" | 提取方法（principal_axis/ml/pa/minres） |
| max_iter | int | 100 | 最大迭代次数 |

**返回值**:

```python
{
    "success": True,
    "results": {
        "kmo": {"overall": float, "per_variable": dict},
        "bartlett_test": {"chi2": float, "df": int, "p": float},
        "communalities": pd.DataFrame,
        "eigenvalues": pd.DataFrame,        # 特征值、方差百分比、累积百分比
        "factor_loadings": pd.DataFrame,     # 因子载荷矩阵
        "rotated_loadings": pd.DataFrame,    # 旋转后载荷
        "variance_explained": dict,          # 各因子方差解释
        "factor_correlation": pd.DataFrame,  # 因子相关矩阵（斜交旋转）
        "factor_scores": pd.DataFrame,       # 因子得分
        "n_factors": int
    },
    "warnings": [],
    "error": None
}
```

### 11.2 confirmatory_factor_analysis

```python
def confirmatory_factor_analysis(
    data: pd.DataFrame,
    model_spec: dict,
    estimator: str = "ml"
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| model_spec | dict | 模型规格 `{因子名: [变量列表]}` |
| estimator | str | 估计方法（ml/mlm/mlr/gls） |

**返回值**: `{success, results: {loadings, fit_indices, model_chi2, df, p, cfi, tli, rmsea, srmr, aic, bic, standardized_loadings, residuals, modification_indices}, warnings, error}`

---

## 12. pca -- 主成分分析

文件路径: `src/axaltyx_core/pca/`

### 12.1 principal_component_analysis

```python
def principal_component_analysis(
    data: pd.DataFrame,
    vars: list[str] = None,
    n_components: int | float | str = None,
    rotation: str = "varimax",
    standardize: bool = True
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "eigenvalues": pd.DataFrame,
        "loadings": pd.DataFrame,
        "rotated_loadings": pd.DataFrame,
        "variance_explained": dict,
        "cumulative_variance": list,
        "component_scores": pd.DataFrame,
        "kmo": float,
        "n_components": int
    },
    "warnings": [],
    "error": None
}
```

---

## 13. clustering -- 聚类分析

文件路径: `src/axaltyx_core/clustering/`

### 13.1 hierarchical_clustering

```python
def hierarchical_clustering(
    data: pd.DataFrame,
    vars: list[str],
    method: str = "ward",
    metric: str = "euclidean",
    n_clusters: int = None
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| method | str | 链接方法（ward/complete/average/single/centroid/median） |
| metric | str | 距离度量（euclidean/cityblock/cosine/correlation） |
| n_clusters | int | 聚类数（None 则不切割） |

**返回值**: `{success, results: {linkage_matrix, dendrogram_data, clusters, cluster_sizes, distance_matrix, silhouette_score}, warnings, error}`

### 13.2 kmeans_clustering

```python
def kmeans_clustering(
    data: pd.DataFrame,
    vars: list[str],
    n_clusters: int,
    init: str = "k-means++",
    n_init: int = 10,
    max_iter: int = 300,
    standardize: bool = True
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "cluster_centers": pd.DataFrame,
        "cluster_sizes": dict,
        "labels": pd.Series,
        "inertia": float,
        "silhouette_score": float,
        "calinski_harabasz_score": float,
        "davies_bouldin_score": float,
        "n_clusters": int,
        "iterations": int,
        "converged": bool
    },
    "warnings": [],
    "error": None
}
```

### 13.3 two_step_clustering

```python
def two_step_clustering(
    data: pd.DataFrame,
    vars: list[str],
    distance_measure: str = "log_likelihood",
    auto_determine_clusters: bool = True,
    max_clusters: int = 15
) -> dict
```

**返回值**: `{success, results: {clusters, cluster_sizes, cluster_centers, silhouette, bic_ic_table, optimal_n}, warnings, error}`

### 13.4 dbscan_clustering

```python
def dbscan_clustering(
    data: pd.DataFrame,
    vars: list[str],
    eps: float = 0.5,
    min_samples: int = 5
) -> dict
```

**返回值**: `{success, results: {labels, n_clusters, n_noise, cluster_sizes, core_samples}, warnings, error}`

---

## 14. discriminant -- 判别分析

文件路径: `src/axaltyx_core/discriminant/`

### 14.1 discriminant_analysis

```python
def discriminant_analysis(
    data: pd.DataFrame,
    group_var: str,
    predictor_vars: list[str],
    method: str = "simultaneous",
    priors: str = "equal"
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "eigenvalues": pd.DataFrame,
        "wilks_lambda": pd.DataFrame,
        "canonical_functions": pd.DataFrame,
        "structure_matrix": pd.DataFrame,
        "standardized_coefficients": pd.DataFrame,
        "classification_functions": pd.DataFrame,
        "classification_table": pd.DataFrame,
        "cross_validated_table": pd.DataFrame,
        "group_statistics": pd.DataFrame,
        "hit_ratio": float
    },
    "warnings": [],
    "error": None
}
```

---

## 15. correspondence -- 对应分析

文件路径: `src/axaltyx_core/correspondence/`

### 15.1 simple_correspondence

```python
def simple_correspondence(
    data: pd.DataFrame,
    row_var: str,
    col_var: str,
    n_dimensions: int = 2,
    standardization: str = "principal"
) -> dict
```

**返回值**: `{success, results: {row_scores, col_scores, singular_values, inertia, chi2, row_profiles, col_profiles, plot_data}, warnings, error}`

### 15.2 multiple_correspondence

```python
def multiple_correspondence(
    data: pd.DataFrame,
    vars: list[str],
    n_dimensions: int = 2
) -> dict
```

**返回值**: `{success, results: {category_scores, inertia, eigenvalues, contribution, plot_data}, warnings, error}`

---

## 16. reliability -- 信度效度分析

文件路径: `src/axaltyx_core/reliability/`

### 16.1 cronbach_alpha

```python
def cronbach_alpha(data: pd.DataFrame, vars: list[str]) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "alpha": float,
        "standardized_alpha": float,
        "n_items": int,
        "item_statistics": pd.DataFrame,    # 删除该项后的alpha、校正项总相关
        "item_total_correlations": dict,
        "alpha_if_deleted": dict,
        "scale_statistics": {"mean": float, "variance": float, "std": float, "n": int}
    },
    "warnings": [],
    "error": None
}
```

### 16.2 split_half_reliability

```python
def split_half_reliability(data: pd.DataFrame, vars: list[str]) -> dict
```

**返回值**: `{success, results: {spearman_brown, guttman_split_half, r_half, n_items}, warnings, error}`

### 16.3 test_retest_reliability

```python
def test_retest_reliability(data: pd.DataFrame, var1: str, var2: str) -> dict
```

**返回值**: `{success, results: {icc, ci_lower, ci_upper, pearson_r, p_value}, warnings, error}`

### 16.4 validity_analysis

```python
def validity_analysis(
    data: pd.DataFrame,
    vars: list[str],
    construct_var: str = None
) -> dict
```

**返回值**: `{success, results: {content_validity, criterion_validity, construct_validity, convergent_validity, discriminant_validity, factor_loadings, ave, cr}, warnings, error}`

---

## 17. survival -- 生存分析

文件路径: `src/axaltyx_core/survival/`

### 17.1 kaplan_meier

```python
def kaplan_meier(
    data: pd.DataFrame,
    time_var: str,
    event_var: str,
    group_var: str = None,
    conf_level: float = 0.95
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "survival_table": pd.DataFrame,    # 时间、风险数、事件数、生存率、SE、CI
        "median_survival": dict,           # {组: 中位生存时间}
        "log_rank_test": {"chi2": float, "df": int, "p": float} if group_var else None,
        "plot_data": dict,
        "conf_level": float
    },
    "warnings": [],
    "error": None
}
```

### 17.2 cox_regression

```python
def cox_regression(
    data: pd.DataFrame,
    time_var: str,
    event_var: str,
    covariates: list[str],
    method: str = "enter",
    ci_level: float = 0.95
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "model_summary": {"n", "events", "log_likelihood", "overall_chi2", "df", "p"},
        "coefficients": pd.DataFrame,     # B, SE, Wald, p, HR, CI
        "omnibus_test": dict,
        "variables_in_model": list,
        "baseline_survival": pd.DataFrame,
        "proportional_hazards_test": dict
    },
    "warnings": [],
    "error": None
}
```

---

## 18. time_series -- 时间序列分析

文件路径: `src/axaltyx_core/time_series/`

### 18.1 acf_pacf

```python
def acf_pacf(
    data: pd.DataFrame,
    var: str,
    nlags: int = 40,
    alpha: float = 0.05
) -> dict
```

**返回值**: `{success, results: {acf_values, acf_ci, pacf_values, pacf_ci, nlags, significant_lags}, warnings, error}`

### 18.2 arima

```python
def arima(
    data: pd.DataFrame,
    var: str,
    order: tuple = (1, 1, 1),
    seasonal_order: tuple = None,
    forecast_steps: int = 10
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "model": {"order", "aic", "bic", "hqic"},
        "coefficients": pd.DataFrame,
        "residuals": {"mean", "std", "ljung_box", "p"},
        "fitted_values": pd.Series,
        "forecast": {"values": list, "ci_lower": list, "ci_upper": list},
        "diagnostics": dict
    },
    "warnings": [],
    "error": None
}
```

### 18.3 exponential_smoothing

```python
def exponential_smoothing(
    data: pd.DataFrame,
    var: str,
    trend: str = "add",
    seasonal: str = None,
    seasonal_periods: int = None,
    damped_trend: bool = False,
    forecast_steps: int = 10
) -> dict
```

**返回值**: `{success, results: {fitted, forecast, residuals, smoothing_parameters, aic, bic, mape, mase}, warnings, error}`

### 18.4 decompose

```python
def decompose(
    data: pd.DataFrame,
    var: str,
    period: int,
    model: str = "additive"
) -> dict
```

**返回值**: `{success, results: {trend, seasonal, residual, observed, plot_data}, warnings, error}`

---

## 19. missing_data -- 缺失值处理

文件路径: `src/axaltyx_core/missing_data/`

### 19.1 missing_pattern

```python
def missing_pattern(data: pd.DataFrame) -> dict
```

**返回值**: `{success, results: {pattern_table, missing_per_variable, missing_per_case, little_mcar_test}, warnings, error}`

### 19.2 em_imputation

```python
def em_imputation(data: pd.DataFrame, vars: list[str], max_iter: int = 100) -> dict
```

**返回值**: `{success, results: {imputed_data, convergence, iterations, missing_filled}, warnings, error}`

### 19.3 multiple_imputation

```python
def multiple_imputation(
    data: pd.DataFrame,
    m: int = 5,
    max_iter: int = 10,
    predictor_vars: list[str] = None
) -> dict
```

**返回值**: `{success, results: {imputed_datasets: list, pooled_estimates, rubin_rules}, warnings, error}`

---

## 20. log_linear -- 对数线性模型

文件路径: `src/axaltyx_core/log_linear/`

### 20.1 log_linear

```python
def log_linear(
    data: pd.DataFrame,
    factors: list[str],
    model: str = "saturated",
    max_iter: int = 100
) -> dict
```

**返回值**: `{success, results: {coefficients, goodness_of_fit, expected_frequencies, residuals, likelihood_ratio, pearson_chi2, df, p}, warnings, error}`

---

## 21. probit -- Probit 分析

文件路径: `src/axaltyx_core/probit/`

### 21.1 probit_analysis

```python
def probit_analysis(
    data: pd.DataFrame,
    response_var: str,
    dose_var: str,
    total_var: str = None
) -> dict
```

**返回值**: `{success, results: {coefficients, ed50, ed90, chi2, p, goodness_of_fit, predicted_probabilities}, warnings, error}`

---

## 22. meta_analysis -- Meta 分析

文件路径: `src/axaltyx_core/meta_analysis/`

### 22.1 meta_analysis

```python
def meta_analysis(
    data: pd.DataFrame,
    effect_sizes: list[float],
    standard_errors: list[float],
    method: str = "random",
    ci_level: float = 0.95
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "overall_effect": {"estimate": float, "ci_lower": float, "ci_upper": float, "z": float, "p": float},
        "heterogeneity": {"q": float, "df": int, "p": float, "i_squared": float, "tau_squared": float, "h": float},
        "forest_plot_data": dict,
        "funnel_plot_data": dict,
        "publication_bias": {"egger_intercept": float, "p": float},
        "sensitivity_analysis": dict,
        "n_studies": int
    },
    "warnings": [],
    "error": None
}
```

---

## 23. sem -- 结构方程模型

文件路径: `src/axaltyx_core/sem/`

### 23.1 sem_analysis

```python
def sem_analysis(
    data: pd.DataFrame,
    model_spec: dict,
    estimator: str = "ml",
    missing: str = "fiml"
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| model_spec | dict | SEM 模型规格（测量模型 + 结构模型） |
| estimator | str | 估计方法（ml/mlm/mlr/gls/uls） |
| missing | str | 缺失值处理（fiml/listwise/pairwise） |

**返回值**:

```python
{
    "success": True,
    "results": {
        "fit_indices": {
            "chi2": float, "df": int, "p": float,
            "cfi": float, "tli": float, "rmsea": float, "srmr": float,
            "aic": float, "bic": float
        },
        "path_coefficients": pd.DataFrame,
        "standardized_coefficients": pd.DataFrame,
        "r_squared": dict,
        "residuals": dict,
        "modification_indices": pd.DataFrame,
        "indirect_effects": dict,
        "total_effects": dict,
        "mediation_tests": dict
    },
    "warnings": [],
    "error": None
}
```

---

## 24. bayesian -- 贝叶斯统计

文件路径: `src/axaltyx_core/bayesian/`

### 24.1 bayesian_t_test

```python
def bayesian_t_test(
    data: pd.DataFrame,
    var: str,
    group_var: str = None,
    test_value: float = 0,
    prior_scale: float = 0.707,
    n_samples: int = 10000
) -> dict
```

**返回值**: `{success, results: {bayes_factor, posterior_mean, posterior_sd, credible_interval, prior, likelihood, effect_size}, warnings, error}`

### 24.2 bayesian_linear_regression

```python
def bayesian_linear_regression(
    data: pd.DataFrame,
    dependent_var: str,
    independent_vars: list[str],
    prior_type: str = "default",
    n_samples: int = 10000,
    n_chains: int = 4
) -> dict
```

**返回值**: `{success, results: {posterior_coefficients, credible_intervals, r_squared, bayes_factor, model_comparison, trace_data, convergence_diagnostics}, warnings, error}`

### 24.3 bayesian_anova

```python
def bayesian_anova(
    data: pd.DataFrame,
    dependent_var: str,
    factor_var: str,
    n_samples: int = 10000
) -> dict
```

**返回值**: `{success, results: {bayes_factor, posterior_means, credible_intervals, effect_sizes, inclusion_probabilities}, warnings, error}`

---

## 25. machine_learning -- 机器学习算法

文件路径: `src/axaltyx_core/machine_learning/`

### 25.1 random_forest

```python
def random_forest(
    data: pd.DataFrame,
    target_var: str,
    feature_vars: list[str],
    task: str = "classification",
    n_estimators: int = 100,
    max_depth: int = None,
    test_size: float = 0.3,
    cv_folds: int = 5
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "model_params": dict,
        "feature_importance": pd.DataFrame,
        "performance": {
            "accuracy": float, "precision": float, "recall": float, "f1": float,
            "auc": float, "confusion_matrix": list
        },
        "cv_results": dict,
        "oob_score": float,
        "predictions": pd.Series
    },
    "warnings": [],
    "error": None
}
```

### 25.2 support_vector_machine

```python
def support_vector_machine(
    data: pd.DataFrame,
    target_var: str,
    feature_vars: list[str],
    kernel: str = "rbf",
    cv_folds: int = 5
) -> dict
```

**返回值**: `{success, results: {model_params, performance, cv_results, support_vectors_count, predictions}, warnings, error}`

### 25.3 gradient_boosting

```python
def gradient_boosting(
    data: pd.DataFrame,
    target_var: str,
    feature_vars: list[str],
    task: str = "classification",
    n_estimators: int = 100,
    learning_rate: float = 0.1,
    max_depth: int = 3,
    cv_folds: int = 5
) -> dict
```

**返回值**: `{success, results: {model_params, feature_importance, performance, cv_results, predictions}, warnings, error}`

### 25.4 neural_network

```python
def neural_network(
    data: pd.DataFrame,
    target_var: str,
    feature_vars: list[str],
    hidden_layers: list[int] = None,
    activation: str = "relu",
    max_iter: int = 200,
    cv_folds: int = 5
) -> dict
```

**返回值**: `{success, results: {architecture, performance, cv_results, loss_curve, predictions}, warnings, error}`

### 25.5 lasso_regression

```python
def lasso_regression(
    data: pd.DataFrame,
    dependent_var: str,
    independent_vars: list[str],
    alpha: float = 1.0,
    cv_folds: int = 5
) -> dict
```

**返回值**: `{success, results: {coefficients, nonzero_count, best_alpha, cv_results, r_squared, predictions}, warnings, error}`

### 25.6 ridge_regression

```python
def ridge_regression(
    data: pd.DataFrame,
    dependent_var: str,
    independent_vars: list[str],
    alpha: float = 1.0,
    cv_folds: int = 5
) -> dict
```

**返回值**: `{success, results: {coefficients, best_alpha, cv_results, r_squared, predictions}, warnings, error}`

### 25.7 elastic_net

```python
def elastic_net(
    data: pd.DataFrame,
    dependent_var: str,
    independent_vars: list[str],
    alpha: float = 1.0,
    l1_ratio: float = 0.5,
    cv_folds: int = 5
) -> dict
```

**返回值**: `{success, results: {coefficients, nonzero_count, best_alpha, best_l1_ratio, cv_results, r_squared, predictions}, warnings, error}`

---

## 26. causal_inference -- 因果推断

文件路径: `src/axaltyx_core/causal_inference/`

### 26.1 propensity_score_matching

```python
def propensity_score_matching(
    data: pd.DataFrame,
    treatment_var: str,
    outcome_var: str,
    covariates: list[str],
    method: str = "nearest",
    caliper: float = 0.2,
    ratio: int = 1
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "matched_data": pd.DataFrame,
        "balance_table": pd.DataFrame,    # 匹配前后标准化差异
        "treatment_effect": {"ate": float, "att": float, "atc": float},
        "propensity_scores": pd.Series,
        "n_matched": int,
        "quality_metrics": dict
    },
    "warnings": [],
    "error": None
}
```

### 26.2 difference_in_differences

```python
def difference_in_differences(
    data: pd.DataFrame,
    outcome_var: str,
    group_var: str,
    time_var: str,
    covariates: list[str] = None
) -> dict
```

**返回值**: `{success, results: {did_estimate, se, ci, p_value, parallel_trend_test, pre_trend, post_trend, plot_data}, warnings, error}`

### 26.3 instrumental_variable

```python
def instrumental_variable(
    data: pd.DataFrame,
    outcome_var: str,
    endogenous_var: str,
    instrument_vars: list[str],
    control_vars: list[str] = None
) -> dict
```

**返回值**: `{success, results: {iv_estimate, first_stage_f, first_stage_p, weak_instrument_test, overid_test, ols_estimate, hausman_test}, warnings, error}`

### 26.4 regression_discontinuity

```python
def regression_discontinuity(
    data: pd.DataFrame,
    outcome_var: str,
    running_var: str,
    cutoff: float,
    bandwidth: float = None,
    kernel: str = "triangular"
) -> dict
```

**返回值**: `{success, results: {rd_estimate, se, ci, p_value, bandwidth_optimal, manipulation_test, plot_data}, warnings, error}`

### 26.5 quantile_regression

```python
def quantile_regression(
    data: pd.DataFrame,
    dependent_var: str,
    independent_vars: list[str],
    quantiles: list[float] = None
) -> dict
```

**返回值**: `{success, results: {coefficients_by_quantile, predictions, plot_data}, warnings, error}`

---

## 27. hlm -- 多层线性模型

文件路径: `src/axaltyx_core/hlm/`

### 27.1 hierarchical_linear_model

```python
def hierarchical_linear_model(
    data: pd.DataFrame,
    dependent_var: str,
    level1_vars: list[str],
    level2_vars: list[str],
    group_var: str,
    random_intercept: bool = True,
    random_slope: list[str] = None
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "fixed_effects": pd.DataFrame,
        "random_effects": pd.DataFrame,
        "variance_components": dict,
        "icc": float,
        "model_fit": {"aic", "bic", "log_likelihood", "n_obs", "n_groups"},
        "reliability": dict
    },
    "warnings": [],
    "error": None
}
```

---

## 28. text_mining -- 文本挖掘

文件路径: `src/axaltyx_core/text_mining/`

### 28.1 sentiment_analysis

```python
def sentiment_analysis(
    data: pd.DataFrame,
    text_var: str,
    method: str = "lexicon",
    language: str = "chinese"
) -> dict
```

**返回值**: `{success, results: {sentiment_scores, distribution, word_frequencies, top_positive, top_negative}, warnings, error}`

### 28.2 text_preprocessing

```python
def text_preprocessing(
    data: pd.DataFrame,
    text_var: str,
    operations: list[str] = None
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| operations | list[str] | 预处理步骤（tokenize/remove_stopwords/stemming/lemmatize/lowercase） |

**返回值**: `{success, results: {processed_text, vocabulary, document_term_matrix}, warnings, error}`

---

## 29. spatial -- 空间计量分析

文件路径: `src/axaltyx_core/spatial/`

### 29.1 moran_i

```python
def moran_i(
    data: pd.DataFrame,
    var: str,
    weights_matrix: np.ndarray
) -> dict
```

**返回值**: `{success, results: {moran_i, expected_i, variance, z_score, p_value, permutation_p}, warnings, error}`

---

## 30. network -- 网络分析

文件路径: `src/axaltyx_core/network/`

### 30.1 network_analysis

```python
def network_analysis(
    data: pd.DataFrame,
    source_var: str,
    target_var: str,
    weight_var: str = None
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "nodes": int,
        "edges": int,
        "density": float,
        "centrality": {"degree": dict, "betweenness": dict, "closeness": dict, "eigenvector": dict},
        "communities": dict,
        "components": int,
        "clustering_coefficient": float,
        "avg_path_length": float
    },
    "warnings": [],
    "error": None
}
```

---

## 31. sampling -- 复杂抽样设计

文件路径: `src/axaltyx_core/sampling/`

### 31.1 complex_survey_analysis

```python
def complex_survey_analysis(
    data: pd.DataFrame,
    design_vars: dict,
    analysis_type: str,
    analysis_vars: dict
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| design_vars | dict | 抽样设计 `{weights, strata, clusters, ids}` |
| analysis_type | str | 分析类型（mean/proportion/total/ratio/logistic_regression） |
| analysis_vars | dict | 分析变量参数 |

**返回值**: `{success, results: {estimate, se, ci, deff, design_effect, effective_n}, warnings, error}`
