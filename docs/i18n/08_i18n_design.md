# AxaltyX 国际化 (i18n) 设计文档

> 版本: 1.0.0 | 版权: TBJ114 | 模块: axaltyx_i18n

---

## 设计原则

- **禁止 Python 内硬编码任何文字**，所有 UI 文字必须从 JSON 文件加载
- 采用嵌套 JSON 结构，按模块/页面/组件分层组织
- 支持语言: 中文(zh_CN)、英文(en_US)、日文(ja_JP)
- 翻译键命名规范: `模块.页面.元素` (如 `menu.file.open`)
- 占位符格式: `{variable_name}`

---

## 1. JSON 文件结构

文件路径: `src/axaltyx_i18n/locales/`

```
locales/
  zh_CN.json    # 简体中文
  en_US.json    # 英文
  ja_JP.json    # 日文
```

---

## 2. 完整 JSON 结构定义

### 2.1 顶层结构

```json
{
  "meta": {
    "language": "zh_CN",
    "language_name": "简体中文",
    "version": "1.0.0",
    "author": "TBJ114",
    "date": "2026-04-20"
  },
  "app": { },
  "menu": { },
  "toolbar": { },
  "navigation": { },
  "table": { },
  "dialog": { },
  "analysis": { },
  "chart": { },
  "output": { },
  "settings": { },
  "notification": { },
  "status": { },
  "error": { },
  "common": { }
}
```

### 2.2 app -- 应用全局

```json
{
  "app": {
    "name": "AxaltyX",
    "version": "v1.0.0",
    "copyright": "Copyright (c) TBJ114",
    "loading": "正在加载核心模块...",
    "loading_data_engine": "正在初始化数据引擎...",
    "loading_analysis_engine": "正在初始化分析引擎...",
    "loading_plot_engine": "正在初始化图表引擎...",
    "loading_ui": "正在构建界面...",
    "ready": "就绪"
  }
}
```

### 2.3 menu -- 菜单栏

```json
{
  "menu": {
    "file": {
      "label": "文件",
      "new": "新建",
      "open": "打开",
      "save": "保存",
      "save_as": "另存为",
      "close": "关闭",
      "export": "导出",
      "recent_files": "最近文件",
      "exit": "退出"
    },
    "edit": {
      "label": "编辑",
      "undo": "撤销",
      "redo": "重做",
      "cut": "剪切",
      "copy": "复制",
      "paste": "粘贴",
      "delete": "删除",
      "find": "查找与替换",
      "select_all": "全选",
      "insert_variable": "插入变量",
      "insert_case": "插入个案",
      "goto": "转到"
    },
    "view": {
      "label": "视图",
      "data_view": "数据视图",
      "variable_view": "变量视图",
      "output_view": "输出视图",
      "syntax_view": "语法视图",
      "toolbar": "工具栏",
      "status_bar": "状态栏",
      "navigation_panel": "导航面板",
      "property_panel": "属性面板",
      "theme": "主题",
      "light_theme": "亮色主题",
      "dark_theme": "暗色主题",
      "zoom_in": "放大",
      "zoom_out": "缩小",
      "reset_zoom": "重置缩放"
    },
    "data": {
      "label": "数据",
      "define_variables": "定义变量",
      "sort_cases": "排序个案",
      "transpose": "转置",
      "merge_files": "合并文件",
      "restructure": "重构数据",
      "aggregate": "分类汇总",
      "weight_cases": "加权个案",
      "select_cases": "选择个案",
      "split_file": "拆分文件",
      "identify_duplicates": "标识重复个案",
      "missing_value_analysis": "缺失值分析"
    },
    "analysis": {
      "label": "分析",
      "descriptive": "描述统计",
      "frequency": "频数分析",
      "crosstabs": "交叉表",
      "means": "均值比较",
      "t_test": "t 检验",
      "anova": "方差分析",
      "nonparametric": "非参数检验",
      "correlation": "相关分析",
      "regression": "回归分析",
      "classification": "分类",
      "dimension_reduction": "降维",
      "scale": "尺度分析",
      "survival": "生存分析",
      "multiple_response": "多重响应",
      "time_series": "时间序列",
      "missing_value": "缺失值处理",
      "advanced": "高级分析",
      "machine_learning": "机器学习",
      "causal_inference": "因果推断",
      "bayesian": "贝叶斯统计",
      "network": "网络分析",
      "spatial": "空间分析",
      "text_mining": "文本挖掘"
    },
    "graph": {
      "label": "图形",
      "chart_builder": "图表构建器",
      "bar": "条形图",
      "histogram": "直方图",
      "scatter": "散点图",
      "line": "折线图",
      "pie": "饼图",
      "boxplot": "箱线图",
      "heatmap": "热图",
      "qq_plot": "P-P/Q-Q 图",
      "roc_curve": "ROC 曲线",
      "custom": "自定义图表"
    },
    "tools": {
      "label": "工具",
      "options": "选项",
      "syntax_editor": "语法编辑器",
      "custom_dialogs": "自定义对话框",
      "package_manager": "扩展包管理"
    },
    "help": {
      "label": "帮助",
      "contents": "帮助目录",
      "tutorial": "教程",
      "about": "关于 AxaltyX",
      "check_update": "检查更新",
      "license": "许可证"
    }
  }
}
```

### 2.4 navigation -- 左侧导航

```json
{
  "navigation": {
    "data": "数据",
    "variables": "变量",
    "analysis": "分析",
    "charts": "图形",
    "output": "输出",
    "syntax": "语法",
    "categories": {
      "descriptive": "描述统计",
      "frequency": "频数分析",
      "crosstabs": "交叉表与卡方检验",
      "means": "均值比较",
      "t_test": "t 检验",
      "anova": "方差分析",
      "nonparametric": "非参数检验",
      "correlation": "相关分析",
      "regression": "回归分析",
      "classification": "分类分析",
      "dimension_reduction": "降维分析",
      "scale": "尺度分析",
      "survival": "生存分析",
      "time_series": "时间序列",
      "missing_value": "缺失值处理",
      "multiple_response": "多重响应分析",
      "log_linear": "对数线性模型",
      "meta_analysis": "Meta 分析",
      "sem": "结构方程模型",
      "bayesian": "贝叶斯统计",
      "machine_learning": "机器学习",
      "causal_inference": "因果推断",
      "network": "网络分析",
      "spatial": "空间分析",
      "text_mining": "文本挖掘"
    },
    "items": {
      "descriptive_stats": "描述性统计",
      "frequencies": "频数分析",
      "crosstabs": "交叉表",
      "one_sample_t": "单样本 t 检验",
      "independent_t": "独立样本 t 检验",
      "paired_t": "配对样本 t 检验",
      "one_way_anova": "单因素方差分析",
      "two_way_anova": "多因素方差分析",
      "ancova": "协方差分析",
      "rm_anova": "重复测量方差分析",
      "mann_whitney": "Mann-Whitney U 检验",
      "wilcoxon": "Wilcoxon 符号秩检验",
      "kruskal_wallis": "Kruskal-Wallis 检验",
      "friedman": "Friedman 检验",
      "pearson": "Pearson 相关",
      "partial_corr": "偏相关",
      "spearman": "Spearman 秩相关",
      "linear_reg": "线性回归",
      "logistic_reg": "Logistic 回归",
      "ordinal_reg": "有序回归",
      "nonlinear_reg": "非线性回归",
      "curve_est": "曲线估计",
      "efa": "探索性因子分析",
      "cfa": "验证性因子分析",
      "pca": "主成分分析",
      "hierarchical_cluster": "层次聚类",
      "kmeans": "K-Means 聚类",
      "discriminant": "判别分析",
      "correspondence": "对应分析",
      "cronbach_alpha": "Cronbach Alpha",
      "split_half": "分半信度",
      "validity": "效度分析",
      "kaplan_meier": "Kaplan-Meier 生存分析",
      "cox_reg": "Cox 回归",
      "acf_pacf": "自相关/偏自相关",
      "arima": "ARIMA 模型",
      "exp_smoothing": "指数平滑",
      "decompose": "时间序列分解",
      "em_imputation": "EM 插补",
      "multiple_imputation": "多重插补",
      "log_linear_model": "对数线性模型",
      "probit": "Probit 分析",
      "meta_analysis": "Meta 分析",
      "sem_analysis": "结构方程模型",
      "bayesian_t": "贝叶斯 t 检验",
      "bayesian_reg": "贝叶斯回归",
      "random_forest": "随机森林",
      "svm": "支持向量机",
      "gradient_boosting": "梯度提升树",
      "neural_network": "神经网络",
      "lasso": "Lasso 回归",
      "ridge": "岭回归",
      "elastic_net": "弹性网",
      "psm": "倾向得分匹配",
      "did": "双重差分",
      "iv": "工具变量法",
      "rdd": "断点回归",
      "quantile_reg": "分位数回归",
      "hlm": "多层线性模型",
      "network_analysis": "网络分析",
      "moran_i": "Moran's I",
      "sentiment": "情感分析",
      "word_cloud": "词云"
    }
  }
}
```

### 2.5 table -- 表格

```json
{
  "table": {
    "default_var_name": "VAR{index}",
    "row_header": "行号",
    "column_header": "变量",
    "right_click": {
      "copy": "复制",
      "paste": "粘贴",
      "insert_variable": "插入变量",
      "insert_case": "插入个案",
      "delete": "删除",
      "clear": "清除内容",
      "sort_ascending": "升序排列",
      "sort_descending": "降序排列",
      "find": "查找..."
    },
    "column_edit": {
      "title": "编辑变量名",
      "current_name": "当前名称",
      "new_name": "新名称",
      "confirm": "确定",
      "cancel": "取消"
    }
  }
}
```

### 2.6 dialog -- 对话框通用

```json
{
  "dialog": {
    "ok": "确定",
    "cancel": "取消",
    "apply": "应用",
    "reset": "重置",
    "paste_syntax": "粘贴语法",
    "close": "关闭",
    "help": "帮助",
    "variable_selector": {
      "available": "可用变量",
      "selected": "分析变量",
      "move_right": "移动到右侧",
      "move_left": "移动到左侧",
      "move_all_right": "全部移动到右侧",
      "move_all_left": "全部移动到左侧"
    },
    "file_dialog": {
      "open_title": "打开数据文件",
      "save_title": "保存数据文件",
      "file_type": "文件类型",
      "encoding": "编码",
      "all_files": "所有文件",
      "csv_files": "CSV 文件 (*.csv)",
      "excel_files": "Excel 文件 (*.xlsx)",
      "spss_files": "SPSS 文件 (*.sav)",
      "stata_files": "Stata 文件 (*.dta)",
      "json_files": "JSON 文件 (*.json)"
    },
    "export_dialog": {
      "title": "导出图表",
      "format": "格式",
      "dpi": "分辨率 (DPI)",
      "width": "宽度",
      "height": "高度",
      "transparent": "透明背景"
    }
  }
}
```

### 2.7 analysis -- 分析对话框专用

```json
{
  "analysis": {
    "descriptive_stats": {
      "title": "描述性统计",
      "variables": "变量",
      "statistics": "统计量",
      "mean": "均值",
      "median": "中位数",
      "mode": "众数",
      "std": "标准差",
      "variance": "方差",
      "min": "最小值",
      "max": "最大值",
      "range": "全距",
      "skewness": "偏度",
      "kurtosis": "峰度",
      "sum": "求和",
      "count": "计数",
      "sem": "标准误",
      "cv": "变异系数",
      "percentiles": "百分位数"
    },
    "t_test": {
      "title": "t 检验",
      "test_variable": "检验变量",
      "group_variable": "分组变量",
      "test_value": "检验值",
      "confidence_interval": "置信区间",
      "equal_variance": "假设方差齐性",
      "define_groups": "定义组"
    },
    "anova": {
      "title": "方差分析",
      "dependent_variable": "因变量",
      "factor": "因子",
      "post_hoc": "事后比较",
      "effect_size": "效应量",
      "homogeneity": "方差齐性检验"
    },
    "regression": {
      "title": "回归分析",
      "dependent": "因变量",
      "independent": "自变量",
      "method": "方法",
      "enter": "进入法",
      "stepwise": "逐步法",
      "forward": "向前法",
      "backward": "向后法",
      "confidence_level": "置信水平",
      "collinearity": "共线性诊断"
    },
    "factor_analysis": {
      "title": "因子分析",
      "variables": "变量",
      "extraction": "提取方法",
      "rotation": "旋转方法",
      "n_factors": "因子数",
      "kaiser": "Kaiser 准则",
      "parallel": "平行分析",
      "scree": "碎石图",
      "varimax": "最大方差法",
      "promax": "Promax 斜交旋转"
    },
    "clustering": {
      "title": "聚类分析",
      "variables": "变量",
      "n_clusters": "聚类数",
      "method": "方法",
      "standardize": "标准化"
    },
    "survival": {
      "title": "生存分析",
      "time_variable": "时间变量",
      "event_variable": "事件变量",
      "group_variable": "分组变量",
      "covariates": "协变量"
    }
  }
}
```

### 2.8 settings -- 设置

```json
{
  "settings": {
    "title": "设置",
    "general": {
      "label": "常规",
      "language": "语言",
      "theme": "主题",
      "startup_action": "启动时",
      "auto_save": "自动保存",
      "auto_save_interval": "自动保存间隔(分钟)",
      "recent_files_count": "最近文件数量",
      "decimal_places": "小数位数"
    },
    "appearance": {
      "label": "外观",
      "font_size": "字体大小",
      "table_font": "表格字体",
      "zoom_level": "缩放级别"
    },
    "data": {
      "label": "数据",
      "default_rows": "默认行数",
      "default_cols": "默认列数",
      "decimal_separator": "小数分隔符",
      "thousand_separator": "千位分隔符"
    },
    "output": {
      "label": "输出",
      "chart_format": "默认图表格式",
      "chart_dpi": "默认图表分辨率",
      "table_format": "表格输出格式"
    },
    "performance": {
      "label": "性能",
      "max_threads": "最大线程数",
      "virtual_scroll": "虚拟滚动",
      "cache_size": "缓存大小(MB)"
    }
  }
}
```

### 2.9 notification -- 通知

```json
{
  "notification": {
    "success": {
      "title": "操作成功",
      "data_loaded": "数据已加载，共 {n} 条记录",
      "data_saved": "数据已保存至 {path}",
      "analysis_completed": "分析完成: {name}",
      "chart_exported": "图表已导出至 {path}"
    },
    "warning": {
      "title": "警告",
      "unsaved_changes": "存在未保存的更改",
      "missing_data": "检测到缺失值，共 {n} 个",
      "small_sample": "样本量较小，结果可能不可靠",
      "perfect_collinearity": "检测到完全共线性"
    },
    "error": {
      "title": "错误",
      "file_not_found": "文件不存在: {path}",
      "invalid_format": "不支持的文件格式: {format}",
      "analysis_failed": "分析失败: {message}",
      "insufficient_data": "数据不足，无法执行分析"
    },
    "info": {
      "title": "提示",
      "update_available": "发现新版本 {version}",
      "memory_usage": "内存使用: {percent}%",
      "processing": "正在处理..."
    }
  }
}
```

### 2.10 status -- 状态栏

```json
{
  "status": {
    "ready": "就绪",
    "processing": "处理中...",
    "rows_cols": "行: {rows}, 列: {cols}",
    "selected": "已选择 {n} 项",
    "cpu": "处理器: {percent}%",
    "memory": "内存: {value}MB"
  }
}
```

### 2.11 error -- 错误信息

```json
{
  "error": {
    "no_data": "当前没有打开的数据文件",
    "no_variables_selected": "请选择至少一个变量",
    "invalid_variable_type": "变量类型不适用于此分析",
    "file_read_error": "文件读取失败: {message}",
    "file_write_error": "文件写入失败: {message}",
    "analysis_error": "分析执行错误: {message}",
    "missing_required_param": "缺少必要参数: {param}",
    "invalid_param_value": "参数值无效: {param} = {value}",
    "out_of_memory": "内存不足",
    "network_error": "网络连接失败"
  }
}
```

### 2.12 common -- 通用文字

```json
{
  "common": {
    "yes": "是",
    "no": "否",
    "confirm": "确认",
    "delete": "删除",
    "rename": "重命名",
    "add": "添加",
    "remove": "移除",
    "edit": "编辑",
    "save": "保存",
    "cancel": "取消",
    "close": "关闭",
    "search": "搜索",
    "filter": "筛选",
    "reset": "重置",
    "default": "默认",
    "custom": "自定义",
    "none": "无",
    "all": "全部",
    "apply": "应用",
    "ok": "确定",
    "back": "返回",
    "next": "下一步",
    "previous": "上一步",
    "finish": "完成",
    "loading": "加载中...",
    "no_data": "暂无数据",
    "select_all": "全选",
    "deselect_all": "取消全选",
    "copy": "复制",
    "cut": "剪切",
    "paste": "粘贴",
    "undo": "撤销",
    "redo": "重做",
    "name": "名称",
    "type": "类型",
    "value": "值",
    "label": "标签",
    "description": "描述",
    "options": "选项",
    "parameters": "参数",
    "results": "结果",
    "details": "详情",
    "summary": "摘要",
    "export": "导出",
    "import": "导入",
    "print": "打印",
    "refresh": "刷新"
  }
}
```

---

## 3. I18nManager API

文件路径: `src/axaltyx_i18n/`

### 3.1 I18nManager

```python
class I18nManager:
    """国际化管理器"""

    def __init__(self, locales_dir: str = None): ...
    def load_language(self, lang_code: str) -> None: ...
    def get_text(self, key: str, **kwargs) -> str: ...
    def get_current_language(self) -> str: ...
    def get_available_languages(self) -> list[dict]: ...
    def set_language(self, lang_code: str) -> None: ...
    def register_fallback(self, lang_code: str) -> None: ...
```

**使用示例**:

```python
i18n = I18nManager("src/axaltyx_i18n/locales")
i18n.set_language("zh_CN")

# 获取文字
title = i18n.get_text("menu.file.open")           # "打开"
msg = i18n.get_text("notification.success.data_loaded", n=1000)  # "数据已加载，共 1000 条记录"
```
