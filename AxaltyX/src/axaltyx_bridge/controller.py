from PyQt6.QtCore import QObject
from .signals.bridge_signals import BridgeSignals
from .slots.data_slots import DataSlots
from .slots.analysis_slots import AnalysisSlots
from .slots.chart_slots import ChartSlots
from .slots.ui_slots import UISlots
from .commands.history import CommandHistory
from .events.event_bus import EventBus
from .events.worker import ThreadPoolManager


class BridgeController(QObject):
    """
    桥接控制器单例
    统一管理 GUI <-> Core 之间的所有通信
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """实现单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化控制器"""
        # 确保父类初始化
        super().__init__()
        
        # 检查是否已经初始化
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        # 初始化信号
        try:
            self._signals = BridgeSignals()
        except Exception as e:
            print(f"Error initializing signals: {e}")
            raise
        
        # 初始化命令历史
        try:
            self._command_history = CommandHistory()
        except Exception as e:
            print(f"Error initializing command history: {e}")
            raise
        
        # 初始化事件总线
        try:
            self._event_bus = EventBus()
        except Exception as e:
            print(f"Error initializing event bus: {e}")
            raise
        
        # 初始化线程池管理器
        try:
            self._thread_pool = ThreadPoolManager()
        except Exception as e:
            print(f"Error initializing thread pool: {e}")
            raise
        
        # 初始化槽函数
        self._data_slots = None
        self._analysis_slots = None
        self._chart_slots = None
        self._ui_slots = None
        
        # 存储引擎引用
        self._core_engine = None
        self._plot_engine = None
        self._i18n_manager = None
        self._theme_manager = None
        
        # 标记初始化完成
        self._initialized = True

    # ---- 初始化 ----
    def initialize(self, core_engine, plot_engine, i18n_manager, theme_manager) -> None:
        """初始化所有子模块"""
        self._core_engine = core_engine
        self._plot_engine = plot_engine
        self._i18n_manager = i18n_manager
        self._theme_manager = theme_manager
        
        # 初始化槽函数
        self._data_slots = DataSlots(core_engine, self._signals)
        self._analysis_slots = AnalysisSlots(core_engine, self._signals)
        self._chart_slots = ChartSlots(plot_engine, self._signals)
        self._ui_slots = UISlots(i18n_manager, theme_manager, self._signals)
        
        # 连接信号和槽
        self._connect_signals()

    def _connect_signals(self) -> None:
        """连接信号和槽"""
        # 数据操作信号
        self._signals.sig_data_load_requested.connect(self._data_slots.on_load_requested)
        self._signals.sig_data_save_requested.connect(self._data_slots.on_save_requested)
        self._signals.sig_data_new_requested.connect(self._data_slots.on_new_requested)
        self._signals.sig_data_changed.connect(self._data_slots.on_data_changed)
        self._signals.sig_variable_changed.connect(self._data_slots.on_variable_changed)
        
        # 分析操作信号
        self._signals.sig_analysis_requested.connect(self._analysis_slots.on_analysis_requested)
        
        # 图表操作信号
        self._signals.sig_chart_requested.connect(self._chart_slots.on_chart_requested)
        self._signals.sig_chart_export_requested.connect(self._chart_slots.on_export_requested)
        
        # UI 操作信号
        self._signals.sig_language_changed.connect(self._ui_slots.on_language_changed)
        self._signals.sig_theme_changed.connect(self._ui_slots.on_theme_changed)
        self._signals.sig_settings_changed.connect(self._ui_slots.on_settings_changed)
        self._signals.sig_syntax_execute.connect(self._ui_slots.on_syntax_execute)

    # ---- 数据操作 ----
    def load_data(self, path: str, file_type: str) -> None:
        """加载数据"""
        self._signals.sig_data_load_requested.emit(path, file_type)

    def save_data(self, path: str, file_type: str, encoding: str = "utf-8") -> None:
        """保存数据"""
        self._signals.sig_data_save_requested.emit(path, file_type, encoding)

    def new_dataset(self, rows: int = 100, cols: int = 100) -> None:
        """新建数据集"""
        self._signals.sig_data_new_requested.emit(rows, cols)

    def get_current_data(self):
        """获取当前数据"""
        if self._core_engine:
            return self._core_engine.get_current_data()
        return None

    def set_current_data(self, data) -> None:
        """设置当前数据"""
        if self._core_engine:
            self._core_engine.set_current_data(data)

    # ---- 分析操作 ----
    def run_analysis(self, analysis_name: str, params: dict) -> None:
        """运行分析"""
        self._signals.sig_analysis_requested.emit(analysis_name, params)

    def cancel_analysis(self, analysis_name: str) -> None:
        """取消分析"""
        # 实现取消分析逻辑
        if self._analysis_slots and hasattr(self._analysis_slots, 'cancel_analysis'):
            self._analysis_slots.cancel_analysis(analysis_name)
        else:
            # 发布取消分析事件
            self.publish('analysis_cancelled', {'analysis_name': analysis_name})

    def get_analysis_names(self) -> list[str]:
        """获取分析名称列表"""
        # 从核心引擎获取分析名称
        if self._core_engine and hasattr(self._core_engine, 'get_analysis_registry'):
            registry = self._core_engine.get_analysis_registry()
            return list(registry.keys())
        # 硬编码的分析名称列表作为后备
        return [
            'descriptive', 'frequency', 'crosstab', 'correlation', 'ttest',
            'anova', 'regression', 'clustering', 'factor', 'nonparametric'
        ]

    def get_analysis_params_schema(self, analysis_name: str) -> dict:
        """获取分析参数 schema"""
        # 从核心引擎获取参数 schema
        if self._core_engine and hasattr(self._core_engine, 'get_analysis_registry'):
            registry = self._core_engine.get_analysis_registry()
            if analysis_name in registry:
                return registry[analysis_name].get('params_schema', {})
        # 返回默认 schema
        return {
            'variables': {'type': 'list', 'required': True},
            'options': {'type': 'dict', 'default': {}}
        }

    # ---- 图表操作 ----
    def create_chart(self, chart_type: str, params: dict) -> None:
        """创建图表"""
        self._signals.sig_chart_requested.emit(chart_type, params)

    def export_chart(self, chart_id: str, path: str, format: str) -> None:
        """导出图表"""
        self._signals.sig_chart_export_requested.emit(chart_id, path, format)

    # ---- UI 操作 ----
    def change_language(self, lang_code: str) -> None:
        """切换语言"""
        self._signals.sig_language_changed.emit(lang_code)

    def change_theme(self, theme_name: str) -> None:
        """切换主题"""
        self._signals.sig_theme_changed.emit(theme_name)

    def update_settings(self, settings: dict) -> None:
        """更新设置"""
        self._signals.sig_settings_changed.emit(settings)

    def show_notification(self, ntype: str, title: str, message: str) -> None:
        """显示通知"""
        self._signals.sig_notification.emit(ntype, title, message)

    def show_status(self, message: str, timeout: int = 0) -> None:
        """显示状态消息"""
        self._signals.sig_status_message.emit(message, timeout)

    # ---- 命令系统 ----
    def execute_command(self, command) -> None:
        """执行命令"""
        result = command.execute()
        if result.get("success"):
            self._command_history.push(command)

    def undo(self) -> None:
        """撤销命令"""
        self._command_history.undo()

    def redo(self) -> None:
        """重做命令"""
        self._command_history.redo()

    # ---- 语法系统 ----
    def execute_syntax(self, syntax_string: str) -> None:
        """执行语法"""
        self._signals.sig_syntax_execute.emit(syntax_string)

    def generate_syntax(self, analysis_name: str, params: dict) -> str:
        """生成语法"""
        # 这里简化处理，实际应实现语法生成逻辑
        return f"# Syntax for {analysis_name}\n# Params: {params}"

    # ---- 事件系统 ----
    def subscribe(self, event_name: str, handler: callable) -> str:
        """订阅事件"""
        return self._event_bus.subscribe(event_name, handler)

    def unsubscribe(self, subscription_id: str) -> None:
        """取消订阅"""
        self._event_bus.unsubscribe(subscription_id)

    def publish(self, event_name: str, data: dict = None) -> None:
        """发布事件"""
        self._event_bus.publish(event_name, data)

    # ---- 信号访问 ----
    @property
    def signals(self) -> BridgeSignals:
        """获取信号对象"""
        return self._signals
