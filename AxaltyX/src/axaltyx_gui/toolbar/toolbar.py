from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtCore import pyqtSignal
from src.axaltyx_i18n.manager import I18nManager

class AxaltyXToolBar(QToolBar):
    """自定义工具栏"""

    # 信号
    sig_action_triggered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.set_icon_size(24)
        self.init_toolbar()

    def init_toolbar(self):
        """初始化工具栏"""
        # 文件操作工具
        self.add_tool_action("new", "new", self.i18n.get_text("menu.file.new"), self._on_tool_action)
        self.add_tool_action("open", "open", self.i18n.get_text("menu.file.open"), self._on_tool_action)
        self.add_tool_action("save", "save", self.i18n.get_text("menu.file.save"), self._on_tool_action)
        self.add_separator()

        # 编辑操作工具
        self.add_tool_action("undo", "undo", self.i18n.get_text("menu.edit.undo"), self._on_tool_action)
        self.add_tool_action("redo", "redo", self.i18n.get_text("menu.edit.redo"), self._on_tool_action)
        self.add_separator()
        self.add_tool_action("cut", "cut", self.i18n.get_text("menu.edit.cut"), self._on_tool_action)
        self.add_tool_action("copy", "copy", self.i18n.get_text("menu.edit.copy"), self._on_tool_action)
        self.add_tool_action("paste", "paste", self.i18n.get_text("menu.edit.paste"), self._on_tool_action)
        self.add_separator()

        # 视图操作工具
        self.add_tool_action("data_view", "data", self.i18n.get_text("menu.view.data_view"), self._on_tool_action)
        self.add_tool_action("variable_view", "variable", self.i18n.get_text("menu.view.variable_view"), self._on_tool_action)
        self.add_tool_action("output_view", "output", self.i18n.get_text("menu.view.output_view"), self._on_tool_action)
        self.add_tool_action("syntax_view", "syntax", self.i18n.get_text("menu.view.syntax_view"), self._on_tool_action)
        self.add_separator()

        # 分析操作工具
        self.add_tool_action("descriptive", "descriptive", self.i18n.get_text("menu.analysis.descriptive"), self._on_tool_action)
        self.add_tool_action("frequency", "frequency", self.i18n.get_text("menu.analysis.frequency"), self._on_tool_action)
        self.add_tool_action("correlation", "correlation", self.i18n.get_text("menu.analysis.correlation"), self._on_tool_action)
        self.add_separator()

        # 图形操作工具
        self.add_tool_action("bar", "bar", self.i18n.get_text("menu.graph.bar"), self._on_tool_action)
        self.add_tool_action("histogram", "histogram", self.i18n.get_text("menu.graph.histogram"), self._on_tool_action)
        self.add_tool_action("scatter", "scatter", self.i18n.get_text("menu.graph.scatter"), self._on_tool_action)
        self.add_separator()

        # 工具操作工具
        self.add_tool_action("options", "settings", self.i18n.get_text("menu.tools.options"), self._on_tool_action)
        self.add_tool_action("help", "help", self.i18n.get_text("menu.help.contents"), self._on_tool_action)

    def add_tool_action(self, action_id: str, icon: str, tooltip: str, callback) -> QAction:
        """添加工具动作

        Args:
            action_id: 动作ID
            icon: 图标名称
            tooltip: 工具提示
            callback: 回调函数

        Returns:
            QAction: 创建的动作对象
        """
        # 这里使用占位图标，实际项目中应该从资源文件加载
        action = QAction(self)
        action.setObjectName(action_id)
        action.setText(tooltip)
        action.setToolTip(tooltip)
        # 创建一个简单的占位图标
        pixmap = QPixmap(24, 24)
        pixmap.fill()
        action.setIcon(QIcon(pixmap))
        action.triggered.connect(callback)
        self.addAction(action)
        return action

    def add_separator(self) -> None:
        """添加分隔符"""
        super().addSeparator()

    def set_icon_size(self, size: int) -> None:
        """设置图标大小

        Args:
            size: 图标大小
        """
        from PyQt6.QtCore import QSize
        super().setIconSize(QSize(size, size))

    def _on_tool_action(self):
        """工具动作处理"""
        action = self.sender()
        action_text = action.toolTip()
        action_object_name = action.objectName()
        print(f"Tool action triggered: {action_text} (ID: {action_object_name})")
        
        # 发送信号到主窗口
        self.sig_action_triggered.emit(action_object_name)
        
        # 这里添加具体的工具处理逻辑
        # 可以根据action_object_name执行不同的操作
        if action_object_name == "new":
            # 新建数据集
            if hasattr(self.parent(), 'new_dataset'):
                self.parent().new_dataset()
        elif action_object_name == "open":
            # 打开文件
            if hasattr(self.parent(), 'load_data'):
                from PyQt6.QtWidgets import QFileDialog
                file_filter = "CSV files (*.csv);;Excel files (*.xlsx);;Text files (*.txt);;JSON files (*.json);;All files (*.*)"
                path, _ = QFileDialog.getOpenFileName(self.parent(), "打开文件", "", file_filter)
                if path:
                    import os
                    _, ext = os.path.splitext(path)
                    file_type = ext.lower().lstrip('.')
                    self.parent().load_data(path, file_type)
        elif action_object_name == "save":
            # 保存文件
            if hasattr(self.parent(), 'save_data'):
                from PyQt6.QtWidgets import QFileDialog
                file_filter = "CSV files (*.csv);;Excel files (*.xlsx);;Text files (*.txt);;JSON files (*.json)"
                path, _ = QFileDialog.getSaveFileName(self.parent(), "保存文件", "", file_filter)
                if path:
                    import os
                    _, ext = os.path.splitext(path)
                    file_type = ext.lower().lstrip('.')
                    if not file_type:
                        # 默认保存为CSV
                        path += ".csv"
                        file_type = "csv"
                    self.parent().save_data(path, file_type)
        elif action_object_name == "undo":
            # 撤销操作
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("撤销操作")
        elif action_object_name == "redo":
            # 重做操作
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("重做操作")
        elif action_object_name == "cut":
            # 剪切操作
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("剪切操作")
        elif action_object_name == "copy":
            # 复制操作
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("复制操作")
        elif action_object_name == "paste":
            # 粘贴操作
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("粘贴操作")
        elif action_object_name == "data_view":
            # 数据视图
            if hasattr(self.parent(), 'switch_tab'):
                self.parent().switch_tab("data_view")
        elif action_object_name == "variable_view":
            # 变量视图
            if hasattr(self.parent(), 'switch_tab'):
                self.parent().switch_tab("variable_view")
        elif action_object_name == "output_view":
            # 输出视图
            if hasattr(self.parent(), 'switch_tab'):
                self.parent().switch_tab("output_view")
        elif action_object_name == "syntax_view":
            # 语法视图
            if hasattr(self.parent(), 'switch_tab'):
                self.parent().switch_tab("syntax_view")
        elif action_object_name == "descriptive":
            # 描述性统计
            if hasattr(self.parent(), 'show_analysis_dialog'):
                self.parent().show_analysis_dialog("descriptive")
        elif action_object_name == "frequency":
            # 频率分析
            if hasattr(self.parent(), 'show_analysis_dialog'):
                self.parent().show_analysis_dialog("frequency")
        elif action_object_name == "correlation":
            # 相关性分析
            if hasattr(self.parent(), 'show_analysis_dialog'):
                self.parent().show_analysis_dialog("correlation")
        elif action_object_name == "bar":
            # 条形图
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("创建条形图")
        elif action_object_name == "histogram":
            # 直方图
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("创建直方图")
        elif action_object_name == "scatter":
            # 散点图
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("创建散点图")
        elif action_object_name == "options":
            # 设置选项
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("打开设置")
            from src.axaltyx_gui.dialogs.settings_dialog import SettingsDialog
            dialog = SettingsDialog(self.parent())
            if hasattr(self.parent(), '_on_settings_changed'):
                dialog.sig_settings_changed.connect(self.parent()._on_settings_changed)
            dialog.exec()
        elif action_object_name == "help":
            # 帮助
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("打开帮助")
            from src.axaltyx_gui.dialogs.help_dialog import HelpDialog
            dialog = HelpDialog(self.parent())
            dialog.exec()
