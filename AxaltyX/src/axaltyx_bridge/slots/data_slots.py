from PyQt6.QtCore import QObject, pyqtSlot


class DataSlots(QObject):
    """数据操作槽函数"""

    def __init__(self, core_engine, signals):
        """
        初始化数据槽函数
        
        Args:
            core_engine: 核心引擎实例
            signals: BridgeSignals 实例
        """
        super().__init__()
        self.core_engine = core_engine
        self.signals = signals

    @pyqtSlot(str, str)
    def on_load_requested(self, path: str, file_type: str) -> None:
        """处理数据加载请求，调用 core 引擎，完成后发射信号"""
        try:
            # 调用核心引擎加载数据
            result = self.core_engine.load_data(path, file_type)
            # 发射加载完成信号
            self.signals.sig_data_load_completed.emit(result)
        except Exception as e:
            # 发射加载失败信号
            self.signals.sig_data_load_completed.emit({
                "success": False,
                "error": str(e)
            })

    @pyqtSlot(str, str, str)
    def on_save_requested(self, path: str, file_type: str, encoding: str) -> None:
        """处理数据保存请求"""
        try:
            # 调用核心引擎保存数据
            result = self.core_engine.save_data(path, file_type, encoding)
            # 发射保存完成信号
            self.signals.sig_data_save_completed.emit(result)
        except Exception as e:
            # 发射保存失败信号
            self.signals.sig_data_save_completed.emit({
                "success": False,
                "error": str(e)
            })

    @pyqtSlot(int, int)
    def on_new_requested(self, rows: int, cols: int) -> None:
        """处理新建数据集请求"""
        try:
            # 调用核心引擎新建数据集
            result = self.core_engine.new_dataset(rows, cols)
            # 发射新建完成信号
            self.signals.sig_data_new_completed.emit(result)
        except Exception as e:
            # 发射新建失败信号
            self.signals.sig_data_new_completed.emit({
                "success": False,
                "error": str(e)
            })

    @pyqtSlot(dict)
    def on_data_changed(self, change_info: dict) -> None:
        """处理数据变更通知"""
        try:
            # 调用核心引擎处理数据变更
            self.core_engine.update_data(change_info)
            # 可以在这里添加额外的处理逻辑
        except Exception as e:
            # 处理错误
            print(f"Data change error: {str(e)}")

    @pyqtSlot(str, dict)
    def on_variable_changed(self, var_name: str, metadata: dict) -> None:
        """处理变量属性变更"""
        try:
            # 调用核心引擎更新变量属性
            self.core_engine.update_variable(var_name, metadata)
            # 可以在这里添加额外的处理逻辑
        except Exception as e:
            # 处理错误
            print(f"Variable change error: {str(e)}")
