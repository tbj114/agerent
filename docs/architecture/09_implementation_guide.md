# AxaltyX AI 编程分步实施指南

> 版本: 1.0.0 | 版权: TBJ114 | 编译环境: Windows 11

---

## 总览

本文档为 AI 编程助手（如 Claude）提供逐步实施 AxaltyX 项目的完整指南。每一步明确：做什么、参考哪个文档、生成什么文件、怎么验证。

**核心原则**: 每步仅完成可验证的最小可运行效果，不思考额外功能。

---

## 文档索引

在开始任何 Step 之前，AI 必须先阅读对应的参考文档。所有文档路径基于 `/workspace/AxaltyX/docs/`：

| 文档编号 | 文件路径 | 内容 |
|---------|---------|------|
| DOC-01 | `architecture/01_product_positioning.md` | 产品定位、技术栈、三层架构、文件夹结构、设计原则 |
| DOC-02 | `gui/02_gui_design_specification.md` | GUI 设计规范（色彩/字体/间距/组件/交互/动画） |
| DOC-03 | `api/core/03_core_api_part1.md` | 统计核心库 API Part1（数据管理/描述统计/频数/交叉表/t检验/方差分析/非参数） |
| DOC-04 | `api/core/04_core_api_part2.md` | 统计核心库 API Part2（相关/回归/因子/聚类/生存/贝叶斯/机器学习/因果推断等） |
| DOC-05 | `api/plot/05_plot_api.md` | 绘图引擎 API（基础图表/统计图表/高级图表/交互图表/导出） |
| DOC-06 | `api/gui/06_gui_api.md` | Qt6 GUI 模块 API（主窗口/标签页/自定义组件/对话框/面板/设置） |
| DOC-07 | `api/bridge/07_bridge_api.md` | 通信桥接 API（信号/槽函数/命令系统/事件总线/控制器/分析注册表） |
| DOC-08 | `i18n/08_i18n_design.md` | 国际化 JSON 结构定义 + I18nManager API |
| DOC-09 | `architecture/09_implementation_guide.md` | 本文档（实施指南） |
| IMG-01 | `gui/screenshots/splash_screen_design.jpg` | 启动页设计效果图 |
| IMG-02 | `gui/screenshots/main_window_design.jpg` | 主窗口设计效果图 |

---

## 阶段一: 项目骨架搭建（Step 1-3）

### Step 1: 创建项目目录结构

**参考文档**: 先读 DOC-01（第4节"项目文件夹结构"），按其中定义的目录树创建全部文件夹和 `__init__.py`

**做什么**: 创建全部文件夹和空的 `__init__.py`

**生成文件**:
```
AxaltyX/
  src/
    axaltyx_core/__init__.py
    axaltyx_core/data_management/__init__.py
    axaltyx_core/descriptive/__init__.py
    axaltyx_core/frequency/__init__.py
    axaltyx_core/crosstab/__init__.py
    axaltyx_core/means_comparison/__init__.py
    axaltyx_core/t_test/__init__.py
    axaltyx_core/anova/__init__.py
    axaltyx_core/ancova/__init__.py
    axaltyx_core/rm_anova/__init__.py
    axaltyx_core/nonparametric/__init__.py
    axaltyx_core/correlation/__init__.py
    axaltyx_core/regression/__init__.py
    axaltyx_core/factor_analysis/__init__.py
    axaltyx_core/pca/__init__.py
    axaltyx_core/clustering/__init__.py
    axaltyx_core/discriminant/__init__.py
    axaltyx_core/correspondence/__init__.py
    axaltyx_core/reliability/__init__.py
    axaltyx_core/survival/__init__.py
    axaltyx_core/cox/__init__.py
    axaltyx_core/time_series/__init__.py
    axaltyx_core/missing_data/__init__.py
    axaltyx_core/multiple_response/__init__.py
    axaltyx_core/log_linear/__init__.py
    axaltyx_core/probit/__init__.py
    axaltyx_core/meta_analysis/__init__.py
    axaltyx_core/general_linear_model/__init__.py
    axaltyx_core/sem/__init__.py
    axaltyx_core/bayesian/__init__.py
    axaltyx_core/machine_learning/__init__.py
    axaltyx_core/deep_learning/__init__.py
    axaltyx_core/causal_inference/__init__.py
    axaltyx_core/spatial/__init__.py
    axaltyx_core/network/__init__.py
    axaltyx_core/hlm/__init__.py
    axaltyx_core/bayesian_advanced/__init__.py
    axaltyx_core/high_dimensional/__init__.py
    axaltyx_core/text_mining/__init__.py
    axaltyx_core/sampling/__init__.py
    axaltyx_gui/__init__.py
    axaltyx_gui/main_window/__init__.py
    axaltyx_gui/splash/__init__.py
    axaltyx_gui/tab_system/__init__.py
    axaltyx_gui/custom_widgets/__init__.py
    axaltyx_gui/dialogs/__init__.py
    axaltyx_gui/panels/__init__.py
    axaltyx_gui/toolbar/__init__.py
    axaltyx_gui/statusbar/__init__.py
    axaltyx_gui/table_view/__init__.py
    axaltyx_gui/output_view/__init__.py
    axaltyx_gui/chart_view/__init__.py
    axaltyx_gui/settings/__init__.py
    axaltyx_bridge/__init__.py
    axaltyx_bridge/signals/__init__.py
    axaltyx_bridge/slots/__init__.py
    axaltyx_bridge/commands/__init__.py
    axaltyx_bridge/events/__init__.py
    axaltyx_i18n/__init__.py
    axaltyx_i18n/locales/__init__.py
    axaltyx_i18n/json/__init__.py
    axaltyx_plot/__init__.py
    axaltyx_plot/basic/__init__.py
    axaltyx_plot/statistical/__init__.py
    axaltyx_plot/advanced/__init__.py
    axaltyx_plot/interactive/__init__.py
    axaltyx_plot/export/__init__.py
  configs/
  resources/
  scripts/
  tests/
  main.py
  requirements.txt
  setup.py
  pyproject.toml
```

**验证**: `python -c "import axaltyx_core; import axaltyx_gui; import axaltyx_bridge; import axaltyx_i18n; import axaltyx_plot"` 无报错

---

### Step 2: 创建 requirements.txt 和项目配置

**参考文档**: 先读 DOC-01（第2节"技术栈"），确认依赖版本

**生成文件**:
- `requirements.txt`: PyQt6, numpy, scipy, pandas, scikit-learn, statsmodels, lifelines, matplotlib, plotly, pyecharts, openpyxl, pyreadstat, jieba, torch (可选)
- `pyproject.toml`: 项目元数据、构建配置
- `setup.py`: 安装脚本

**验证**: `pip install -r requirements.txt` 成功

---

### Step 3: 创建 i18n JSON 文件和 I18nManager

**参考文档**: 先读 DOC-08（完整 JSON 结构定义 + I18nManager API），严格按照其中定义的 JSON 结构生成三语言文件

**做什么**: 创建三语言 JSON 文件和 I18nManager 类

**生成文件**:
- `src/axaltyx_i18n/locales/zh_CN.json`
- `src/axaltyx_i18n/locales/en_US.json`
- `src/axaltyx_i18n/locales/ja_JP.json`
- `src/axaltyx_i18n/manager.py` -- I18nManager 类（API 严格遵循 DOC-08 第3节）

**验证**: `python -c "from axaltyx_i18n.manager import I18nManager; m = I18nManager(); m.set_language('zh_CN'); print(m.get_text('app.name'))"` 输出 "AxaltyX"

---

## 阶段二: 核心统计引擎（Step 4-6）

### Step 4: 实现数据管理模块

**参考文档**: 先读 DOC-03（第1节"data_management"），每个函数的签名、参数、返回值必须严格一致

**做什么**: 实现 `axaltyx_core/data_management/` 下的全部 20 个函数

**生成文件**:
- `src/axaltyx_core/data_management/io.py` -- load_csv, load_excel, load_sav, load_dta, load_json, save_csv, save_excel, save_sav（8个函数）
- `src/axaltyx_core/data_management/manipulation.py` -- merge_datasets, sort_data, filter_data, aggregate_data, transpose_data, reshape_wide, reshape_long, compute_variable, recode_variable, detect_missing, weight_data, create_dataset（12个函数）

**验证**:
```python
from axaltyx_core.data_management.manipulation import create_dataset
result = create_dataset(100, 100)
assert result["success"] == True
assert result["results"]["shape"] == (100, 100)
assert len(result["results"]["columns"]) == 100
assert result["results"]["columns"][0] == "VAR00001"
```

---

### Step 5: 实现基础统计模块

**参考文档**: 先读 DOC-03（第2~8节），涵盖 descriptive、frequency、crosstab、means_comparison、t_test、anova、nonparametric、correlation 共 8 个模块

**做什么**: 实现 8 个基础统计模块的全部函数

**生成文件**:
- `src/axaltyx_core/descriptive/stats.py` -- descriptive_stats, frequency_table, cross_tabulation（DOC-03 第2节）
- `src/axaltyx_core/frequency/frequency.py` -- frequencies, multiple_response_frequencies（DOC-03 第3节）
- `src/axaltyx_core/crosstab/crosstab.py` -- crosstabs, chi_square_test, mcnemar_test, cochran_q_test（DOC-03 第4节）
- `src/axaltyx_core/means_comparison/means.py` -- means, one_sample_t_test, independent_samples_t_test, paired_samples_t_test（DOC-03 第5节）
- `src/axaltyx_core/t_test/t_tests.py` -- one_sample_t, independent_t, paired_t（DOC-03 第6节）
- `src/axaltyx_core/anova/anova.py` -- one_way_anova, two_way_anova, repeated_measures_anova, ancova, manova（DOC-03 第7节）
- `src/axaltyx_core/nonparametric/nonparametric.py` -- mann_whitney_u, wilcoxon_signed_rank, kruskal_wallis, friedman_test, chi_square_goodness_of_fit, kolmogorov_smirnov_test, shapiro_wilk_test, runs_test, binomial_test, moses_extreme_reactions, spearman_rank, kendall_tau（DOC-03 第8节）
- `src/axaltyx_core/correlation/correlation.py` -- pearson_correlation, partial_correlation, canonical_correlation（DOC-04 第9节）

**验证**: 每个模块用 scipy 内置数据集验证结果与 scipy/statsmodels 一致

---

### Step 6: 实现高级统计模块

**参考文档**: 先读 DOC-04（第10~31节），涵盖 regression、factor_analysis、pca、clustering、discriminant、correspondence、reliability、survival、time_series、missing_data、log_linear、probit、meta_analysis、sem、bayesian、machine_learning、causal_inference、spatial、network、hlm、text_mining、sampling 共 22 个模块

**做什么**: 实现 22 个高级统计模块的全部函数

**生成文件**: 每个模块一个或多个 `.py` 文件，函数签名严格遵循 DOC-04

| 模块 | 参考文档章节 | 文件路径 |
|------|-------------|---------|
| regression | DOC-04 第10节 | `src/axaltyx_core/regression/regression.py` |
| factor_analysis | DOC-04 第11节 | `src/axaltyx_core/factor_analysis/factor_analysis.py` |
| pca | DOC-04 第12节 | `src/axaltyx_core/pca/pca.py` |
| clustering | DOC-04 第13节 | `src/axaltyx_core/clustering/clustering.py` |
| discriminant | DOC-04 第14节 | `src/axaltyx_core/discriminant/discriminant.py` |
| correspondence | DOC-04 第15节 | `src/axaltyx_core/correspondence/correspondence.py` |
| reliability | DOC-04 第16节 | `src/axaltyx_core/reliability/reliability.py` |
| survival | DOC-04 第17节 | `src/axaltyx_core/survival/survival.py` |
| time_series | DOC-04 第18节 | `src/axaltyx_core/time_series/time_series.py` |
| missing_data | DOC-04 第19节 | `src/axaltyx_core/missing_data/missing.py` |
| log_linear | DOC-04 第20节 | `src/axaltyx_core/log_linear/log_linear.py` |
| probit | DOC-04 第21节 | `src/axaltyx_core/probit/probit.py` |
| meta_analysis | DOC-04 第22节 | `src/axaltyx_core/meta_analysis/meta_analysis.py` |
| sem | DOC-04 第23节 | `src/axaltyx_core/sem/sem.py` |
| bayesian | DOC-04 第24节 | `src/axaltyx_core/bayesian/bayesian.py` |
| machine_learning | DOC-04 第25节 | `src/axaltyx_core/machine_learning/ml.py` |
| causal_inference | DOC-04 第26节 | `src/axaltyx_core/causal_inference/causal.py` |
| hlm | DOC-04 第27节 | `src/axaltyx_core/hlm/hlm.py` |
| text_mining | DOC-04 第28节 | `src/axaltyx_core/text_mining/text_mining.py` |
| spatial | DOC-04 第29节 | `src/axaltyx_core/spatial/spatial.py` |
| network | DOC-04 第30节 | `src/axaltyx_core/network/network.py` |
| sampling | DOC-04 第31节 | `src/axaltyx_core/sampling/sampling.py` |

**验证**: 每个函数用已知数据集验证输出正确性

---

## 阶段三: 绘图引擎（Step 7）

### Step 7: 实现绘图模块

**参考文档**: 先读 DOC-05（全部5个章节），涵盖 basic（第1节）、statistical（第2节）、advanced（第3节）、interactive（第4节）、export（第5节）

**做什么**: 实现 axaltyx_plot 下全部绘图函数

**生成文件**:
- `src/axaltyx_plot/basic/charts.py` -- DOC-05 第1节（12个函数）
- `src/axaltyx_plot/statistical/stat_charts.py` -- DOC-05 第2节（11个函数）
- `src/axaltyx_plot/advanced/advanced_charts.py` -- DOC-05 第3节（13个函数）
- `src/axaltyx_plot/interactive/interactive_charts.py` -- DOC-05 第4节（11个函数）
- `src/axaltyx_plot/export/exporter.py` -- DOC-05 第5节（5个函数）
- `src/axaltyx_plot/themes/arco_theme.py` -- Arco Design 配色主题（参考 DOC-02 第1节色彩体系）

**验证**:
```python
from axaltyx_plot.basic.charts import bar_chart
import pandas as pd
df = pd.DataFrame({"category": ["A","B","C"], "value": [10,20,30]})
result = bar_chart(df, "category", "value")
assert result["success"] == True
assert result["results"]["type"] == "bar_chart"
```

---

## 阶段四: 通信桥接层（Step 8）

### Step 8: 实现 Bridge 层

**参考文档**: 先读 DOC-07（全部6个章节），涵盖 signals（第1节）、slots（第2节）、commands（第3节）、events（第4节）、BridgeController（第5节）、ANALYSIS_REGISTRY（第6节）

**做什么**: 实现信号定义、槽函数、命令系统、事件总线、线程池、控制器

**生成文件**:
- `src/axaltyx_bridge/signals/bridge_signals.py` -- BridgeSignals 类（DOC-07 第1节）
- `src/axaltyx_bridge/slots/data_slots.py` -- DataSlots 类（DOC-07 第2.1节）
- `src/axaltyx_bridge/slots/analysis_slots.py` -- AnalysisSlots 类（DOC-07 第2.2节）
- `src/axaltyx_bridge/slots/chart_slots.py` -- ChartSlots 类（DOC-07 第2.3节）
- `src/axaltyx_bridge/slots/ui_slots.py` -- UISlots 类（DOC-07 第2.4节）
- `src/axaltyx_bridge/commands/commands.py` -- CommandBase 及 7 个子命令类（DOC-07 第3节）
- `src/axaltyx_bridge/commands/history.py` -- CommandHistory（DOC-07 第3.8节）
- `src/axaltyx_bridge/events/event_bus.py` -- EventBus（DOC-07 第4.1节）
- `src/axaltyx_bridge/events/worker.py` -- AnalysisWorker, ThreadPoolManager（DOC-07 第4.2~4.3节）
- `src/axaltyx_bridge/controller.py` -- BridgeController 单例（DOC-07 第5节）
- `src/axaltyx_bridge/registry.py` -- ANALYSIS_REGISTRY（DOC-07 第6节）

**验证**: 单元测试验证信号发射和槽函数调用

---

## 阶段五: GUI 界面（Step 9-16）

### Step 9: 实现启动页和主窗口骨架

**参考文档**:
- 启动页设计: 先看 IMG-01（`gui/screenshots/splash_screen_design.jpg`）+ DOC-02 第2.1节（启动页 ASCII 线框图）
- 主窗口布局: 先看 IMG-02（`gui/screenshots/main_window_design.jpg`）+ DOC-02 第2.2节（主窗口 ASCII 线框图）
- 主窗口 API: 先读 DOC-06 第1节（AxaltyXMainWindow 类定义）
- 标题栏 API: 先读 DOC-06 第4.1节（AxaltyXTitleBar 类定义）
- 启动页 API: 先读 DOC-06 第2节（AxaltyXSplashScreen 类定义）
- 色彩/字体/间距: 先读 DOC-02 第1节（设计语言定义）

**做什么**: 创建无边框窗口 + 自定义标题栏 + 启动页 + 应用入口

**生成文件**:
- `src/axaltyx_gui/splash/splash_screen.py` -- AxaltyXSplashScreen（DOC-06 第2节）
- `src/axaltyx_gui/main_window/main_window.py` -- AxaltyXMainWindow（DOC-06 第1节）
- `src/axaltyx_gui/main_window/title_bar.py` -- AxaltyXTitleBar（DOC-06 第4.1节）
- `main.py` -- 应用入口

**验证**: `python main.py` 显示启动页 -> 主窗口（空白，有标题栏和菜单栏）

---

### Step 10: 实现菜单栏和工具栏

**参考文档**:
- 菜单结构: 先读 DOC-08 第2.3节（menu JSON 结构，定义了全部菜单项文字）
- 工具栏 API: 先读 DOC-06 第7节（AxaltyXToolBar 类定义）
- 快捷键: 先读 DOC-02 第4.1节（快捷键体系）

**做什么**: 实现完整菜单栏（8个菜单）和工具栏，所有文字从 i18n JSON 加载

**生成文件**:
- `src/axaltyx_gui/main_window/menu_bar.py`
- `src/axaltyx_gui/toolbar/toolbar.py`

**验证**: 点击每个菜单项有反应（至少显示通知），快捷键可用

---

### Step 11: 实现标签页系统

**参考文档**:
- 标签页设计: 先读 DOC-02 第2.7节（标签页系统 ASCII 线框图）
- 标签页 API: 先读 DOC-06 第3节（AxaltyXTabWidget、DataTab、VariableTab、OutputTab、SyntaxTab 全部类定义）

**做什么**: 实现数据视图、变量视图、输出视图、语法视图四个标签页

**生成文件**:
- `src/axaltyx_gui/tab_system/tab_widget.py` -- AxaltyXTabWidget（DOC-06 第3.1节）
- `src/axaltyx_gui/tab_system/data_tab.py` -- DataTab（DOC-06 第3.2节）
- `src/axaltyx_gui/tab_system/variable_tab.py` -- VariableTab（DOC-06 第3.3节）
- `src/axaltyx_gui/tab_system/output_tab.py` -- OutputTab（DOC-06 第3.4节）
- `src/axaltyx_gui/tab_system/syntax_tab.py` -- SyntaxTab（DOC-06 第3.5节）

**验证**: 标签页可切换，数据视图显示 100x100 空表格

---

### Step 12: 实现数据表格组件

**参考文档**:
- 表格设计: 先读 DOC-02 第2.5节（数据编辑区 ASCII 线框图 + 表格规格）
- 表格 API: 先读 DOC-06 第4.6节（AxaltyXDataTable 类定义，含全部方法签名）
- 表格右键菜单文字: 先读 DOC-08 第2.5节（table JSON 结构）

**做什么**: 实现 SPSS 式可编辑表格（核心组件）

**生成文件**:
- `src/axaltyx_gui/table_view/data_table.py` -- AxaltyXDataTable（DOC-06 第4.6节）
- `src/axaltyx_gui/table_view/delegate.py` -- 单元格编辑委托
- `src/axaltyx_gui/table_view/model.py` -- 自定义数据模型（支持虚拟滚动）

**验证**:
- 默认显示 100x100 空表格
- 列头为 VAR00001~VAR00100
- 双击列头可编辑变量名
- 单元格可编辑
- 支持选中、复制、粘贴
- 右键菜单可用

---

### Step 13: 实现左侧导航面板和右侧属性面板

**参考文档**:
- 导航面板设计: 先读 DOC-02 第2.4节（左侧导航面板 ASCII 线框图）
- 导航 API: 先读 DOC-06 第6.1节（NavigationPanel 类定义）
- 属性面板设计: 先读 DOC-02 第2.6节（右侧属性面板 ASCII 线框图）
- 属性面板 API: 先读 DOC-06 第6.2节（PropertyPanel 类定义）
- 树形菜单 API: 先读 DOC-06 第4.5节（AxaltyXTreeWidget 类定义）
- 导航文字: 先读 DOC-08 第2.4节（navigation JSON 结构，含全部分析项文字）

**做什么**: 实现图标+文字的树形导航菜单和变量属性面板

**生成文件**:
- `src/axaltyx_gui/panels/navigation_panel.py` -- NavigationPanel（DOC-06 第6.1节）
- `src/axaltyx_gui/panels/property_panel.py` -- PropertyPanel（DOC-06 第6.2节）

**验证**: 点击分析项触发对应对话框打开，属性面板显示选中变量信息

---

### Step 14: 实现分析对话框

**参考文档**:
- 对话框基类 API: 先读 DOC-06 第5.1节（AnalysisDialogBase 类定义）
- 变量选择器 API: 先读 DOC-06 第4.7节（AxaltyXVariableSelector 类定义）
- 对话框通用文字: 先读 DOC-08 第2.6节（dialog JSON 结构）
- 分析对话框专用文字: 先读 DOC-08 第2.7节（analysis JSON 结构）
- 分析注册表: 先读 DOC-07 第6节（ANALYSIS_REGISTRY，定义了每个分析的参数 schema）
- 对话框设计参考: 先读 DOC-02 第2.9节（分析对话框 ASCII 线框图）

**做什么**: 为每个分析模块创建对应对话框

**生成文件**:
- `src/axaltyx_gui/dialogs/base_dialog.py` -- AnalysisDialogBase（DOC-06 第5.1节）
- `src/axaltyx_gui/dialogs/descriptive_dialog.py`
- `src/axaltyx_gui/dialogs/frequency_dialog.py`
- `src/axaltyx_gui/dialogs/crosstabs_dialog.py`
- `src/axaltyx_gui/dialogs/t_test_dialogs.py`
- `src/axaltyx_gui/dialogs/anova_dialogs.py`
- `src/axaltyx_gui/dialogs/regression_dialogs.py`
- `src/axaltyx_gui/dialogs/factor_dialog.py`
- `src/axaltyx_gui/dialogs/clustering_dialog.py`
- `src/axaltyx_gui/dialogs/survival_dialogs.py`
- `src/axaltyx_gui/dialogs/reliability_dialog.py`
- `src/axaltyx_gui/dialogs/correlation_dialog.py`
- `src/axaltyx_gui/dialogs/nonparametric_dialogs.py`
- `src/axaltyx_gui/dialogs/file_dialogs.py` -- 先读 DOC-06 第5.2~5.3节
- `src/axaltyx_gui/dialogs/settings_dialog.py` -- 先读 DOC-06 第5.4节
- `src/axaltyx_gui/dialogs/export_dialog.py` -- 先读 DOC-06 第5.5节

**验证**: 打开描述性统计对话框 -> 选择变量 -> 点击确定 -> 输出视图显示结果

---

### Step 15: 实现输出视图和图表显示

**参考文档**:
- 输出视图设计: 先读 DOC-02 第2.8节（输出视图 ASCII 线框图）
- 输出标签页 API: 先读 DOC-06 第3.4节（OutputTab 类定义）
- 通知文字: 先读 DOC-08 第2.9节（notification JSON 结构）

**做什么**: 输出视图显示分析结果表格和图表

**生成文件**:
- `src/axaltyx_gui/output_view/output_widget.py`
- `src/axaltyx_gui/output_view/result_table.py`
- `src/axaltyx_gui/chart_view/chart_widget.py`

**验证**: 运行分析后，输出视图正确显示结果表格，图表可内嵌显示

---

### Step 16: 实现设置和状态栏

**参考文档**:
- 设置 API: 先读 DOC-06 第9节（AppSettings、ThemeManager 类定义）
- 状态栏 API: 先读 DOC-06 第8节（AxaltyXStatusBar 类定义）
- 设置文字: 先读 DOC-08 第2.8节（settings JSON 结构）
- 状态栏文字: 先读 DOC-08 第2.10节（status JSON 结构）
- 主题色彩: 先读 DOC-02 第1.1节（亮色/暗色模式色板）

**做什么**: 设置对话框（语言/主题/性能）和状态栏

**生成文件**:
- `src/axaltyx_gui/settings/app_settings.py` -- AppSettings（DOC-06 第9.1节）
- `src/axaltyx_gui/settings/theme_manager.py` -- ThemeManager（DOC-06 第9.2节）
- `src/axaltyx_gui/statusbar/status_bar.py` -- AxaltyXStatusBar（DOC-06 第8节）

**验证**: 切换语言后所有 UI 文字更新，切换主题后颜色变化

---

## 阶段六: 集成与打包（Step 17-19）

### Step 17: 端到端集成测试

**参考文档**: 先读 DOC-07（整体通信流程），确认 GUI -> Bridge -> Core 的完整调用链路

**做什么**: 完整流程测试：打开文件 -> 数据编辑 -> 运行分析 -> 查看结果 -> 导出图表

**生成文件**:
- `tests/e2e/test_full_workflow.py`
- `tests/integration/test_bridge.py`
- `tests/unit/test_core/*.py`

**验证**: 全流程无报错，结果正确

---

### Step 18: 创建 QSS 样式表

**参考文档**: 先读 DOC-02（全部设计规范），将色彩/字体/间距/圆角/阴影/动画规范转化为 QSS

**做什么**: 创建亮色和暗色主题的 QSS 样式表

**生成文件**:
- `resources/themes/light/arco_light.qss`
- `resources/themes/dark/arco_dark.qss`

**验证**: 应用样式后界面符合设计规范

---

### Step 19: Windows 安装包打包

**参考文档**: 先读 DOC-01（第2节"技术栈"），确认打包工具链

**做什么**: 使用 PyInstaller 或 cx_Freeze 打包为 Windows 安装包

**生成文件**:
- `scripts/build/build_spec.py` -- PyInstaller spec 文件
- `scripts/packaging/create_installer.py` -- Inno Setup 脚本
- `scripts/install/build.bat` -- 一键构建脚本

**验证**: 在干净的 Windows 11 机器上安装并运行

---

## 阶段七: 文档与发布（Step 20）

### Step 20: 最终文档和发布

**参考文档**: 通读全部 DOC-01 ~ DOC-08，确保用户手册覆盖所有功能

**做什么**: 整理所有文档，创建用户手册

**生成文件**:
- `docs/deployment/user_manual.md`
- `docs/deployment/developer_guide.md`
- `docs/deployment/changelog.md`
- `LICENSE`

**验证**: 文档完整，覆盖所有功能

---

## 依赖关系图

```
Step 1 (目录) -> Step 2 (依赖) -> Step 3 (i18n)
                                        |
                                        v
Step 4 (数据管理) -> Step 5 (基础统计) -> Step 6 (高级统计)
                                                |
                                                v
Step 7 (绘图) --------> Step 8 (Bridge) --------> Step 9 (GUI骨架)
                                                |
                                                v
Step 10 (菜单) -> Step 11 (标签页) -> Step 12 (表格) -> Step 13 (导航)
                                                        |
                                                        v
Step 14 (对话框) -> Step 15 (输出) -> Step 16 (设置) -> Step 17 (集成测试)
                                                            |
                                                            v
Step 18 (样式) -> Step 19 (打包) -> Step 20 (文档)
```

---

## 每步 AI 提示词模板

对 AI 编程助手，每步使用如下提示词格式：

```
你正在开发 AxaltyX 统计软件。

【第一步：阅读参考文档】
请先阅读以下文档（按顺序）：
1. {参考文档路径}
2. {参考文档路径}

【第二步：实施】
按照参考文档中定义的接口和规范，实现 Step {N}: {步骤描述}。

要求：
1. 仅实现该步骤描述的功能，不添加额外功能
2. 所有 UI 文字从 i18n JSON 加载，禁止 Python 内硬编码任何文字
3. 函数签名、参数、返回值严格遵循参考文档中的 API 定义
4. 代码放在正确的文件路径下
5. 完成后提供验证命令
```
