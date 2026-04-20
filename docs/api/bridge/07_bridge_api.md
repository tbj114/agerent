# AxaltyX 模块间通信桥接 API 文档

> 版本: 1.0.0 | 版权: TBJ114 | 模块: axaltyx_bridge

---

## 设计约定

- axaltyx_bridge 是 GUI 层与统计核心层之间的通信桥梁
- 采用信号-槽（Signal-Slot）模式实现松耦合
- 所有通信通过 BridgeController 单例调度
- 耗时计算通过 QThread 线程池异步执行
- 通信数据格式统一为 JSON 兼容的 dict

---

## 1. signals -- 信号定义

文件路径: `src/axaltyx_bridge/signals/`

### 1.1 BridgeSignals

```python
class BridgeSignals(QObject):
    """全局信号集合"""

    # ---- 数据操作信号 ----
    sig_data_load_requested = pyqtSignal(str, str)        # (path, file_type)
    sig_data_load_completed = pyqtSignal(dict)            # {success, data, columns, shape, ...}
    sig_data_save_requested = pyqtSignal(str, str, str)   # (path, file_type, encoding)
    sig_data_save_completed = pyqtSignal(dict)            # {success, path, ...}
    sig_data_new_requested = pyqtSignal(int, int)         # (rows, cols)
    sig_data_new_completed = pyqtSignal(dict)             # {success, data, shape}
    sig_data_changed = pyqtSignal(dict)                   # {action, row, col, value}
    sig_variable_changed = pyqtSignal(str, dict)          # (var_name, metadata)

    # ---- 分析操作信号 ----
    sig_analysis_requested = pyqtSignal(str, dict)        # (analysis_name, params)
    sig_analysis_started = pyqtSignal(str)                # analysis_name
    sig_analysis_progress = pyqtSignal(str, int, int)     # (analysis_name, current, total)
    sig_analysis_completed = pyqtSignal(str, dict)        # (analysis_name, results)
    sig_analysis_failed = pyqtSignal(str, str)            # (analysis_name, error_msg)

    # ---- 图表操作信号 ----
    sig_chart_requested = pyqtSignal(str, dict)           # (chart_type, params)
    sig_chart_created = pyqtSignal(str, object)           # (chart_id, figure)
    sig_chart_export_requested = pyqtSignal(str, str, str) # (chart_id, path, format)
    sig_chart_export_completed = pyqtSignal(dict)

    # ---- UI 操作信号 ----
    sig_language_changed = pyqtSignal(str)                # lang_code
    sig_theme_changed = pyqtSignal(str)                   # theme_name
    sig_settings_changed = pyqtSignal(dict)               # settings_dict
    sig_status_message = pyqtSignal(str, int)             # (message, timeout)
    sig_notification = pyqtSignal(str, str, str)          # (type, title, message)
    sig_dialog_open = pyqtSignal(str, dict)               # (dialog_name, params)
    sig_dialog_close = pyqtSignal(str)                    # dialog_name

    # ---- 语法操作信号 ----
    sig_syntax_execute = pyqtSignal(str)                  # syntax_string
    sig_syntax_generated = pyqtSignal(str, str)           # (analysis_name, syntax)
```

---

## 2. slots -- 槽函数

文件路径: `src/axaltyx_bridge/slots/`

### 2.1 DataSlots

```python
class DataSlots(QObject):
    """数据操作槽函数"""

    def __init__(self, core_engine, signals: BridgeSignals): ...

    @pyqtSlot(str, str)
    def on_load_requested(self, path: str, file_type: str) -> None:
        """处理数据加载请求，调用 core 引擎，完成后发射信号"""

    @pyqtSlot(str, str, str)
    def on_save_requested(self, path: str, file_type: str, encoding: str) -> None:
        """处理数据保存请求"""

    @pyqtSlot(int, int)
    def on_new_requested(self, rows: int, cols: int) -> None:
        """处理新建数据集请求"""

    @pyqtSlot(dict)
    def on_data_changed(self, change_info: dict) -> None:
        """处理数据变更通知"""

    @pyqtSlot(str, dict)
    def on_variable_changed(self, var_name: str, metadata: dict) -> None:
        """处理变量属性变更"""
```

### 2.2 AnalysisSlots

```python
class AnalysisSlots(QObject):
    """分析操作槽函数"""

    def __init__(self, core_engine, signals: BridgeSignals): ...

    @pyqtSlot(str, dict)
    def on_analysis_requested(self, analysis_name: str, params: dict) -> None:
        """
        处理分析请求
        1. 验证参数
        2. 发射 analysis_started 信号
        3. 在工作线程中执行分析
        4. 发射 progress 信号
        5. 完成后发射 completed 或 failed 信号
        """

    def _execute_analysis(self, analysis_name: str, params: dict) -> dict:
        """分发到对应的核心模块函数"""

    def _get_analysis_function(self, analysis_name: str) -> callable:
        """根据分析名称获取核心函数引用"""
```

### 2.3 ChartSlots

```python
class ChartSlots(QObject):
    """图表操作槽函数"""

    def __init__(self, plot_engine, signals: BridgeSignals): ...

    @pyqtSlot(str, dict)
    def on_chart_requested(self, chart_type: str, params: dict) -> None:
        """处理图表创建请求"""

    @pyqtSlot(str, str, str)
    def on_export_requested(self, chart_id: str, path: str, format: str) -> None:
        """处理图表导出请求"""
```

### 2.4 UISlots

```python
class UISlots(QObject):
    """UI 操作槽函数"""

    def __init__(self, i18n_manager, theme_manager, signals: BridgeSignals): ...

    @pyqtSlot(str)
    def on_language_changed(self, lang_code: str) -> None:
        """处理语言切换"""

    @pyqtSlot(str)
    def on_theme_changed(self, theme_name: str) -> None:
        """处理主题切换"""

    @pyqtSlot(dict)
    def on_settings_changed(self, settings: dict) -> None:
        """处理设置变更"""

    @pyqtSlot(str)
    def on_syntax_execute(self, syntax_string: str) -> None:
        """处理语法执行"""
```

---

## 3. commands -- 命令系统

文件路径: `src/axaltyx_bridge/commands/`

### 3.1 CommandBase

```python
class CommandBase:
    """命令基类（支持撤销/重做）"""

    def __init__(self): ...
    def execute(self) -> dict: ...
    def undo(self) -> dict: ...
    def redo(self) -> dict: ...
    def get_description(self) -> str: ...
```

### 3.2 LoadDataCommand

```python
class LoadDataCommand(CommandBase):
    def __init__(self, path: str, file_type: str): ...
    def execute(self) -> dict: ...  # 返回 {success, data, ...}
    def undo(self) -> dict: ...    # 恢复之前的数据状态
```

### 3.3 EditCellCommand

```python
class EditCellCommand(CommandBase):
    def __init__(self, row: int, col: int, old_value, new_value): ...
    def execute(self) -> dict: ...
    def undo(self) -> dict: ...    # 恢复 old_value
    def redo(self) -> dict: ...    # 重新设置 new_value
```

### 3.4 InsertColumnCommand

```python
class InsertColumnCommand(CommandBase):
    def __init__(self, position: int, name: str): ...
    def execute(self) -> dict: ...
    def undo(self) -> dict: ...    # 删除插入的列
```

### 3.5 InsertRowCommand

```python
class InsertRowCommand(CommandBase):
    def __init__(self, position: int): ...
    def execute(self) -> dict: ...
    def undo(self) -> dict: ...    # 删除插入的行
```

### 3.6 DeleteColumnsCommand

```python
class DeleteColumnsCommand(CommandBase):
    def __init__(self, columns: list[int], data_backup: pd.DataFrame): ...
    def execute(self) -> dict: ...
    def undo(self) -> dict: ...    # 从备份恢复
```

### 3.7 DeleteRowsCommand

```python
class DeleteRowsCommand(CommandBase):
    def __init__(self, rows: list[int], data_backup: pd.DataFrame): ...
    def execute(self) -> dict: ...
    def undo(self) -> dict: ...
```

### 3.8 CommandHistory

```python
class CommandHistory:
    """命令历史管理（撤销/重做栈）"""

    def __init__(self, max_size: int = 100): ...
    def push(self, command: CommandBase) -> None: ...
    def undo(self) -> dict: ...
    def redo(self) -> dict: ...
    def can_undo(self) -> bool: ...
    def can_redo(self) -> bool: ...
    def clear(self) -> None: ...
    def get_history(self) -> list[str]: ...
```

---

## 4. events -- 事件系统

文件路径: `src/axaltyx_bridge/events/`

### 4.1 EventBus

```python
class EventBus(QObject):
    """事件总线，支持发布-订阅模式"""

    def __init__(self): ...
    def subscribe(self, event_name: str, handler: callable) -> str: ...
    def unsubscribe(self, subscription_id: str) -> None: ...
    def publish(self, event_name: str, data: dict = None) -> None: ...
    def publish_delayed(self, event_name: str, data: dict, delay_ms: int) -> None: ...
```

### 4.2 AnalysisWorker

```python
class AnalysisWorker(QThread):
    """分析工作线程"""

    sig_finished = pyqtSignal(str, dict)   # (analysis_name, result)
    sig_error = pyqtSignal(str, str)       # (analysis_name, error_msg)
    sig_progress = pyqtSignal(int, int)    # (current, total)

    def __init__(self, analysis_func: callable, params: dict): ...
    def run(self) -> None: ...
    def cancel(self) -> None: ...
```

### 4.3 ThreadPoolManager

```python
class ThreadPoolManager:
    """线程池管理"""

    def __init__(self, max_workers: int = 4): ...
    def submit(self, func: callable, *args, **kwargs) -> Future: ...
    def submit_analysis(self, analysis_name: str, func: callable, params: dict) -> AnalysisWorker: ...
    def cancel_all(self) -> None: ...
    def active_count(self) -> int: ...
    def wait_all(self) -> None: ...
```

---

## 5. BridgeController -- 桥接控制器

文件路径: `src/axaltyx_bridge/`

### 5.1 BridgeController

```python
class BridgeController(QObject):
    """
    桥接控制器单例
    统一管理 GUI <-> Core 之间的所有通信
    """

    _instance = None

    def __new__(cls, *args, **kwargs): ...
    def __init__(self): ...

    # ---- 初始化 ----
    def initialize(self, core_engine, plot_engine, i18n_manager, theme_manager) -> None:
        """初始化所有子模块"""

    # ---- 数据操作 ----
    def load_data(self, path: str, file_type: str) -> None: ...
    def save_data(self, path: str, file_type: str, encoding: str = "utf-8") -> None: ...
    def new_dataset(self, rows: int = 100, cols: int = 100) -> None: ...
    def get_current_data(self) -> pd.DataFrame: ...
    def set_current_data(self, data: pd.DataFrame) -> None: ...

    # ---- 分析操作 ----
    def run_analysis(self, analysis_name: str, params: dict) -> None: ...
    def cancel_analysis(self, analysis_name: str) -> None: ...
    def get_analysis_names(self) -> list[str]: ...
    def get_analysis_params_schema(self, analysis_name: str) -> dict: ...

    # ---- 图表操作 ----
    def create_chart(self, chart_type: str, params: dict) -> None: ...
    def export_chart(self, chart_id: str, path: str, format: str) -> None: ...

    # ---- UI 操作 ----
    def change_language(self, lang_code: str) -> None: ...
    def change_theme(self, theme_name: str) -> None: ...
    def update_settings(self, settings: dict) -> None: ...
    def show_notification(self, ntype: str, title: str, message: str) -> None: ...
    def show_status(self, message: str, timeout: int = 0) -> None: ...

    # ---- 命令系统 ----
    def execute_command(self, command: CommandBase) -> None: ...
    def undo(self) -> None: ...
    def redo(self) -> None: ...

    # ---- 语法系统 ----
    def execute_syntax(self, syntax_string: str) -> None: ...
    def generate_syntax(self, analysis_name: str, params: dict) -> str: ...

    # ---- 事件系统 ----
    def subscribe(self, event_name: str, handler: callable) -> str: ...
    def unsubscribe(self, subscription_id: str) -> None: ...
    def publish(self, event_name: str, data: dict = None) -> None: ...

    # ---- 信号访问 ----
    @property
    def signals(self) -> BridgeSignals: ...
```

---

## 6. 分析名称注册表

### 6.1 ANALYSIS_REGISTRY

```python
ANALYSIS_REGISTRY = {
    # 描述统计
    "descriptive_stats": {
        "module": "axaltyx_core.descriptive",
        "function": "descriptive_stats",
        "category": "descriptive",
        "label_key": "analysis.descriptive_stats",
        "dialog": "DescriptiveDialog",
        "params_schema": {
            "vars": {"type": "list[str]", "required": True, "source": "variable_selector"},
            "stats": {"type": "list[str]", "required": False, "default": ["mean", "std", "min", "max"], "source": "checkbox_group"}
        }
    },
    "frequencies": {
        "module": "axaltyx_core.frequency",
        "function": "frequencies",
        "category": "frequency",
        "label_key": "analysis.frequencies",
        "dialog": "FrequenciesDialog",
        "params_schema": {
            "vars": {"type": "list[str]", "required": True, "source": "variable_selector"},
            "format": {"type": "str", "default": "table", "source": "radio_group"},
            "order": {"type": "str", "default": "ascending", "source": "radio_group"}
        }
    },
    "crosstabs": {
        "module": "axaltyx_core.crosstab",
        "function": "crosstabs",
        "category": "crosstab",
        "label_key": "analysis.crosstabs",
        "dialog": "CrosstabsDialog",
        "params_schema": {
            "row_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "col_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "layer_var": {"type": "str", "required": False, "source": "variable_selector_single"},
            "statistics": {"type": "list[str]", "required": False, "source": "checkbox_group"}
        }
    },
    "one_sample_t_test": {
        "module": "axaltyx_core.t_test",
        "function": "one_sample_t",
        "category": "t_test",
        "label_key": "analysis.one_sample_t_test",
        "dialog": "OneSampleTDialog",
        "params_schema": {
            "var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "test_value": {"type": "float", "default": 0, "source": "number_input"},
            "ci_level": {"type": "float", "default": 0.95, "source": "number_input"}
        }
    },
    "independent_t_test": {
        "module": "axaltyx_core.t_test",
        "function": "independent_t",
        "category": "t_test",
        "label_key": "analysis.independent_t_test",
        "dialog": "IndependentTDialog",
        "params_schema": {
            "test_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "group_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "equal_var": {"type": "bool", "default": True, "source": "checkbox"},
            "ci_level": {"type": "float", "default": 0.95, "source": "number_input"}
        }
    },
    "paired_t_test": {
        "module": "axaltyx_core.t_test",
        "function": "paired_t",
        "category": "t_test",
        "label_key": "analysis.paired_t_test",
        "dialog": "PairedTDialog",
        "params_schema": {
            "var1": {"type": "str", "required": True, "source": "variable_selector_single"},
            "var2": {"type": "str", "required": True, "source": "variable_selector_single"},
            "ci_level": {"type": "float", "default": 0.95, "source": "number_input"}
        }
    },
    "one_way_anova": {
        "module": "axaltyx_core.anova",
        "function": "one_way_anova",
        "category": "anova",
        "label_key": "analysis.one_way_anova",
        "dialog": "OneWayAnovaDialog",
        "params_schema": {
            "dependent_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "factor_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "post_hoc": {"type": "str", "default": None, "source": "dropdown"},
            "effect_size": {"type": "bool", "default": True, "source": "checkbox"}
        }
    },
    "linear_regression": {
        "module": "axaltyx_core.regression",
        "function": "linear_regression",
        "category": "regression",
        "label_key": "analysis.linear_regression",
        "dialog": "LinearRegressionDialog",
        "params_schema": {
            "dependent_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "independent_vars": {"type": "list[str]", "required": True, "source": "variable_selector"},
            "method": {"type": "str", "default": "enter", "source": "dropdown"},
            "ci_level": {"type": "float", "default": 0.95, "source": "number_input"}
        }
    },
    "logistic_regression": {
        "module": "axaltyx_core.regression",
        "function": "logistic_regression",
        "category": "regression",
        "label_key": "analysis.logistic_regression",
        "dialog": "LogisticRegressionDialog",
        "params_schema": {
            "dependent_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "independent_vars": {"type": "list[str]", "required": True, "source": "variable_selector"},
            "method": {"type": "str", "default": "enter", "source": "dropdown"},
            "ci_level": {"type": "float", "default": 0.95, "source": "number_input"}
        }
    },
    "exploratory_factor_analysis": {
        "module": "axaltyx_core.factor_analysis",
        "function": "exploratory_factor_analysis",
        "category": "dimension_reduction",
        "label_key": "analysis.efa",
        "dialog": "EFADialog",
        "params_schema": {
            "vars": {"type": "list[str]", "required": True, "source": "variable_selector"},
            "n_factors": {"type": "int", "default": "kaiser", "source": "number_or_auto"},
            "rotation": {"type": "str", "default": "varimax", "source": "dropdown"},
            "extraction": {"type": "str", "default": "principal_axis", "source": "dropdown"}
        }
    },
    "kmeans_clustering": {
        "module": "axaltyx_core.clustering",
        "function": "kmeans_clustering",
        "category": "classification",
        "label_key": "analysis.kmeans",
        "dialog": "KMeansDialog",
        "params_schema": {
            "vars": {"type": "list[str]", "required": True, "source": "variable_selector"},
            "n_clusters": {"type": "int", "required": True, "source": "number_input"},
            "init": {"type": "str", "default": "k-means++", "source": "dropdown"},
            "standardize": {"type": "bool", "default": True, "source": "checkbox"}
        }
    },
    "kaplan_meier": {
        "module": "axaltyx_core.survival",
        "function": "kaplan_meier",
        "category": "survival",
        "label_key": "analysis.kaplan_meier",
        "dialog": "KaplanMeierDialog",
        "params_schema": {
            "time_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "event_var": {"type": "str", "required": True, "source": "variable_selector_single"},
            "group_var": {"type": "str", "required": False, "source": "variable_selector_single"},
            "conf_level": {"type": "float", "default": 0.95, "source": "number_input"}
        }
    },
    "cronbach_alpha": {
        "module": "axaltyx_core.reliability",
        "function": "cronbach_alpha",
        "category": "reliability",
        "label_key": "analysis.cronbach_alpha",
        "dialog": "CronbachAlphaDialog",
        "params_schema": {
            "vars": {"type": "list[str]", "required": True, "source": "variable_selector"}
        }
    },
    # ... 其他分析方法的注册信息
}
```
