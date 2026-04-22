from PyQt6.QtCore import QObject, pyqtSlot
import logging

# 配置日志
logger = logging.getLogger(__name__)

class UISlots(QObject):
    """UI 操作槽函数"""

    def __init__(self, i18n_manager, theme_manager, signals, app_controller=None):
        super().__init__()
        self.i18n_manager = i18n_manager
        self.theme_manager = theme_manager
        self.signals = signals
        self.app_controller = app_controller

    @pyqtSlot(str)
    def on_language_changed(self, lang_code: str) -> None:
        """处理语言切换"""
        try:
            # 调用国际化管理器切换语言
            if self.i18n_manager:
                logger.info(f"Changing language to: {lang_code}")
                self.i18n_manager.set_language(lang_code)
                
                # 发送语言变更完成信号
                if hasattr(self.signals, 'sig_language_apply_finished'):
                    self.signals.sig_language_apply_finished.emit(lang_code)
                    
                # 更新所有UI组件的文本
                if self.app_controller and hasattr(self.app_controller, 'refresh_ui'):
                    self.app_controller.refresh_ui()
                    
        except Exception as e:
            logger.error(f"Error changing language: {str(e)}", exc_info=True)
            if hasattr(self.signals, 'sig_error_occurred'):
                self.signals.sig_error_occurred.emit(f"语言切换失败: {str(e)}")

    @pyqtSlot(str)
    def on_theme_changed(self, theme_name: str) -> None:
        """处理主题切换"""
        try:
            # 调用主题管理器切换主题
            if self.theme_manager:
                logger.info(f"Changing theme to: {theme_name}")
                self.theme_manager.set_theme(theme_name)
                
                # 发送主题变更完成信号
                if hasattr(self.signals, 'sig_theme_apply_finished'):
                    self.signals.sig_theme_apply_finished.emit(theme_name)
                    
        except Exception as e:
            logger.error(f"Error changing theme: {str(e)}", exc_info=True)
            if hasattr(self.signals, 'sig_error_occurred'):
                self.signals.sig_error_occurred.emit(f"主题切换失败: {str(e)}")

    @pyqtSlot(dict)
    def on_settings_changed(self, settings: dict) -> None:
        """处理设置变更"""
        try:
            logger.info(f"Settings changed: {settings}")
            
            # 处理常规设置
            if 'general' in settings:
                general = settings['general']
                
                # 自动保存设置
                if 'auto_save' in general and hasattr(self, '_auto_save_manager'):
                    self._auto_save_manager.set_enabled(general['auto_save'])
                
                # 自动保存间隔
                if 'auto_save_interval' in general and hasattr(self, '_auto_save_manager'):
                    self._auto_save_manager.set_interval(general['auto_save_interval'])
            
            # 处理输出设置
            if 'output' in settings:
                output = settings['output']
                
                # 图表格式
                if 'chart_format' in output and hasattr(self, '_chart_manager'):
                    self._chart_manager.set_default_format(output['chart_format'])
                
                # 图表分辨率
                if 'chart_dpi' in output and hasattr(self, '_chart_manager'):
                    self._chart_manager.set_default_dpi(output['chart_dpi'])
            
            # 发送设置变更完成信号
            if hasattr(self.signals, 'sig_settings_apply_finished'):
                self.signals.sig_settings_apply_finished.emit(settings)
                
        except Exception as e:
            logger.error(f"Error changing settings: {str(e)}", exc_info=True)
            if hasattr(self.signals, 'sig_error_occurred'):
                self.signals.sig_error_occurred.emit(f"设置变更失败: {str(e)}")

    @pyqtSlot(str)
    def on_syntax_execute(self, syntax_string: str) -> None:
        """处理语法执行"""
        try:
            logger.info(f"Executing syntax: {syntax_string}")
            
            # 语法执行逻辑
            if self.app_controller and hasattr(self.app_controller, 'execute_syntax'):
                # 发送执行开始信号
                if hasattr(self.signals, 'sig_syntax_execute_started'):
                    self.signals.sig_syntax_execute_started.emit(syntax_string)
                
                # 执行语法
                result = self.app_controller.execute_syntax(syntax_string)
                
                # 发送执行完成信号
                if hasattr(self.signals, 'sig_syntax_execute_finished'):
                    self.signals.sig_syntax_execute_finished.emit(result)
            else:
                logger.warning("No app_controller available to execute syntax")
                
        except Exception as e:
            logger.error(f"Error executing syntax: {str(e)}", exc_info=True)
            if hasattr(self.signals, 'sig_error_occurred'):
                self.signals.sig_error_occurred.emit(f"语法执行失败: {str(e)}")
            if hasattr(self.signals, 'sig_syntax_execute_failed'):
                self.signals.sig_syntax_execute_failed.emit(str(e))
