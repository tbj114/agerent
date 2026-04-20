# AxaltyX 绘图引擎 API 文档

> 版本: 1.0.0 | 版权: TBJ114 | 模块: axaltyx_plot

---

## 设计约定

- 所有绘图函数返回 `dict`，包含 `figure` 对象和 `metadata`
- 支持 matplotlib 静态图和 plotly 交互图两种后端
- 统一配色方案遵循 Arco Design 色彩体系
- 支持图表编辑、样式修改、标注添加、多格式导出

---

## 1. basic -- 基础图表

文件路径: `src/axaltyx_plot/basic/`

### 1.1 bar_chart

```python
def bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str = None,
    color: str = None,
    orientation: str = "vertical",
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    figsize: tuple = (10, 6),
    style: str = "arco",
    interactive: bool = False
) -> dict
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| data | DataFrame | 必填 | 数据 |
| x | str | 必填 | X 轴变量 |
| y | str | None | Y 轴变量（None 则计数） |
| color | str | None | 颜色分组变量 |
| orientation | str | "vertical" | 方向（vertical/horizontal） |
| style | str | "arco" | 样式主题（arco/arco_dark/minimal） |
| interactive | bool | False | 是否使用 plotly 交互模式 |

**返回值**:

```python
{
    "success": True,
    "results": {
        "figure": matplotlib.Figure | plotly.Figure,
        "type": "bar_chart",
        "backend": "matplotlib" | "plotly",
        "metadata": {"x", "y", "n_bars", "color_groups"}
    },
    "warnings": [],
    "error": None
}
```

### 1.2 stacked_bar_chart

```python
def stacked_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    stack: str,
    normalize: bool = False,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict
```

### 1.3 grouped_bar_chart

```python
def grouped_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    group: str,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict
```

### 1.4 pie_chart

```python
def pie_chart(
    data: pd.DataFrame,
    labels: str,
    values: str,
    hole: float = 0,
    title: str = "",
    figsize: tuple = (8, 8),
    interactive: bool = False
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| hole | float | 环图孔径（0=饼图, 0.5=环图） |

### 1.5 histogram

```python
def histogram(
    data: pd.DataFrame,
    var: str,
    bins: int | str = "auto",
    kde: bool = True,
    color: str = None,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict
```

### 1.6 density_plot

```python
def density_plot(
    data: pd.DataFrame,
    var: str,
    group_var: str = None,
    fill: bool = True,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict
```

### 1.7 scatter_plot

```python
def scatter_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str = None,
    size: str = None,
    trend_line: str = None,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| trend_line | str | 趋势线类型（linear/quadratic/polynomial/loess） |

### 1.8 line_chart

```python
def line_chart(
    data: pd.DataFrame,
    x: str,
    y: str | list[str],
    group: str = None,
    markers: bool = True,
    fill_area: bool = False,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict
```

### 1.9 area_chart

```python
def area_chart(
    data: pd.DataFrame,
    x: str,
    y: str | list[str],
    stacked: bool = True,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict
```

### 1.10 box_plot

```python
def box_plot(
    data: pd.DataFrame,
    y: str,
    x: str = None,
    group: str = None,
    notch: bool = False,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict
```

### 1.11 violin_plot

```python
def violin_plot(
    data: pd.DataFrame,
    y: str,
    x: str = None,
    group: str = None,
    split: bool = False,
    inner: str = "box",
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict
```

### 1.12 error_bar_chart

```python
def error_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    yerr: str | list = None,
    ci: float = 0.95,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict
```

---

## 2. statistical -- 统计图表

文件路径: `src/axaltyx_plot/statistical/`

### 2.1 pp_plot

```python
def pp_plot(
    data: pd.DataFrame,
    var: str,
    dist: str = "norm",
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict
```

### 2.2 qq_plot

```python
def qq_plot(
    data: pd.DataFrame,
    var: str,
    dist: str = "norm",
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict
```

### 2.3 roc_curve

```python
def roc_curve(
    y_true: np.ndarray,
    y_scores: np.ndarray,
    title: str = "",
    figsize: tuple = (8, 8),
    interactive: bool = False
) -> dict
```

**返回值**: `{success, results: {figure, auc, optimal_threshold, sensitivity, specificity, plot_data}, warnings, error}`

### 2.4 interaction_plot

```python
def interaction_plot(
    data: pd.DataFrame,
    x: str,
    trace: str,
    y: str,
    title: str = "",
    figsize: tuple = (10, 6)
) -> dict
```

### 2.5 means_plot

```python
def means_plot(
    data: pd.DataFrame,
    dependent_var: str,
    factor_var: str,
    error_bars: str = "ci",
    ci_level: float = 0.95,
    title: str = "",
    figsize: tuple = (10, 6)
) -> dict
```

### 2.6 stem_leaf_plot

```python
def stem_leaf_plot(
    data: np.ndarray | pd.Series,
    title: str = ""
) -> dict
```

**返回值**: `{success, results: {text_representation, figure, stem_leaf_dict}, warnings, error}`

### 2.7 pareto_chart

```python
def pareto_chart(
    data: pd.DataFrame,
    category_var: str,
    count_var: str = None,
    title: str = "",
    figsize: tuple = (10, 6)
) -> dict
```

### 2.8 autocorrelation_plot

```python
def autocorrelation_plot(
    data: pd.Series | np.ndarray,
    nlags: int = 40,
    alpha: float = 0.05,
    title: str = "",
    figsize: tuple = (10, 4)
) -> dict
```

### 2.9 partial_autocorrelation_plot

```python
def partial_autocorrelation_plot(
    data: pd.Series | np.ndarray,
    nlags: int = 40,
    alpha: float = 0.05,
    title: str = "",
    figsize: tuple = (10, 4)
) -> dict
```

### 2.10 forest_plot

```python
def forest_plot(
    estimates: list[float],
    ci_lower: list[float],
    ci_upper: list[float],
    labels: list[str] = None,
    overall: dict = None,
    title: str = "",
    figsize: tuple = (10, 8)
) -> dict
```

### 2.11 funnel_plot

```python
def funnel_plot(
    estimates: list[float],
    standard_errors: list[float],
    labels: list[str] = None,
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict
```

---

## 3. advanced -- 高级图表

文件路径: `src/axaltyx_plot/advanced/`

### 3.1 heatmap

```python
def heatmap(
    data: pd.DataFrame | np.ndarray,
    annotation: bool = True,
    cmap: str = "arco_blue",
    cluster_rows: bool = False,
    cluster_cols: bool = False,
    title: str = "",
    figsize: tuple = (10, 8),
    interactive: bool = False
) -> dict
```

### 3.2 matrix_scatter_plot

```python
def matrix_scatter_plot(
    data: pd.DataFrame,
    vars: list[str],
    diagonal: str = "histogram",
    title: str = "",
    figsize: tuple = (10, 10)
) -> dict
```

### 3.3 three_d_scatter

```python
def three_d_scatter(
    data: pd.DataFrame,
    x: str,
    y: str,
    z: str,
    color: str = None,
    title: str = "",
    figsize: tuple = (10, 8),
    interactive: bool = True
) -> dict
```

### 3.4 three_d_surface

```python
def three_d_surface(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    cmap: str = "arco_gradient",
    title: str = "",
    figsize: tuple = (10, 8),
    interactive: bool = True
) -> dict
```

### 3.5 radar_chart

```python
def radar_chart(
    data: pd.DataFrame,
    categories: list[str],
    values: list[float] | dict,
    group_var: str = None,
    fill: bool = True,
    title: str = "",
    figsize: tuple = (8, 8)
) -> dict
```

### 3.6 population_pyramid

```python
def population_pyramid(
    data: pd.DataFrame,
    age_group: str,
    male_var: str,
    female_var: str,
    title: str = "",
    figsize: tuple = (10, 8)
) -> dict
```

### 3.7 dendrogram

```python
def dendrogram(
    linkage_matrix: np.ndarray,
    labels: list[str] = None,
    orientation: str = "top",
    title: str = "",
    figsize: tuple = (12, 8)
) -> dict
```

### 3.8 correspondence_plot

```python
def correspondence_plot(
    row_scores: pd.DataFrame,
    col_scores: pd.DataFrame,
    title: str = "",
    figsize: tuple = (10, 8)
) -> dict
```

### 3.9 word_cloud

```python
def word_cloud(
    text_data: str | list[str],
    max_words: int = 200,
    width: int = 800,
    height: int = 400,
    background_color: str = "white",
    colormap: str = "arco",
    font_path: str = None
) -> dict
```

### 3.10 ridge_plot

```python
def ridge_plot(
    data: pd.DataFrame,
    value_var: str,
    group_var: str,
    title: str = "",
    figsize: tuple = (10, 8)
) -> dict
```

### 3.11 grouped_density_plot

```python
def grouped_density_plot(
    data: pd.DataFrame,
    value_var: str,
    group_var: str,
    title: str = "",
    figsize: tuple = (10, 6)
) -> dict
```

### 3.12 survival_curve

```python
def survival_curve(
    survival_table: pd.DataFrame,
    group_var: str = None,
    ci: bool = True,
    title: str = "",
    figsize: tuple = (10, 6),
    interactive: bool = False
) -> dict
```

### 3.13 multi_panel

```python
def multi_panel(
    figures: list,
    rows: int = 1,
    cols: int = None,
    titles: list[str] = None,
    sharex: bool = False,
    sharey: bool = False,
    figsize: tuple = None,
    suptitle: str = ""
) -> dict
```

---

## 4. interactive -- 交互式图表

文件路径: `src/axaltyx_plot/interactive/`

### 4.1 dynamic_line_chart

```python
def dynamic_line_chart(
    data: pd.DataFrame,
    x: str,
    y: list[str],
    title: str = "",
    width: int = 900,
    height: int = 500
) -> dict
```

**返回值**: `{success, results: {html_path, figure, animation_frames}, warnings, error}`

### 4.2 interactive_scatter

```python
def interactive_scatter(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str = None,
    size: str = None,
    tooltip_vars: list[str] = None,
    title: str = "",
    width: int = 900,
    height: int = 500
) -> dict
```

### 4.3 interactive_boxplot

```python
def interactive_boxplot(
    data: pd.DataFrame,
    y: str,
    x: str = None,
    points: str = "outliers",
    title: str = "",
    width: int = 900,
    height: int = 500
) -> dict
```

### 4.4 dynamic_time_series

```python
def dynamic_time_series(
    data: pd.DataFrame,
    time_var: str,
    value_vars: list[str],
    title: str = "",
    width: int = 1000,
    height: int = 500
) -> dict
```

### 4.5 dynamic_roc_curve

```python
def dynamic_roc_curve(
    y_true: np.ndarray,
    y_scores: np.ndarray,
    title: str = "",
    width: int = 800,
    height: int = 600
) -> dict
```

### 4.6 correlation_network

```python
def correlation_network(
    correlation_matrix: pd.DataFrame,
    threshold: float = 0.3,
    title: str = "",
    width: int = 900,
    height: int = 700
) -> dict
```

### 4.7 sankey_diagram

```python
def sankey_diagram(
    data: pd.DataFrame,
    source: str,
    target: str,
    value: str,
    title: str = "",
    width: int = 900,
    height: int = 600
) -> dict
```

### 4.8 chord_diagram

```python
def chord_diagram(
    matrix: np.ndarray | pd.DataFrame,
    labels: list[str] = None,
    title: str = "",
    width: int = 800,
    height: int = 800
) -> dict
```

### 4.9 sunburst_chart

```python
def sunburst_chart(
    data: pd.DataFrame,
    path: list[str],
    values: str,
    title: str = "",
    width: int = 800,
    height: int = 600
) -> dict
```

### 4.10 treemap

```python
def treemap(
    data: pd.DataFrame,
    names: str,
    values: str,
    parents: str = None,
    title: str = "",
    width: int = 900,
    height: int = 600
) -> dict
```

### 4.11 heatmap_cluster

```python
def heatmap_cluster(
    data: pd.DataFrame,
    cluster_rows: bool = True,
    cluster_cols: bool = True,
    title: str = "",
    width: int = 900,
    height: int = 700
) -> dict
```

---

## 5. export -- 图表导出

文件路径: `src/axaltyx_plot/export/`

### 5.1 export_figure

```python
def export_figure(
    figure,
    path: str,
    format: str = "png",
    dpi: int = 300,
    width: float = None,
    height: float = None,
    transparent: bool = False
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| format | str | 导出格式（png/jpg/svg/pdf/tiff/eps） |
| dpi | int | 分辨率 |
| transparent | bool | 是否透明背景 |

**返回值**: `{success, results: {path, format, file_size, dpi}, warnings, error}`

### 5.2 export_interactive

```python
def export_interactive(
    figure,
    path: str,
    format: str = "html"
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| format | str | 导出格式（html/json） |

**返回值**: `{success, results: {path, format, file_size}, warnings, error}`

### 5.3 apply_style

```python
def apply_style(
    figure,
    theme: str = "arco",
    custom_params: dict = None
) -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| theme | str | 主题（arco/arco_dark/minimal/publication） |
| custom_params | dict | 自定义样式参数 |

**返回值**: `{success, results: {figure, applied_theme, applied_params}, warnings, error}`

### 5.4 add_annotation

```python
def add_annotation(
    figure,
    x: float,
    y: float,
    text: str,
    arrow: bool = False,
    fontsize: int = 12,
    color: str = None
) -> dict
```

**返回值**: `{success, results: {figure, annotation_id}, warnings, error}`

### 5.5 set_chart_title

```python
def set_chart_title(
    figure,
    title: str,
    subtitle: str = "",
    fontsize: int = 16,
    color: str = None
) -> dict
```

**返回值**: `{success, results: {figure}, warnings, error}`
