# AxaltyX 产品定位与总体架构

> 版本：v1.0.0
> 更新日期：2026-04-20
> 版权所有：TBJ114

---

## 目录

1. [产品定位](#1-产品定位)
2. [技术栈](#2-技术栈)
3. [总体架构](#3-总体架构)
4. [项目文件夹结构](#4-项目文件夹结构)
5. [设计原则](#5-设计原则)

---

## 1. 产品定位

### 1.1 目标用户

AxaltyX 面向以下四类核心用户群体：

| 用户群体 | 典型场景 | 核心诉求 |
|---------|---------|---------|
| 本科生 | 课程作业、毕业论文数据分析 | 易上手、免费、功能覆盖教学大纲 |
| 研究生 | 学位论文、课题研究 | 专业统计方法、高质量输出图表 |
| 科研人员 | 学术论文、课题申报、数据分析 | 方法全面、结果可靠、可重复性 |
| 问卷与数据分析用户 | 市场调研、社会调查、用户研究 | 高效数据清洗、描述统计、交叉分析 |

### 1.2 核心定位

AxaltyX 定位为**专业级桌面统计工具**，具备以下核心特征：

- **功能对标 SPSS 标准版**：覆盖描述统计、推断统计、回归分析、方差分析、非参数检验、因子分析、聚类分析、生存分析、信效度检验等主流统计方法，功能范围不低于 SPSS 标准版。
- **性能超越 SPSS**：核心计算引擎基于 Python 科学计算生态，关键统计任务执行速度不低于 SPSS 的 3 倍。
- **零成本使用**：面向目标用户群体完全免费，降低学术与教育领域的统计工具使用门槛。

### 1.3 运行模式

- **本地离线优先**：所有统计计算与数据处理均在用户本地完成，无需网络连接即可使用全部核心功能，保障数据隐私与处理效率。
- **可选云端同步**：支持通过字节跳动账号登录，实现用户配置、自定义模板、偏好设置等轻量数据的云端同步。云端同步为可选功能，不影响离线使用。

### 1.4 视觉风格

- **设计语言**：遵循字节跳动设计语言体系，采用 Arco Design / ByteDesign 设计规范。
- **界面风格**：现代简洁，信息密度适中，操作路径清晰。
- **色彩体系**：以 Arco Design 色彩体系为基础，主色调为 `#165DFF`（Arco Blue），辅以中性灰色系与功能色。
- **无装饰原则**：界面中不使用任何 emoji 或装饰性图标，保持专业工具的严肃性与一致性。

### 1.5 版权声明

- **版权所有**：TBJ114
- **开源协议**：详见项目根目录 LICENSE 文件

---

## 2. 技术栈

### 2.1 核心技术栈总览

| 层级 | 技术选型 | 版本要求 | 用途说明 |
|------|---------|---------|---------|
| 编程语言 | Python | 3.11+ | 核心统计引擎与业务逻辑 |
| GUI 框架 | PyQt6 (Qt6) | 6.5+ | 桌面图形用户界面 |
| 操作系统 | Windows 11 | 22H2+ | 主力编译与运行环境 |
| 打包工具 | PyInstaller / cx_Freeze | 最新稳定版 | 构建 Windows 安装包 |

### 2.2 统计计算后端

| 库 | 用途 |
|---|------|
| **numpy** | 高性能数值计算、矩阵运算 |
| **scipy** | 科学计算、统计分布、优化算法 |
| **pandas** | 数据结构、数据清洗、数据变换 |
| **scikit-learn** | 机器学习算法、聚类、分类、回归 |
| **statsmodels** | 统计建模、回归分析、假设检验、时间序列 |
| **lifelines** | 生存分析（Kaplan-Meier、Cox 回归等） |
| **torch** (PyTorch) | 深度学习、神经网络（可选模块） |

### 2.3 绘图后端

| 库 | 用途 |
|---|------|
| **matplotlib** | 基础统计图表（柱状图、散点图、箱线图等） |
| **plotly** | 交互式图表（支持缩放、悬停提示等） |
| **pyecharts** | 基于 ECharts 的图表渲染（适用于复杂可视化场景） |

### 2.4 开发工具链

| 工具 | 用途 |
|------|------|
| **PyInstaller / cx_Freeze** | 将 Python 应用打包为 Windows 可执行文件 |
| **pytest** | 单元测试与集成测试 |
| **ruff / black** | 代码格式化与静态检查 |
| **mypy** | 类型检查 |
| **pylint** | 代码质量检查 |

---

## 3. 总体架构

### 3.1 架构概览

AxaltyX 采用**三层架构**设计，各层之间通过明确的接口通信，实现高内聚低耦合：

```
+--------------------------------------------------+
|                  axaltyx_gui                      |
|              (Qt6 图形用户界面)                    |
|  - 窗口管理、菜单栏、工具栏、状态栏                |
|  - 数据编辑器、变量视图、输出视图                  |
|  - 对话框、参数面板、结果展示                      |
+--------------------------------------------------+
                        |
                   信号-槽机制
                        |
+--------------------------------------------------+
|                axaltyx_bridge                     |
|              (通信桥接层)                         |
|  - GUI 与核心引擎之间的消息路由                    |
|  - 任务调度与线程池管理                            |
|  - 进度报告与状态反馈                              |
|  - 数据格式转换与校验                              |
+--------------------------------------------------+
                        |
                   信号-槽机制
                        |
+--------------------------------------------------+
|                axaltyx_core                       |
|              (核心统计引擎)                        |
|  - 描述统计、推断统计、回归分析                    |
|  - 方差分析、非参数检验、因子分析                  |
|  - 聚类分析、生存分析、信效度检验                  |
|  - 数据导入/导出、数据清洗                         |
+--------------------------------------------------+
```

### 3.2 辅助模块

除三层核心架构外，系统包含以下辅助模块：

```
+-------------------+    +-------------------+    +-------------------+
|   axaltyx_i18n    |    |   axaltyx_plot    |    |   axaltyx_utils   |
|   (国际化模块)     |    |   (绘图引擎)       |    |   (工具集)         |
|                   |    |                   |    |                   |
| - JSON 驱动       |    | - matplotlib 封装  |    | - 文件路径处理     |
| - 中/英/日 多语言  |    | - plotly 封装      |    | - 数据类型转换     |
| - 语言热切换       |    | - pyecharts 封装   |    | - 异常处理工具     |
| - 禁止硬编码文字   |    | - 图表样式统一     |    | - 日志工具         |
+-------------------+    +-------------------+    +-------------------+
```

### 3.3 通信机制

#### 3.3.1 信号-槽机制

模块间通信采用 Qt 的**信号-槽（Signal-Slot）**机制实现松耦合：

- **GUI -> Bridge**：用户操作（如点击"运行分析"按钮）触发信号，Bridge 接收并解析任务请求。
- **Bridge -> Core**：Bridge 将任务分发至 Core 的对应统计模块，通过独立线程执行。
- **Core -> Bridge -> GUI**：Core 完成计算后，通过信号将结果回传至 Bridge，Bridge 再转发至 GUI 进行展示。
- **进度反馈**：长时间计算任务通过进度信号实时反馈至 GUI 的进度条。

#### 3.3.2 线程池

- 使用 `QThreadPool` 管理计算任务线程，避免阻塞 GUI 主线程。
- 每个统计任务封装为 `QRunnable` 对象，提交至线程池异步执行。
- 线程池大小根据 CPU 核心数动态配置，默认为 `max(2, CPU核心数 - 1)`。

### 3.4 数据流

```
用户操作 (GUI)
    |
    v
参数校验 (Bridge)
    |
    v
数据预处理 (Core)
    |
    v
统计计算 (Core)  -----> [线程池异步执行]
    |
    v
结果格式化 (Core)
    |
    v
结果展示 (GUI)
    |
    v
图表生成 (Plot)  -----> [可选，按需生成]
```

---

## 4. 项目文件夹结构

```
AxaltyX/
|
|-- docs/                              # 项目文档
|   |-- architecture/                  # 架构文档
|   |   |-- 01_product_positioning.md  # 产品定位与总体架构（本文档）
|   |   |-- 02_module_design.md        # 模块详细设计
|   |   |-- 03_ui_specification.md     # UI 界面规范
|   |   |-- 04_statistics_methods.md   # 统计方法清单
|   |   +-- 05_i18n_specification.md   # 国际化规范
|   +-- api/                           # API 文档
|
|-- src/                               # 源代码根目录
|   |
|   |-- axaltyx_core/                  # 核心统计引擎
|   |   |-- __init__.py                # 包初始化
|   |   |-- base/                      # 基础模块
|   |   |   |-- __init__.py
|   |   |   |-- data_loader.py         # 数据加载器（CSV/Excel/SPSS/JSON）
|   |   |   |-- data_cleaner.py        # 数据清洗（缺失值、异常值处理）
|   |   |   |-- data_transformer.py    # 数据变换（标准化、编码、分箱）
|   |   |   |-- variable.py            # 变量定义与类型管理
|   |   |   +-- dataset.py             # 数据集容器
|   |   |
|   |   |-- descriptive/               # 描述统计模块
|   |   |   |-- __init__.py
|   |   |   |-- frequencies.py         # 频率分析
|   |   |   |-- descriptives.py        # 描述统计量
|   |   |   |-- crosstabs.py           # 交叉表
|   |   |   +-- explore.py             # 数据探索
|   |   |
|   |   |-- inferential/               # 推断统计模块
|   |   |   |-- __init__.py
|   |   |   |-- t_test.py              # T 检验（单样本、独立样本、配对样本）
|   |   |   |-- anova.py               # 方差分析（单因素、多因素、重复测量）
|   |   |   |-- nonparametric.py       # 非参数检验（Mann-Whitney、Kruskal-Wallis 等）
|   |   |   |-- chi_square.py          # 卡方检验
|   |   |   |-- correlation.py         # 相关分析（Pearson、Spearman、Kendall）
|   |   |   +-- regression.py          # 回归分析（线性、逻辑、多元）
|   |   |
|   |   |-- advanced/                  # 高级统计模块
|   |   |   |-- __init__.py
|   |   |   |-- factor_analysis.py     # 因子分析（探索性、验证性）
|   |   |   |-- cluster.py             # 聚类分析（K-Means、层次聚类）
|   |   |   |-- survival.py            # 生存分析（Kaplan-Meier、Cox 回归）
|   |   |   |-- reliability.py         # 信度分析（Cronbach's Alpha）
|   |   |   |-- validity.py            # 效度分析（KMO、Bartlett）
|   |   |   |-- time_series.py         # 时间序列分析
|   |   |   +-- pca.py                 # 主成分分析
|   |   |
|   |   |-- ml/                        # 机器学习模块（可选）
|   |   |   |-- __init__.py
|   |   |   |-- classification.py      # 分类算法
|   |   |   |-- neural_network.py      # 神经网络（基于 PyTorch）
|   |   |   +-- model_evaluation.py    # 模型评估
|   |   |
|   |   +-- export/                    # 结果导出模块
|   |       |-- __init__.py
|   |       |-- spss_exporter.py       # SPSS 格式导出
|   |       |-- csv_exporter.py        # CSV 导出
|   |       |-- excel_exporter.py      # Excel 导出
|   |       +-- pdf_exporter.py        # PDF 报告导出
|   |
|   |-- axaltyx_bridge/                # 通信桥接层
|   |   |-- __init__.py
|   |   |-- task_dispatcher.py         # 任务分发器
|   |   |-- task_queue.py              # 任务队列管理
|   |   |-- result_handler.py          # 结果处理器
|   |   |-- progress_manager.py        # 进度管理
|   |   |-- signal_bus.py              # 全局信号总线
|   |   |-- thread_pool.py             # 线程池管理
|   |   +-- validators.py              # 参数校验器
|   |
|   |-- axaltyx_gui/                   # Qt6 图形用户界面
|   |   |-- __init__.py
|   |   |-- app.py                     # 应用入口
|   |   |-- main_window.py             # 主窗口
|   |   |-- menus/                     # 菜单栏
|   |   |   |-- __init__.py
|   |   |   |-- file_menu.py           # 文件菜单
|   |   |   |-- edit_menu.py           # 编辑菜单
|   |   |   |-- view_menu.py           # 视图菜单
|   |   |   |-- data_menu.py           # 数据菜单
|   |   |   |-- analyze_menu.py        # 分析菜单
|   |   |   |-- graphs_menu.py         # 图形菜单
|   |   |   |-- extensions_menu.py     # 扩展菜单
|   |   |   +-- help_menu.py           # 帮助菜单
|   |   |
|   |   |-- toolbars/                  # 工具栏
|   |   |   |-- __init__.py
|   |   |   |-- main_toolbar.py        # 主工具栏
|   |   |   +-- data_toolbar.py        # 数据编辑工具栏
|   |   |
|   |   |-- panels/                    # 面板
|   |   |   |-- __init__.py
|   |   |   |-- data_editor.py         # 数据编辑器（SPSS 式表格）
|   |   |   |-- variable_view.py       # 变量视图
|   |   |   |-- output_viewer.py       # 输出查看器
|   |   |   +-- syntax_editor.py       # 语法编辑器
|   |   |
|   |   |-- dialogs/                   # 对话框
|   |   |   |-- __init__.py
|   |   |   |-- about_dialog.py        # 关于对话框
|   |   |   |-- preferences_dialog.py  # 偏好设置对话框
|   |   |   |-- login_dialog.py        # 登录对话框（字节账号）
|   |   |   |-- import_dialog.py       # 数据导入对话框
|   |   |   |-- export_dialog.py       # 数据导出对话框
|   |   |   +-- analysis_dialogs/      # 统计分析对话框
|   |   |       |-- __init__.py
|   |   |       |-- t_test_dialog.py
|   |   |       |-- anova_dialog.py
|   |   |       |-- regression_dialog.py
|   |   |       |-- correlation_dialog.py
|   |   |       |-- factor_dialog.py
|   |   |       |-- cluster_dialog.py
|   |   |       |-- survival_dialog.py
|   |   |       +-- ...                # 其他统计方法对话框
|   |   |
|   |   |-- widgets/                   # 自定义控件
|   |   |   |-- __init__.py
|   |   |   |-- data_table.py          # 数据表格控件（100x100 默认）
|   |   |   |-- variable_table.py      # 变量表格控件
|   |   |   |-- result_table.py        # 结果表格控件
|   |   |   |-- chart_widget.py        # 图表容器控件
|   |   |   |-- progress_widget.py     # 进度条控件
|   |   |   +-- status_bar.py          # 状态栏控件
|   |   |
|   |   |-- styles/                    # 样式表
|   |   |   |-- theme_arco.py          # Arco Design 主题定义
|   |   |   |-- colors.py              # 颜色常量
|   |   |   +-- fonts.py               # 字体定义
|   |   |
|   |   +-- resources/                 # GUI 资源文件
|   |       |-- icons/                 # 图标资源
|   |       +-- fonts/                 # 字体文件
|   |
|   |-- axaltyx_i18n/                  # 国际化模块
|   |   |-- __init__.py
|   |   |-- i18n_manager.py            # 国际化管理器（语言加载、切换）
|   |   |-- locale/                    # 语言文件目录
|   |   |   |-- zh_CN.json             # 简体中文
|   |   |   |-- en_US.json             # 英文（美国）
|   |   |   +-- ja_JP.json             # 日文
|   |   +-- schema/                    # 语言文件 JSON Schema
|   |       +-- locale_schema.json     # 语言文件结构校验
|   |
|   |-- axaltyx_plot/                  # 绘图引擎
|   |   |-- __init__.py
|   |   |-- plot_manager.py            # 绘图管理器（统一入口）
|   |   |-- base_plotter.py            # 绘图基类
|   |   |-- matplotlib_plotter.py      # matplotlib 封装
|   |   |-- plotly_plotter.py          # plotly 封装
|   |   |-- pyecharts_plotter.py       # pyecharts 封装
|   |   |-- styles/                    # 图表样式
|   |   |   |-- arco_style.py          # Arco Design 图表样式
|   |   |   +-- academic_style.py      # 学术论文图表样式
|   |   +-- templates/                 # 图表模板
|   |       |-- bar_chart.py           # 柱状图模板
|   |       |-- line_chart.py          # 折线图模板
|   |       |-- scatter_chart.py       # 散点图模板
|   |       |-- box_chart.py           # 箱线图模板
|   |       |-- histogram_chart.py     # 直方图模板
|   |       |-- pie_chart.py           # 饼图模板
|   |       |-- heatmap_chart.py       # 热力图模板
|   |       +-- survival_chart.py      # 生存曲线模板
|   |
|   +-- axaltyx_utils/                 # 通用工具集
|       |-- __init__.py
|       |-- logger.py                  # 日志工具
|       |-- config.py                  # 配置管理
|       |-- exceptions.py              # 自定义异常
|       |-- file_utils.py              # 文件路径工具
|       |-- type_utils.py              # 数据类型工具
|       +-- math_utils.py              # 数学辅助工具
|
|-- tests/                             # 测试代码
|   |-- test_core/                     # 核心引擎测试
|   |   |-- test_descriptive/
|   |   |-- test_inferential/
|   |   +-- test_advanced/
|   |-- test_bridge/                   # 桥接层测试
|   |-- test_gui/                      # GUI 测试
|   |-- test_i18n/                     # 国际化测试
|   |-- test_plot/                     # 绘图测试
|   +-- conftest.py                    # 测试配置
|
|-- resources/                         # 全局资源文件
|   |-- icons/                         # 应用图标
|   |-- splash/                        # 启动画面
|   +-- samples/                       # 示例数据集
|
|-- build/                             # 构建输出目录
|   |-- windows/                       # Windows 安装包输出
|   +-- scripts/                       # 构建脚本
|       |-- build_pyinstaller.py       # PyInstaller 构建脚本
|       +-- build_cxfreeze.py          # cx_Freeze 构建脚本
|
|-- config/                            # 配置文件
|   |-- app_config.json                # 应用默认配置
|   +-- build_config.json              # 构建配置
|
|-- pyproject.toml                     # 项目元数据与依赖管理
|-- setup.py                           # 安装脚本（兼容）
|-- requirements.txt                   # 依赖清单
|-- .gitignore                         # Git 忽略规则
+-- LICENSE                            # 开源协议
```

### 4.1 文件夹用途说明

| 文件夹 | 用途 |
|--------|------|
| `docs/` | 项目所有文档，包括架构设计、API 文档、用户手册等 |
| `src/axaltyx_core/` | 核心统计引擎，包含所有统计方法的实现 |
| `src/axaltyx_core/base/` | 数据加载、清洗、变换等基础数据处理功能 |
| `src/axaltyx_core/descriptive/` | 描述统计方法（频率分析、描述统计量、交叉表等） |
| `src/axaltyx_core/inferential/` | 推断统计方法（T 检验、方差分析、回归分析等） |
| `src/axaltyx_core/advanced/` | 高级统计方法（因子分析、聚类、生存分析等） |
| `src/axaltyx_core/ml/` | 机器学习方法（分类、神经网络等） |
| `src/axaltyx_core/export/` | 结果导出功能（SPSS、CSV、Excel、PDF） |
| `src/axaltyx_bridge/` | 通信桥接层，负责 GUI 与 Core 之间的消息路由与任务调度 |
| `src/axaltyx_gui/` | Qt6 图形用户界面，包含主窗口、菜单、面板、对话框等 |
| `src/axaltyx_gui/menus/` | 菜单栏各菜单项的实现 |
| `src/axaltyx_gui/panels/` | 主窗口中的各个面板（数据编辑器、输出查看器等） |
| `src/axaltyx_gui/dialogs/` | 各类对话框（导入、导出、分析参数设置等） |
| `src/axaltyx_gui/widgets/` | 自定义 UI 控件 |
| `src/axaltyx_gui/styles/` | 界面样式定义（Arco Design 主题） |
| `src/axaltyx_gui/resources/` | GUI 所需的图标、字体等静态资源 |
| `src/axaltyx_i18n/` | 国际化模块，管理多语言支持 |
| `src/axaltyx_i18n/locale/` | 各语言的 JSON 翻译文件 |
| `src/axaltyx_plot/` | 绘图引擎，封装多种绘图后端 |
| `src/axaltyx_utils/` | 通用工具集（日志、配置、异常处理等） |
| `tests/` | 全部测试代码 |
| `resources/` | 全局资源（应用图标、启动画面、示例数据集） |
| `build/` | 构建脚本与输出目录 |
| `config/` | 应用配置文件 |

---

## 5. 设计原则

### 5.1 模块化设计

- **独立模块**：每个统计方法封装为独立模块，拥有清晰的输入输出接口。
- **可插拔架构**：新增统计方法只需在对应目录下添加模块文件，无需修改现有代码。
- **单一职责**：每个模块只负责一项统计功能，避免功能交叉。
- **依赖注入**：模块之间通过接口通信，不直接依赖具体实现。

### 5.2 JSON 驱动

- **UI 文字外部化**：界面中显示的所有文字（包括菜单项、按钮文字、提示信息、错误信息、列标题等）必须从 JSON 语言文件加载，**严禁在 Python 代码中硬编码任何界面文字**。
- **语言文件结构**：JSON 文件按功能模块组织键值结构，支持嵌套命名空间。
- **热切换**：用户可在运行时切换界面语言，无需重启应用。
- **缺失值处理**：当某语言文件中缺少某个键时，自动回退至英文默认值。

### 5.3 字节设计风格（Arco Design）

#### 5.3.1 色彩体系

| 用途 | 色值 | 说明 |
|------|------|------|
| 主色（Primary） | `#165DFF` | Arco Blue，用于主要按钮、选中状态、链接 |
| 主色悬停 | `#4080FF` | 主色鼠标悬停态 |
| 主色点击 | `#0E42D2` | 主色按下态 |
| 成功色（Success） | `#00B42A` | 操作成功、正向指标 |
| 警告色（Warning） | `#FF7D00` | 警告提示、需注意的信息 |
| 错误色（Error） | `#F53F3F` | 错误提示、异常状态 |
| 信息色（Info） | `#165DFF` | 信息提示 |
| 背景色（Bg） | `#F7F8FA` | 页面背景 |
| 卡片背景 | `#FFFFFF` | 卡片与面板背景 |
| 边框色（Border） | `#E5E6EB` | 默认边框 |
| 文字主色 | `#1D2129` | 主要文字 |
| 文字次色 | `#4E5969` | 次要文字 |
| 文字辅助色 | `#86909C` | 辅助说明文字 |
| 文字禁用色 | `#C9CDD4` | 禁用状态文字 |

#### 5.3.2 字体规范

| 类型 | 字体 | 字号 | 字重 |
|------|------|------|------|
| 标题 | Inter / 思源黑体 | 16px / 20px | 600 (Semi-Bold) |
| 正文 | Inter / 思源黑体 | 14px | 400 (Regular) |
| 辅助文字 | Inter / 思源黑体 | 12px | 400 (Regular) |
| 代码/数据 | JetBrains Mono / Consolas | 13px | 400 (Regular) |

#### 5.3.3 间距规范

| 类型 | 间距 |
|------|------|
| 页面内边距 | 24px |
| 卡片内边距 | 16px / 20px |
| 组件间距 | 8px / 12px / 16px |
| 紧凑间距 | 4px |

### 5.4 SPSS 式表格

- **默认空表格**：数据编辑器启动时展示 100 行 x 100 列的空表格，用户可直接输入数据。
- **可编辑表头**：表格列标题（变量名）可直接双击编辑，支持重命名。
- **变量视图**：提供独立的变量视图面板，用于设置变量类型、标签、值标签、缺失值、度量类型等属性。
- **单元格编辑**：支持单击选中、双击编辑、Tab 键切换单元格、方向键导航。
- **数据类型**：自动识别数值型、字符串型、日期型数据，支持手动设置。

### 5.5 多语言支持

- **支持语言**：简体中文（zh_CN）、英文（en_US）、日文（ja_JP）。
- **扩展机制**：语言文件基于 JSON 格式，新增语言只需添加对应 JSON 文件并注册即可。
- **翻译覆盖**：所有面向用户的文字均需提供翻译，包括但不限于：
  - 菜单项与子菜单
  - 按钮文字
  - 对话框标题与内容
  - 表头与列名
  - 提示信息与错误信息
  - 工具提示（Tooltip）
  - 状态栏文字

### 5.6 无 Emoji 原则

- **界面文字**：所有界面文字中不使用任何 emoji 字符。
- **日志与代码**：代码注释、日志输出、提交信息中不使用 emoji。
- **文档**：项目文档中不使用 emoji。
- **图标替代**：如需视觉标识，使用 SVG 矢量图标替代 emoji。

### 5.7 性能要求

- **启动时间**：冷启动时间不超过 3 秒（SSD 环境）。
- **计算响应**：单次统计计算（数据量 <= 10000 行）响应时间不超过 1 秒。
- **大数据支持**：支持处理百万级数据行，内存占用不超过可用内存的 80%。
- **界面流畅**：GUI 操作（滚动、切换、输入）帧率不低于 60 FPS。

### 5.8 安全与隐私

- **数据本地化**：用户数据默认存储在本地，不上传至任何服务器。
- **配置同步可选**：云端同步功能需用户主动开启并授权，仅同步配置信息，不同步用户数据。
- **无遥测**：默认不收集任何使用数据，用户可选择性地开启匿名使用统计。

---

> 本文档为 AxaltyX 项目的顶层架构设计文档，后续详细设计请参阅 `docs/architecture/` 目录下的其他文档。
