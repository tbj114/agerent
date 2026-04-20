from PyQt6.QtCore import QObject, pyqtSlot
import importlib


class AnalysisSlots(QObject):
    """分析操作槽函数"""

    def __init__(self, core_engine, signals):
        """
        初始化分析槽函数
        
        Args:
            core_engine: 核心引擎实例
            signals: BridgeSignals 实例
        """
        super().__init__()
        self.core_engine = core_engine
        self.signals = signals

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
        try:
            # 验证参数
            if not analysis_name:
                self.signals.sig_analysis_failed.emit(analysis_name, "Analysis name is required")
                return
            
            # 发射分析开始信号
            self.signals.sig_analysis_started.emit(analysis_name)
            
            # 执行分析
            result = self._execute_analysis(analysis_name, params)
            
            # 发射分析完成信号
            self.signals.sig_analysis_completed.emit(analysis_name, result)
        except Exception as e:
            # 发射分析失败信号
            self.signals.sig_analysis_failed.emit(analysis_name, str(e))

    def _execute_analysis(self, analysis_name: str, params: dict) -> dict:
        """分发到对应的核心模块函数"""
        # 获取分析函数
        analysis_func = self._get_analysis_function(analysis_name)
        
        if not analysis_func:
            raise ValueError(f"Analysis function {analysis_name} not found")
        
        # 执行分析
        result = analysis_func(**params)
        
        return result

    def _get_analysis_function(self, analysis_name: str) -> callable:
        """根据分析名称获取核心函数引用"""
        # 从分析注册表中获取模块和函数信息
        from axaltyx_bridge.registry import ANALYSIS_REGISTRY
        
        if analysis_name not in ANALYSIS_REGISTRY:
            return None
        
        # 获取模块和函数信息
        registry_info = ANALYSIS_REGISTRY[analysis_name]
        module_name = registry_info["module"]
        function_name = registry_info["function"]
        
        try:
            # 导入模块
            module = importlib.import_module(module_name)
            # 获取函数
            analysis_func = getattr(module, function_name)
            return analysis_func
        except ImportError:
            print(f"Module {module_name} not found")
            return None
        except AttributeError:
            print(f"Function {function_name} not found in module {module_name}")
            return None
