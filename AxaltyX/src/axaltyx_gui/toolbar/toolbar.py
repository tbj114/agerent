from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QAction, QIcon, QPixmap
from src.axaltyx_i18n.manager import I18nManager

class AxaltyXToolBar(QToolBar):
    """自定义工具栏"""

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
        print(f"Tool action triggered: {action.toolTip()}")
        # 这里可以添加具体的工具处理逻辑
