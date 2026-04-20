from PyQt6.QtCore import QObject
from axaltyx_bridge.signals.bridge_signals import BridgeSignals
from axaltyx_bridge.slots.data_slots import DataSlots
from axaltyx_bridge.slots.analysis_slots import AnalysisSlots
from axaltyx_bridge.slots.chart_slots import ChartSlots
from axaltyx_bridge.slots.ui_slots import UISlots
from axaltyx_bridge.commands.history import CommandHistory
from axaltyx_bridge.events.event_bus import EventBus
from axaltyx_bridge.events.worker import ThreadPoolManager


class BridgeController(QObject):
    """
    桥接控制器单例
    统一管理 GUI <-> Core 之间的所有通信
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # 初始化实例
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """初始化控制器"""
        super().__init__()
        
        # 初始化信号
        self._signals = BridgeSignals()
        
        # 初始化事件总线
        self._event_bus = EventBus()
        
        # 初始化线程池
        self._thread_pool = ThreadPoolManager()
        
        # 初始化命令历史
        self._command_history = CommandHistory()
        
        # 初始化槽函数
        self._data_slots = None
        self._analysis_slots = None
        self._chart_slots = None
        self._ui_slots = None
        
        # 初始化核心引擎
        self._core_engine = None
        self._plot_engine = None
        self._i18n_manager = None
        self._theme_manager = None
        
        # 当前数据
        self._current_data = None
        
        # 标记初始化完成
        self._initialized = True

    def __init__(self):
        """初始化控制器"""
        pass

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

    def _connect_signals(self):
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
        return self._current_data

    def set_current_data(self, data) -> None:
        """设置当前数据"""
        self._current_data = data

    # ---- 分析操作 ----
    def run_analysis(self, analysis_name: str, params: dict) -> None:
        """运行分析"""
        self._signals.sig_analysis_requested.emit(analysis_name, params)

    def cancel_analysis(self, analysis_name: str) -> None:
        """取消分析"""
        # 这里可以实现取消分析的逻辑
        pass

    def get_analysis_names(self) -> list[str]:
        """获取分析名称列表"""
        from axaltyx_bridge.registry import ANALYSIS_REGISTRY
        return list(ANALYSIS_REGISTRY.keys())

    def get_analysis_params_schema(self, analysis_name: str) -> dict:
        """获取分析参数 schema"""
        from axaltyx_bridge.registry import ANALYSIS_REGISTRY
        if analysis_name in ANALYSIS_REGISTRY:
            return ANALYSIS_REGISTRY[analysis_name].get('params_schema', {})
        return {}

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
        """显示状态栏消息"""
        self._signals.sig_status_message.emit(message, timeout)

    # ---- 命令系统 ----
    def execute_command(self, command) -> None:
        """执行命令"""
        self._command_history.push(command)

    def undo(self) -> None:
        """撤销操作"""
        self._command_history.undo()

    def redo(self) -> None:
        """重做操作"""
        self._command_history.redo()

    # ---- 语法系统 ----
    def execute_syntax(self, syntax_string: str) -> None:
        """执行语法"""
        self._signals.sig_syntax_execute.emit(syntax_string)

    def generate_syntax(self, analysis_name: str, params: dict) -> str:
        """生成语法"""
        # 这里可以实现生成语法的逻辑
        return f"# Syntax for {analysis_name} with params {params}"

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

    @property
    def command_history(self) -> CommandHistory:
        """获取命令历史"""
        return self._command_history

    @property
    def thread_pool(self) -> ThreadPoolManager:
        """获取线程池"""
        return self._thread_pool

    @property
    def event_bus(self) -> EventBus:
        """获取事件总线"""
        return self._event_bus
