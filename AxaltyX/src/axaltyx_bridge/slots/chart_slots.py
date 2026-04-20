from PyQt6.QtCore import QObject, pyqtSlot
import uuid


class ChartSlots(QObject):
    """图表操作槽函数"""

    def __init__(self, plot_engine, signals):
        """
        初始化图表槽函数
        
        Args:
            plot_engine: 绘图引擎实例
            signals: BridgeSignals 实例
        """
        super().__init__()
        self.plot_engine = plot_engine
        self.signals = signals

    @pyqtSlot(str, dict)
    def on_chart_requested(self, chart_type: str, params: dict) -> None:
        """处理图表创建请求"""
        try:
            # 生成唯一的图表 ID
            chart_id = str(uuid.uuid4())
            
            # 调用绘图引擎创建图表
            result = self._create_chart(chart_type, params)
            
            if result["success"]:
                # 发射图表创建成功信号
                self.signals.sig_chart_created.emit(chart_id, result["results"]["figure"])
            else:
                # 处理图表创建失败
                print(f"Chart creation failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            # 处理错误
            print(f"Chart request error: {str(e)}")

    @pyqtSlot(str, str, str)
    def on_export_requested(self, chart_id: str, path: str, format: str) -> None:
        """处理图表导出请求"""
        try:
            # 这里需要获取图表对象，实际实现中可能需要一个图表管理器
            # 暂时假设我们有一个方法可以获取图表对象
            chart = self._get_chart_by_id(chart_id)
            
            if chart:
                # 调用绘图引擎导出图表
                result = self.plot_engine.export_chart(chart, path, format)
                # 发射导出完成信号
                self.signals.sig_chart_export_completed.emit(result)
            else:
                # 发射导出失败信号
                self.signals.sig_chart_export_completed.emit({
                    "success": False,
                    "error": f"Chart with id {chart_id} not found"
                })
        except Exception as e:
            # 发射导出失败信号
            self.signals.sig_chart_export_completed.emit({
                "success": False,
                "error": str(e)
            })

    def _create_chart(self, chart_type: str, params: dict) -> dict:
        """根据图表类型创建图表"""
        # 根据图表类型调用对应的绘图函数
        # 这里需要根据实际的绘图引擎接口进行调整
        if hasattr(self.plot_engine, chart_type):
            chart_func = getattr(self.plot_engine, chart_type)
            return chart_func(**params)
        else:
            # 尝试从不同模块中获取图表函数
            try:
                # 基础图表
                from axaltyx_plot.basic.charts import bar_chart, pie_chart, scatter_plot, line_chart
                # 统计图表
                from axaltyx_plot.statistical.stat_charts import roc_curve, pp_plot, qq_plot
                # 高级图表
                from axaltyx_plot.advanced.advanced_charts import heatmap, three_d_scatter
                # 交互式图表
                from axaltyx_plot.interactive.interactive_charts import interactive_scatter, dynamic_line_chart
                
                # 图表函数映射
                chart_functions = {
                    "bar_chart": bar_chart,
                    "pie_chart": pie_chart,
                    "scatter_plot": scatter_plot,
                    "line_chart": line_chart,
                    "roc_curve": roc_curve,
                    "pp_plot": pp_plot,
                    "qq_plot": qq_plot,
                    "heatmap": heatmap,
                    "three_d_scatter": three_d_scatter,
                    "interactive_scatter": interactive_scatter,
                    "dynamic_line_chart": dynamic_line_chart
                }
                
                if chart_type in chart_functions:
                    return chart_functions[chart_type](**params)
                else:
                    return {
                        "success": False,
                        "error": f"Chart type {chart_type} not supported"
                    }
            except ImportError as e:
                return {
                    "success": False,
                    "error": f"Error importing chart modules: {str(e)}"
                }

    def _get_chart_by_id(self, chart_id: str):
        """根据图表 ID 获取图表对象"""
        # 实际实现中，这里可能需要一个图表管理器来存储和管理图表对象
        # 暂时返回 None，需要根据实际情况实现
        return None
