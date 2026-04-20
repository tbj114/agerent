# AxaltyX 统计核心库 API 文档（第一部分）

> 版本: 1.0.0 | 版权: TBJ114 | 模块: axaltyx_core

---

## 设计约定

- 所有函数为纯 Python 函数，无 GUI 依赖
- 输入: `numpy.ndarray` 或 `pandas.DataFrame`
- 输出: `dict`，包含计算结果、元数据、状态信息
- 返回 dict 统一结构: `{success: bool, results: dict/Any, warnings: list, error: str|None}`

---

## 1. data_management -- 数据录入与管理

文件路径: `src/axaltyx_core/data_management/`

### 1.1 load_csv

```python
def load_csv(
    path: str,
    encoding: str = "utf-8",
    delimiter: str = ",",
    header: bool = True,
    na_values: list = None
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| path | str | 必填 | CSV 文件绝对路径 |
| encoding | str | "utf-8" | 文件编码（utf-8/gbk/latin1） |
| delimiter | str | "," | 分隔符 |
| header | bool | True | 首行是否为表头 |
| na_values | list | None | 自定义缺失值标记列表 |

**返回值**:

```python
{
    "success": True,
    "results": {
        "data": pd.DataFrame,       # 数据内容
        "columns": list[str],       # 列名列表
        "dtypes": dict,             # {列名: 数据类型}
        "shape": tuple,             # (行数, 列数)
        "missing_count": int,       # 缺失值总数
        "file_size": int            # 文件大小(bytes)
    },
    "warnings": [],
    "error": None
}
```

### 1.2 load_excel

```python
def load_excel(
    path: str,
    sheet_name: str | int | list = 0,
    header: bool = True,
    na_values: list = None
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| path | str | 必填 | Excel 文件路径 |
| sheet_name | str/int/list | 0 | 工作表名或索引 |
| header | bool | True | 首行是否为表头 |
| na_values | list | None | 缺失值标记 |

**返回值**: 同 load_csv 结构，若多表则 results 含 `sheets: dict{sheet_name: DataFrame}`

### 1.3 load_sav

```python
def load_sav(path: str) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| path | str | SPSS .sav 文件路径 |

**返回值**:

```python
{
    "success": True,
    "results": {
        "data": pd.DataFrame,
        "columns": list[str],
        "dtypes": dict,
        "shape": tuple,
        "value_labels": dict,        # {变量名: {数值: 标签}}
        "variable_labels": dict,     # {变量名: 变量标签}
        "missing_values": dict,      # {变量名: 缺失值定义}
        "measure": dict,             # {变量名: 度量类型}
        "file_label": str            # 文件标签
    },
    "warnings": [],
    "error": None
}
```

### 1.4 load_dta

```python
def load_dta(path: str) -> dict
```

**返回值**: 同 load_sav 结构（Stata .dta 格式）

### 1.5 load_json

```python
def load_json(path: str, encoding: str = "utf-8", orient: str = "records") -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| path | str | 必填 | JSON 文件路径 |
| encoding | str | "utf-8" | 编码 |
| orient | str | "records" | 数据方向（records/columns/index） |

**返回值**: 同 load_csv 结构

### 1.6 save_csv

```python
def save_csv(
    data: pd.DataFrame,
    path: str,
    encoding: str = "utf-8",
    delimiter: str = ",",
    index: bool = False,
    na_rep: str = ""
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "path": str,
        "rows": int,
        "columns": int,
        "file_size": int
    },
    "warnings": [],
    "error": None
}
```

### 1.7 save_excel

```python
def save_excel(
    data: pd.DataFrame,
    path: str,
    sheet_name: str = "Sheet1",
    index: bool = False
) -> dict
```

**返回值**: 同 save_csv

### 1.8 save_sav

```python
def save_sav(
    data: pd.DataFrame,
    path: str,
    variable_labels: dict = None,
    value_labels: dict = None
) -> dict
```

**返回值**: 同 save_csv

### 1.9 create_dataset

```python
def create_dataset(rows: int = 100, cols: int = 100) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| rows | int | 100 | 行数 |
| cols | int | 100 | 列数 |

**返回值**:

```python
{
    "success": True,
    "results": {
        "data": pd.DataFrame,    # 100x100 空DataFrame，列名 VAR00001~VAR00100
        "columns": list[str],
        "shape": (100, 100)
    },
    "warnings": [],
    "error": None
}
```

### 1.10 merge_datasets

```python
def merge_datasets(
    left: pd.DataFrame,
    right: pd.DataFrame,
    on: str | list,
    how: str = "inner"
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| left | DataFrame | 必填 | 左表 |
| right | DataFrame | 必填 | 右表 |
| on | str/list | 必填 | 合并键 |
| how | str | "inner" | 合并方式（inner/left/right/outer） |

**返回值**: `{success, results: {data, shape, merge_keys, merged_rows}, warnings, error}`

### 1.11 sort_data

```python
def sort_data(
    data: pd.DataFrame,
    by: str | list,
    ascending: bool | list = True
) -> dict
```

**返回值**: `{success, results: {data, shape, sort_columns}, warnings, error}`

### 1.12 filter_data

```python
def filter_data(data: pd.DataFrame, condition: str) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| data | DataFrame | 原始数据 |
| condition | str | 过滤条件表达式（如 "age > 18 & score < 90"） |

**返回值**: `{success, results: {data, shape, condition, filtered_count}, warnings, error}`

### 1.13 aggregate_data

```python
def aggregate_data(
    data: pd.DataFrame,
    group_by: str | list,
    agg_func: dict
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| group_by | str/list | 分组变量 |
| agg_func | dict | 聚合规则，如 `{"score": ["mean", "std"]}` |

**返回值**: `{success, results: {data, shape, group_by, aggregations}, warnings, error}`

### 1.14 transpose_data

```python
def transpose_data(data: pd.DataFrame) -> dict
```

**返回值**: `{success, results: {data, original_shape, new_shape}, warnings, error}`

### 1.15 reshape_wide

```python
def reshape_wide(
    data: pd.DataFrame,
    id_var: str,
    time_var: str,
    var_name: str,
    value_name: str = "value"
) -> dict
```

**返回值**: `{success, results: {data, shape, id_var, time_points}, warnings, error}`

### 1.16 reshape_long

```python
def reshape_long(
    data: pd.DataFrame,
    stubnames: list,
    id_var: str,
    j: str
) -> dict
```

**返回值**: `{success, results: {data, shape, id_var, j_values}, warnings, error}`

### 1.17 compute_variable

```python
def compute_variable(
    data: pd.DataFrame,
    expression: str,
    new_var: str
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| expression | str | 计算表达式（如 "log(income) + 1"） |
| new_var | str | 新变量名 |

**返回值**: `{success, results: {data, new_var, expression}, warnings, error}`

### 1.18 recode_variable

```python
def recode_variable(
    data: pd.DataFrame,
    var: str,
    rules: dict,
    new_var: str = None
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| rules | dict | 重编码规则，如 `{(0, 18): 1, (18, 60): 2, (60, 120): 3}` |
| new_var | str | 新变量名，None 则覆盖原变量 |

**返回值**: `{success, results: {data, var, mapping, new_var}, warnings, error}`

### 1.19 detect_missing

```python
def detect_missing(data: pd.DataFrame) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "missing_counts": dict,      # {列名: 缺失数}
        "missing_pct": dict,         # {列名: 缺失百分比}
        "total_missing": int,        # 总缺失数
        "total_cells": int,          # 总单元格数
        "missing_rate": float        # 总缺失率
    },
    "warnings": [],
    "error": None
}
```

### 1.20 weight_data

```python
def weight_data(data: pd.DataFrame, weight_var: str) -> dict
```

**返回值**: `{success, results: {data, weight_var, effective_n, design_effect}, warnings, error}`

---

## 2. descriptive -- 描述性统计

文件路径: `src/axaltyx_core/descriptive/`

### 2.1 descriptive_stats

```python
def descriptive_stats(
    data: pd.DataFrame,
    vars: list[str] = None,
    stats: list[str] = None
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| data | DataFrame | 必填 | 输入数据 |
| vars | list[str] | None | 目标变量列表，None 则分析全部数值列 |
| stats | list[str] | None | 统计量列表 |

**可选统计量**:

| stat 名称 | 含义 |
|-----------|------|
| mean | 均值 |
| median | 中位数 |
| mode | 众数 |
| std | 标准差 |
| variance | 方差 |
| min | 最小值 |
| max | 最大值 |
| range | 全距 |
| skewness | 偏度 |
| kurtosis | 峰度 |
| sum | 求和 |
| count | 有效计数 |
| sem | 标准误 |
| cv | 变异系数 |
| percentiles | 百分位数（默认 5/25/50/75/95） |

**返回值**:

```python
{
    "success": True,
    "results": {
        "table": pd.DataFrame,       # 变量 x 统计量 交叉表
        "variables": list[str],      # 分析的变量列表
        "statistics": list[str],     # 使用的统计量列表
        "n_cases": int               # 总个案数
    },
    "warnings": [],
    "error": None
}
```

### 2.2 frequency_table

```python
def frequency_table(
    data: pd.DataFrame,
    var: str,
    sort: str = "value",
    cumulative: bool = True
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| var | str | 必填 | 目标变量 |
| sort | str | "value" | 排序方式（value/frequency/descending） |
| cumulative | bool | True | 是否计算累积百分比 |

**返回值**:

```python
{
    "success": True,
    "results": {
        "frequencies": pd.DataFrame,  # 值/频次/百分比/有效百分比
        "cumulative": pd.DataFrame,   # 累积频次/累积百分比
        "valid_n": int,               # 有效N
        "missing_n": int,             # 缺失N
        "total_n": int,               # 总N
        "n_categories": int           # 类别数
    },
    "warnings": [],
    "error": None
}
```

### 2.3 cross_tabulation

```python
def cross_tabulation(
    data: pd.DataFrame,
    row_var: str,
    col_var: str,
    expected: bool = False,
    percentages: str = "none"
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| row_var | str | 必填 | 行变量 |
| col_var | str | 必填 | 列变量 |
| expected | bool | False | 是否计算期望频数 |
| percentages | str | "none" | 百分比类型（none/row/column/total） |

**返回值**:

```python
{
    "success": True,
    "results": {
        "table": pd.DataFrame,        # 交叉频数表
        "row_totals": pd.Series,
        "col_totals": pd.Series,
        "chi2": float,                # 卡方值
        "df": int,                    # 自由度
        "p_value": float,             # p 值
        "expected": pd.DataFrame,     # 期望频数（若 requested）
        "percentages": pd.DataFrame   # 百分比表（若 requested）
    },
    "warnings": [],
    "error": None
}
```

---

## 3. frequency -- 频数分析

文件路径: `src/axaltyx_core/frequency/`

### 3.1 frequencies

```python
def frequencies(
    data: pd.DataFrame,
    vars: list[str],
    format: str = "table",
    order: str = "ascending",
    multiple_responses: bool = False
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| vars | list[str] | 必填 | 分析变量列表 |
| format | str | "table" | 输出格式（table/chart） |
| order | str | "ascending" | 排序方式 |
| multiple_responses | bool | False | 是否为多重响应集 |

**返回值**:

```python
{
    "success": True,
    "results": {
        "tables": dict[str, dict],    # {变量名: frequency_table_result}
        "charts_data": dict,          # 绑图数据
        "summary": dict               # 汇总信息
    },
    "warnings": [],
    "error": None
}
```

### 3.2 multiple_response_frequencies

```python
def multiple_response_frequencies(
    data: pd.DataFrame,
    var_sets: dict,
    dichotomies: dict = None
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| var_sets | dict | 多重响应集定义 `{集名: [变量列表]}` |
| dichotomies | dict | 二分变量定义 `{变量名: 计数值}` |

**返回值**:

```python
{
    "success": True,
    "results": {
        "tables": dict[str, dict],    # 每个响应集的频数表
        "response_rates": dict,       # 响应率
        "total_responses": dict       # 总响应数
    },
    "warnings": [],
    "error": None
}
```

---

## 4. crosstab -- 交叉表与卡方检验

文件路径: `src/axaltyx_core/crosstab/`

### 4.1 crosstabs

```python
def crosstabs(
    data: pd.DataFrame,
    row_var: str,
    col_var: str,
    layer_var: str = None,
    statistics: list[str] = None
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| row_var | str | 必填 | 行变量 |
| col_var | str | 必填 | 列变量 |
| layer_var | str | None | 分层变量 |
| statistics | list[str] | None | 统计量（chi2/phi/cramer_v/lambda/uncertainty/contingency/gamma/kappa/risk/odds_ratio） |

**返回值**:

```python
{
    "success": True,
    "results": {
        "table": pd.DataFrame,
        "expected": pd.DataFrame,
        "percentages": dict,          # {row/col/total: DataFrame}
        "chi2": {"value": float, "df": int, "p": float},
        "phi": float,
        "cramer_v": float,
        "contingency_coefficient": float,
        "lambda": {"symmetric": float, "row": float, "col": float},
        "uncertainty": {"symmetric": float, "row": float, "col": float},
        "gamma": {"value": float, "ase": float, "p": float},
        "risk_ratio": dict,
        "odds_ratio": {"value": float, "ci_lower": float, "ci_upper": float}
    },
    "warnings": [],
    "error": None
}
```

### 4.2 chi_square_test

```python
def chi_square_test(
    data: pd.DataFrame,
    row_var: str,
    col_var: str
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "chi2": float,
        "df": int,
        "p_value": float,
        "expected": pd.DataFrame,
        "residuals": pd.DataFrame,
        "standardized_residuals": pd.DataFrame,
        "cells": int,
        "min_expected": float,
        "warning_small_expected": bool
    },
    "warnings": [],
    "error": None
}
```

### 4.3 mcnemar_test

```python
def mcnemar_test(data: pd.DataFrame, var1: str, var2: str, exact: bool = False) -> dict
```

**返回值**: `{success, results: {statistic, p_value, table, n_discordant}, warnings, error}`

### 4.4 cochran_q_test

```python
def cochran_q_test(data: pd.DataFrame, vars: list[str]) -> dict
```

**返回值**: `{success, results: {q_statistic, df, p_value, n, k, table}, warnings, error}`

---

## 5. means_comparison -- 均值比较

文件路径: `src/axaltyx_core/means_comparison/`

### 5.1 means

```python
def means(
    data: pd.DataFrame,
    dependent_vars: list[str],
    independent_var: str,
    statistics: list[str] = None
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| dependent_vars | list[str] | 因变量列表 |
| independent_var | str | 自变量（分组变量） |
| statistics | list[str] | 统计量（mean/std/variance/n/min/max/kurtosis/skewness/se） |

**返回值**:

```python
{
    "success": True,
    "results": {
        "group_stats": pd.DataFrame,  # 分组统计表
        "anova_table": dict,          # 单因素方差分析表
        "eta_squared": dict,          # {变量名: eta_sq}
        "omega_squared": dict         # {变量名: omega_sq}
    },
    "warnings": [],
    "error": None
}
```

### 5.2 one_sample_t_test

```python
def one_sample_t_test(
    data: pd.DataFrame,
    var: str,
    test_value: float = 0
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "t": float,
        "df": int,
        "p_value": float,
        "mean_diff": float,
        "se": float,
        "ci_lower": float,
        "ci_upper": float,
        "sample_mean": float,
        "sample_std": float,
        "n": int
    },
    "warnings": [],
    "error": None
}
```

### 5.3 independent_samples_t_test

```python
def independent_samples_t_test(
    data: pd.DataFrame,
    test_var: str,
    group_var: str,
    equal_variance: bool = True
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "group_stats": pd.DataFrame,  # 两组统计量
        "levene_test": {"f": float, "p": float},
        "t_equal": {"t": float, "df": int, "p": float, "mean_diff": float, "se": float, "ci": tuple},
        "t_unequal": {"t": float, "df": float, "p": float, "mean_diff": float, "se": float, "ci": tuple},
        "cohens_d": float
    },
    "warnings": [],
    "error": None
}
```

### 5.4 paired_samples_t_test

```python
def paired_samples_t_test(
    data: pd.DataFrame,
    var1: str,
    var2: str
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "pair_stats": pd.DataFrame,  # 配对统计量
        "correlation": float,        # 配对相关系数
        "t": float,
        "df": int,
        "p_value": float,
        "mean_diff": float,
        "se": float,
        "ci_lower": float,
        "ci_upper": float,
        "cohens_d": float
    },
    "warnings": [],
    "error": None
}
```

---

## 6. t_test -- t 检验模块（详细版）

文件路径: `src/axaltyx_core/t_test/`

### 6.1 one_sample_t

```python
def one_sample_t(
    data: pd.DataFrame,
    var: str,
    test_value: float = 0,
    ci_level: float = 0.95
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| var | str | 必填 | 检验变量 |
| test_value | float | 0 | 检验值 |
| ci_level | float | 0.95 | 置信水平 |

**返回值**:

```python
{
    "success": True,
    "results": {
        "t": float,
        "df": int,
        "p_value": float,
        "mean_diff": float,
        "se": float,
        "ci_lower": float,
        "ci_upper": float,
        "cohens_d": float,
        "sample_mean": float,
        "sample_std": float,
        "n": int,
        "ci_level": float
    },
    "warnings": [],
    "error": None
}
```

### 6.2 independent_t

```python
def independent_t(
    data: pd.DataFrame,
    test_var: str,
    group_var: str,
    group1: str = None,
    group2: str = None,
    equal_var: bool = True,
    ci_level: float = 0.95
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| test_var | str | 必填 | 检验变量 |
| group_var | str | 必填 | 分组变量 |
| group1 | str | None | 第一组值（None 取前两个唯一值） |
| group2 | str | None | 第二组值 |
| equal_var | bool | True | 是否假设方差齐性 |
| ci_level | float | 0.95 | 置信水平 |

**返回值**:

```python
{
    "success": True,
    "results": {
        "group_stats": {
            "group1": {"n": int, "mean": float, "std": float, "se": float},
            "group2": {"n": int, "mean": float, "std": float, "se": float}
        },
        "levene_test": {"f": float, "df1": int, "df2": int, "p": float},
        "t_test": {
            "t": float,
            "df": float,
            "p_value": float,
            "mean_diff": float,
            "se_diff": float,
            "ci_lower": float,
            "ci_upper": float,
            "equal_variance_assumed": bool
        },
        "effect_size": {
            "cohens_d": float,
            "hedges_g": float,
            "glass_delta": float
        },
        "ci_level": float
    },
    "warnings": [],
    "error": None
}
```

### 6.3 paired_t

```python
def paired_t(
    data: pd.DataFrame,
    var1: str,
    var2: str,
    ci_level: float = 0.95
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "pair_stats": {
            "var1": {"mean": float, "std": float, "se": float, "n": int},
            "var2": {"mean": float, "std": float, "se": float, "n": int},
            "diff": {"mean": float, "std": float, "se": float, "n": int}
        },
        "correlation": {"r": float, "p": float},
        "t_test": {
            "t": float,
            "df": int,
            "p_value": float,
            "mean_diff": float,
            "se_diff": float,
            "ci_lower": float,
            "ci_upper": float
        },
        "effect_size": {"cohens_d": float},
        "ci_level": float
    },
    "warnings": [],
    "error": None
}
```

---

## 7. anova -- 方差分析

文件路径: `src/axaltyx_core/anova/`

### 7.1 one_way_anova

```python
def one_way_anova(
    data: pd.DataFrame,
    dependent_var: str,
    factor_var: str,
    post_hoc: str = None,
    effect_size: bool = True
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| dependent_var | str | 必填 | 因变量 |
| factor_var | str | 必填 | 因子变量 |
| post_hoc | str | None | 事后检验（tukey/bonferroni/scheffe/games_howell/dunnett_t3/tamhane_t2） |
| effect_size | bool | True | 是否计算效应量 |

**返回值**:

```python
{
    "success": True,
    "results": {
        "descriptives": pd.DataFrame,     # 各组描述统计
        "anova_table": {
            "ss_between": float,
            "ss_within": float,
            "ss_total": float,
            "df_between": int,
            "df_within": int,
            "ms_between": float,
            "ms_within": float,
            "f": float,
            "p": float
        },
        "effect_sizes": {
            "eta_squared": float,
            "omega_squared": float,
            "partial_eta_squared": float
        },
        "post_hoc": {                     # 若 requested
            "method": str,
            "comparisons": pd.DataFrame,  # 组间比较表
            "homogeneous_subsets": list   # 齐性子集
        },
        "test_homogeneity": {"levene_f": float, "df1": int, "df2": int, "p": float},
        "means_plot_data": dict           # 均值图数据
    },
    "warnings": [],
    "error": None
}
```

### 7.2 two_way_anova

```python
def two_way_anova(
    data: pd.DataFrame,
    dependent_var: str,
    factor_a: str,
    factor_b: str,
    interaction: bool = True,
    post_hoc: str = None
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "descriptives": pd.DataFrame,
        "anova_table": {
            "factor_a": {"ss": float, "df": int, "ms": float, "f": float, "p": float, "eta_sq": float},
            "factor_b": {"ss": float, "df": int, "ms": float, "f": float, "p": float, "eta_sq": float},
            "interaction": {"ss": float, "df": int, "ms": float, "f": float, "p": float, "eta_sq": float},
            "error": {"ss": float, "df": int, "ms": float},
            "total": {"ss": float, "df": int}
        },
        "interaction_effect": {"present": bool, "effect_size": float},
        "post_hoc": dict,
        "means_plot_data": dict,
        "interaction_plot_data": dict
    },
    "warnings": [],
    "error": None
}
```

### 7.3 repeated_measures_anova

```python
def repeated_measures_anova(
    data: pd.DataFrame,
    dependent_vars: list[str],
    subject_var: str = None,
    sphericity: bool = True,
    corrections: list[str] = None
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| dependent_vars | list[str] | 必填 | 重复测量变量列表 |
| subject_var | str | None | 被试ID变量 |
| sphericity | bool | True | 是否假设球形性 |
| corrections | list[str] | None | 球形性校正方法（greenhouse_geisser/huynh_feldt/lower_bound） |

**返回值**:

```python
{
    "success": True,
    "results": {
        "descriptives": pd.DataFrame,
        "within_subjects": {
            "ss": float, "df": int, "ms": float, "f": float, "p": float,
            "greenhouse_geisser": {"epsilon": float, "ss": float, "df": float, "f": float, "p": float},
            "huynh_feldt": {"epsilon": float, "ss": float, "df": float, "f": float, "p": float}
        },
        "between_subjects": {"ss": float, "df": int, "ms": float},
        "error": {"ss": float, "df": int, "ms": float},
        "mauchly_test": {"w": float, "p": float, "df": int},
        "post_hoc": dict,
        "means_plot_data": dict
    },
    "warnings": [],
    "error": None
}
```

### 7.4 ancova

```python
def ancova(
    data: pd.DataFrame,
    dependent_var: str,
    covariate_vars: list[str],
    factor_var: str
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "anova_table": {
            "covariates": {var: {"ss": float, "f": float, "p": float} for var in covariate_vars},
            "factor": {"ss": float, "df": int, "ms": float, "f": float, "p": float},
            "error": {"ss": float, "df": int, "ms": float},
            "total": {"ss": float, "df": int}
        },
        "adjusted_means": pd.DataFrame,
        "effect_sizes": dict,
        "regression_coefficients": pd.DataFrame
    },
    "warnings": [],
    "error": None
}
```

### 7.5 manova

```python
def manova(
    data: pd.DataFrame,
    dependent_vars: list[str],
    factor_var: str
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "multivariate_tests": {
            "wilks_lambda": {"value": float, "f": float, "df1": float, "df2": float, "p": float},
            "pillai_trace": {"value": float, "f": float, "df1": float, "df2": float, "p": float},
            "hotelling_lawley": {"value": float, "f": float, "df1": float, "df2": float, "p": float},
            "roys_largest_root": {"value": float, "f": float, "df1": float, "df2": float, "p": float}
        },
        "between_subjects_tests": pd.DataFrame,
        "descriptives": pd.DataFrame
    },
    "warnings": [],
    "error": None
}
```

---

## 8. nonparametric -- 非参数检验

文件路径: `src/axaltyx_core/nonparametric/`

### 8.1 mann_whitney_u

```python
def mann_whitney_u(
    data: pd.DataFrame,
    var: str,
    group_var: str,
    group1: str = None,
    group2: str = None,
    exact: bool = False,
    continuity: bool = True
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "u": float,
        "z": float,
        "p_value": float,
        "rank_sum_group1": float,
        "rank_sum_group2": float,
        "mean_rank_group1": float,
        "mean_rank_group2": float,
        "n_group1": int,
        "n_group2": int,
        "effect_size_r": float
    },
    "warnings": [],
    "error": None
}
```

### 8.2 wilcoxon_signed_rank

```python
def wilcoxon_signed_rank(
    data: pd.DataFrame,
    var1: str,
    var2: str = None,
    zero_method: str = "wilcox"
) -> dict
```

**返回值**: `{success, results: {w, z, p_value, n_positive_ranks, n_negative_ranks, n_ties, mean_rank_positive, mean_rank_negative, effect_size_r}, warnings, error}`

### 8.3 kruskal_wallis

```python
def kruskal_wallis(
    data: pd.DataFrame,
    var: str,
    group_var: str,
    post_hoc: str = None
) -> dict
```

**返回值**:

```python
{
    "success": True,
    "results": {
        "h": float,
        "df": int,
        "p_value": float,
        "mean_ranks": dict,
        "group_n": dict,
        "post_hoc": dict,
        "effect_size_eta_sq": float
    },
    "warnings": [],
    "error": None
}
```

### 8.4 friedman_test

```python
def friedman_test(
    data: pd.DataFrame,
    vars: list[str],
    post_hoc: str = None
) -> dict
```

**返回值**: `{success, results: {chi2, df, p_value, mean_ranks, post_hoc, kendall_w}, warnings, error}`

### 8.5 chi_square_goodness_of_fit

```python
def chi_square_goodness_of_fit(
    data: pd.DataFrame,
    var: str,
    expected: list[float] | str = "uniform"
) -> dict
```

**返回值**: `{success, results: {chi2, df, p_value, observed, expected, residuals}, warnings, error}`

### 8.6 kolmogorov_smirnov_test

```python
def kolmogorov_smirnov_test(
    data: pd.DataFrame,
    var: str,
    dist: str = "norm"
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| dist | str | "norm" | 参考分布（norm/exponential/uniform/poisson） |

**返回值**: `{success, results: {statistic, p_value, parameters, dist_name}, warnings, error}`

### 8.7 shapiro_wilk_test

```python
def shapiro_wilk_test(data: pd.DataFrame, var: str) -> dict
```

**返回值**: `{success, results: {w, p_value, normality: bool, alpha: float}, warnings, error}`

### 8.8 runs_test

```python
def runs_test(data: pd.DataFrame, var: str, cutoff: float | str = "median") -> dict
```

**返回值**: `{success, results: {n_runs, n1, n2, z, p_value, cutoff_value}, warnings, error}`

### 8.9 binomial_test

```python
def binomial_test(
    data: pd.DataFrame,
    var: str,
    test_prop: float = 0.5,
    alternative: str = "two-sided"
) -> dict
```

**返回值**: `{success, results: {proportion, n, p_value, ci_lower, ci_upper, test_prop}, warnings, error}`

### 8.10 moses_extreme_reactions

```python
def moses_extreme_reactions(data: pd.DataFrame, var: str, group_var: str) -> dict
```

**返回值**: `{success, results: {observed_span, expected_span, p_value, outliers_removed}, warnings, error}`

### 8.11 spearman_rank

```python
def spearman_rank(data: pd.DataFrame, var1: str, var2: str) -> dict
```

**返回值**: `{success, results: {rho, p_value, n, ci_lower, ci_upper}, warnings, error}`

### 8.12 kendall_tau

```python
def kendall_tau(data: pd.DataFrame, var1: str, var2: str, variant: str = "b") -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| variant | str | "b" | 变体（a/b/c） |

**返回值**: `{success, results: {tau, p_value, n, ci_lower, ci_upper}, warnings, error}`
