from PyQt6.QtCore import QObject, pyqtSlot


class UISlots(QObject):
    """UI 操作槽函数"""

    def __init__(self, i18n_manager, theme_manager, signals):
        super().__init__()
        self.i18n_manager = i18n_manager
        self.theme_manager = theme_manager
        self.signals = signals

    @pyqtSlot(str)
    def on_language_changed(self, lang_code: str) -> None:
        """处理语言切换"""
        try:
            # 调用国际化管理器切换语言
            if self.i18n_manager:
                self.i18n_manager.set_language(lang_code)
            # 这里可以添加额外的处理逻辑
        except Exception as e:
            # 处理错误情况
            print(f"Error changing language: {str(e)}")

    @pyqtSlot(str)
    def on_theme_changed(self, theme_name: str) -> None:
        """处理主题切换"""
        try:
            # 调用主题管理器切换主题
            if self.theme_manager:
                self.theme_manager.set_theme(theme_name)
            # 这里可以添加额外的处理逻辑
        except Exception as e:
            # 处理错误情况
            print(f"Error changing theme: {str(e)}")

    @pyqtSlot(dict)
    def on_settings_changed(self, settings: dict) -> None:
        """处理设置变更"""
        try:
            # 处理设置变更
            # 这里可以添加具体的设置处理逻辑
            print(f"Settings changed: {settings}")
            # 这里可以添加额外的处理逻辑
        except Exception as e:
            # 处理错误情况
            print(f"Error changing settings: {str(e)}")

    @pyqtSlot(str)
    def on_syntax_execute(self, syntax_string: str) -> None:
        """处理语法执行"""
        try:
            # 处理语法执行
            # 这里可以添加具体的语法执行逻辑
            print(f"Executing syntax: {syntax_string}")
            # 这里可以添加额外的处理逻辑
        except Exception as e:
            # 处理错误情况
            print(f"Error executing syntax: {str(e)}")
