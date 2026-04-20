from PyQt6.QtCore import QObject, pyqtSlot
import importlib


class AnalysisSlots(QObject):
    """分析操作槽函数"""

    def __init__(self, core_engine, signals):
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
            # 1. 验证参数
            if not analysis_name:
                raise ValueError("Analysis name is required")
            
            # 2. 发射分析开始信号
            self.signals.sig_analysis_started.emit(analysis_name)
            
            # 3-4. 执行分析（这里简化处理，实际应在工作线程中执行）
            # 发射进度信号
            self.signals.sig_analysis_progress.emit(analysis_name, 0, 100)
            
            # 执行分析
            result = self._execute_analysis(analysis_name, params)
            
            # 发射进度完成信号
            self.signals.sig_analysis_progress.emit(analysis_name, 100, 100)
            
            # 5. 发射分析完成信号
            self.signals.sig_analysis_completed.emit(analysis_name, result)
            
        except Exception as e:
            # 发射分析失败信号
            self.signals.sig_analysis_failed.emit(analysis_name, str(e))

    def _execute_analysis(self, analysis_name: str, params: dict) -> dict:
        """分发到对应的核心模块函数"""
        try:
            # 获取分析函数
            analysis_func = self._get_analysis_function(analysis_name)
            if not analysis_func:
                raise ValueError(f"Analysis function not found: {analysis_name}")
            
            # 执行分析
            result = analysis_func(params)
            
            # 确保返回格式正确
            if isinstance(result, dict):
                return result
            else:
                return {"success": True, "results": result}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _get_analysis_function(self, analysis_name: str) -> callable:
        """根据分析名称获取核心函数引用"""
        try:
            # 这里简化处理，实际应从 ANALYSIS_REGISTRY 中获取
            # 暂时返回一个模拟函数
            def mock_analysis(params):
                return {"success": True, "results": f"Analysis {analysis_name} executed with params: {params}"}
            return mock_analysis
            
        except Exception as e:
            print(f"Error getting analysis function: {str(e)}")
            return None
