from PyQt6.QtCore import QObject, pyqtSlot
import logging
import time

# 配置日志
logger = logging.getLogger(__name__)

class DataSlots(QObject):
    """数据操作槽函数"""

    def __init__(self, core_engine, signals, history_manager=None):
        super().__init__()
        self.core_engine = core_engine
        self.signals = signals
        self.history_manager = history_manager

    @pyqtSlot(str, str)
    def on_load_requested(self, path: str, file_type: str) -> None:
        """处理数据加载请求，调用 core 引擎，完成后发射信号"""
        start_time = time.time()
        
        try:
            logger.info(f"Loading data from: {path} (type: {file_type})")
            
            # 发送加载开始信号
            if hasattr(self.signals, 'sig_data_load_started'):
                self.signals.sig_data_load_started.emit(path, file_type)
                
            # 检查核心引擎是否存在
            if not self.core_engine:
                raise Exception("Core engine not initialized")
                
            # 调用核心引擎加载数据
            result = self.core_engine.load_data(path, file_type)
            
            # 记录加载时间
            elapsed = time.time() - start_time
            logger.info(f"Data loaded successfully in {elapsed:.2f}s")
            
            # 记录到历史记录
            if self.history_manager:
                self.history_manager.add_record(
                    action_type='load',
                    details={'path': path, 'file_type': file_type},
                    success=True
                )
            
            # 发射加载完成信号
            self.signals.sig_data_load_completed.emit(result)
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"Error loading data in {elapsed:.2f}s: {str(e)}", exc_info=True)
            
            # 记录到历史记录
            if self.history_manager:
                self.history_manager.add_record(
                    action_type='load',
                    details={'path': path, 'file_type': file_type},
                    success=False,
                    error=str(e)
                )
            
            # 处理错误情况
            error_result = {
                "success": False,
                "error": str(e),
                "path": path,
                "file_type": file_type,
                "timestamp": time.time()
            }
            self.signals.sig_data_load_completed.emit(error_result)
            
            # 发送错误信号
            if hasattr(self.signals, 'sig_error_occurred'):
                self.signals.sig_error_occurred.emit(f"数据加载失败: {str(e)}")

    @pyqtSlot(str, str, str)
    def on_save_requested(self, path: str, file_type: str, encoding: str) -> None:
        """处理数据保存请求"""
        start_time = time.time()
        
        try:
            logger.info(f"Saving data to: {path} (type: {file_type}, encoding: {encoding})")
            
            # 发送保存开始信号
            if hasattr(self.signals, 'sig_data_save_started'):
                self.signals.sig_data_save_started.emit(path, file_type)
                
            # 检查核心引擎是否存在
            if not self.core_engine:
                raise Exception("Core engine not initialized")
                
            # 调用核心引擎保存数据
            result = self.core_engine.save_data(path, file_type, encoding)
            
            elapsed = time.time() - start_time
            logger.info(f"Data saved successfully in {elapsed:.2f}s")
            
            # 记录到历史记录
            if self.history_manager:
                self.history_manager.add_record(
                    action_type='save',
                    details={'path': path, 'file_type': file_type},
                    success=True
                )
            
            # 发射保存完成信号
            self.signals.sig_data_save_completed.emit(result)
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"Error saving data in {elapsed:.2f}s: {str(e)}", exc_info=True)
            
            # 记录到历史记录
            if self.history_manager:
                self.history_manager.add_record(
                    action_type='save',
                    details={'path': path, 'file_type': file_type},
                    success=False,
                    error=str(e)
                )
            
            # 处理错误情况
            error_result = {
                "success": False,
                "error": str(e),
                "path": path,
                "file_type": file_type,
                "timestamp": time.time()
            }
            self.signals.sig_data_save_completed.emit(error_result)
            
            if hasattr(self.signals, 'sig_error_occurred'):
                self.signals.sig_error_occurred.emit(f"数据保存失败: {str(e)}")

    @pyqtSlot(int, int)
    def on_new_requested(self, rows: int, cols: int) -> None:
        """处理新建数据集请求"""
        try:
            logger.info(f"Creating new dataset: {rows} rows x {cols} cols")
            
            # 发送新建开始信号
            if hasattr(self.signals, 'sig_data_new_started'):
                self.signals.sig_data_new_started.emit(rows, cols)
                
            # 检查核心引擎是否存在
            if not self.core_engine:
                raise Exception("Core engine not initialized")
                
            # 调用核心引擎创建新数据集
            result = self.core_engine.create_new_data(rows, cols)
            
            # 记录到历史记录
            if self.history_manager:
                self.history_manager.add_record(
                    action_type='new_dataset',
                    details={'rows': rows, 'cols': cols},
                    success=True
                )
            
            # 发射新建完成信号
            self.signals.sig_data_new_completed.emit(result)
            
        except Exception as e:
            logger.error(f"Error creating new dataset: {str(e)}", exc_info=True)
            
            # 记录到历史记录
            if self.history_manager:
                self.history_manager.add_record(
                    action_type='new_dataset',
                    details={'rows': rows, 'cols': cols},
                    success=False,
                    error=str(e)
                )
            
            # 处理错误情况
            error_result = {
                "success": False,
                "error": str(e),
                "rows": rows,
                "cols": cols,
                "timestamp": time.time()
            }
            self.signals.sig_data_new_completed.emit(error_result)
            
            if hasattr(self.signals, 'sig_error_occurred'):
                self.signals.sig_error_occurred.emit(f"创建数据集失败: {str(e)}")

    @pyqtSlot(dict)
    def on_data_changed(self, change_info: dict) -> None:
        """处理数据变更通知"""
        try:
            logger.debug(f"Data changed: {change_info}")
            
            # 检查核心引擎是否存在
            if not self.core_engine:
                raise Exception("Core engine not initialized")
                
            # 调用核心引擎处理数据变更
            self.core_engine.update_data(change_info)
            
            # 触发自动保存（如果启用）
            if hasattr(self, '_auto_save_manager') and self._auto_save_manager.is_enabled():
                self._auto_save_manager.trigger_save_after_change()
                
            # 记录到历史记录
            if self.history_manager:
                self.history_manager.add_record(
                    action_type='data_edit',
                    details=change_info,
                    success=True
                )
            
            # 发送数据变更完成信号
            if hasattr(self.signals, 'sig_data_change_processed'):
                self.signals.sig_data_change_processed.emit(change_info)
                
        except Exception as e:
            logger.error(f"Error in data change: {str(e)}", exc_info=True)
            
            if hasattr(self.signals, 'sig_error_occurred'):
                self.signals.sig_error_occurred.emit(f"数据更新失败: {str(e)}")

    @pyqtSlot(str, dict)
    def on_variable_changed(self, var_name: str, metadata: dict) -> None:
        """处理变量属性变更"""
        try:
            logger.debug(f"Variable changed: {var_name} -> {metadata}")
            
            # 检查核心引擎是否存在
            if not self.core_engine:
                raise Exception("Core engine not initialized")
                
            # 调用核心引擎更新变量属性
            self.core_engine.update_variable_metadata(var_name, metadata)
            
            # 记录到历史记录
            if self.history_manager:
                self.history_manager.add_record(
                    action_type='variable_edit',
                    details={'var_name': var_name, 'metadata': metadata},
                    success=True
                )
            
            # 发送变量变更完成信号
            if hasattr(self.signals, 'sig_variable_change_processed'):
                self.signals.sig_variable_change_processed.emit(var_name, metadata)
                
        except Exception as e:
            logger.error(f"Error in variable change: {str(e)}", exc_info=True)
            
            if hasattr(self.signals, 'sig_error_occurred'):
                self.signals.sig_error_occurred.emit(f"变量属性更新失败: {str(e)}")
