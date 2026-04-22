from PyQt6.QtCore import QObject, pyqtSlot
import uuid


class ChartSlots(QObject):
    """图表操作槽函数"""

    def __init__(self, plot_engine, signals):
        super().__init__()
        self.plot_engine = plot_engine
        self.signals = signals
        self.charts = {}  # 存储已创建的图表

    @pyqtSlot(str, dict)
    def on_chart_requested(self, chart_type: str, params: dict) -> None:
        """处理图表创建请求"""
        try:
            # 生成唯一的图表 ID
            chart_id = str(uuid.uuid4())
            
            # 检查绘图引擎是否存在
            if not self.plot_engine:
                raise Exception("Plot engine not initialized")
                
            # 调用绘图引擎创建图表
            result = self.plot_engine.create_chart(chart_type, params)
            
            if result.get("success"):
                # 存储图表
                self.charts[chart_id] = result.get("results", {})
                
                # 发射图表创建成功信号
                figure = result["results"].get("figure")
                self.signals.sig_chart_created.emit(chart_id, figure)
            else:
                # 处理错误情况
                error_msg = result.get("error", "Failed to create chart")
                print(f"Chart creation failed: {error_msg}")
                
        except Exception as e:
            # 处理异常
            print(f"Error creating chart: {str(e)}")

    @pyqtSlot(str, str, str)
    def on_export_requested(self, chart_id: str, path: str, format: str) -> None:
        """处理图表导出请求"""
        try:
            # 检查图表是否存在
            if chart_id not in self.charts:
                raise ValueError(f"Chart with id {chart_id} not found")
            
            # 获取图表对象
            chart_info = self.charts[chart_id]
            figure = chart_info.get("figure")
            
            if not figure:
                raise ValueError("Chart figure not found")
            
            # 检查绘图引擎是否存在
            if not self.plot_engine:
                raise Exception("Plot engine not initialized")
                
            # 调用绘图引擎导出图表
            result = self.plot_engine.export_chart(figure, path, format)
            
            # 发射导出完成信号
            self.signals.sig_chart_export_completed.emit(result)
            
        except Exception as e:
            # 处理错误情况
            error_result = {
                "success": False,
                "error": str(e),
                "chart_id": chart_id,
                "path": path,
                "format": format
            }
            self.signals.sig_chart_export_completed.emit(error_result)
