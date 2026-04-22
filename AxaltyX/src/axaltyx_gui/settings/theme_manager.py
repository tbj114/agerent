from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtCore import Qt


class ThemeManager:
    """主题管理"""

    def __init__(self):
        """初始化主题管理器"""
        self._themes = {
            "light": self._get_light_theme_stylesheet(),
            "dark": self._get_dark_theme_stylesheet()
        }
        self._current_theme = "light"

    def apply_theme(self, theme_name: str, app: QApplication) -> None:
        """应用主题

        Args:
            theme_name: 主题名称
            app: QApplication实例
        """
        if theme_name not in self._themes:
            theme_name = "light"
        
        self._current_theme = theme_name
        stylesheet = self.get_stylesheet(theme_name)
        app.setStyleSheet(stylesheet)
        
        # 设置应用级别的调色板
        palette = QPalette()
        if theme_name == "dark":
            # 暗色主题调色板
            palette.setColor(QPalette.ColorRole.Window, QColor(23, 23, 26))  # #17171A
            palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255, 217))  # #FFFFFFD9
            palette.setColor(QPalette.ColorRole.Base, QColor(29, 29, 32))  # #1D1D20
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(38, 38, 41))  # #262629
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(23, 23, 26))  # #17171A
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255, 217))  # #FFFFFFD9
            palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255, 217))  # #FFFFFFD9
            palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))  # #2D2D2D
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255, 217))  # #FFFFFFD9
            palette.setColor(QPalette.ColorRole.Highlight, QColor(48, 128, 255))  # #3080FF
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))  # #FFFFFF
            palette.setColor(QPalette.ColorRole.Link, QColor(48, 128, 255))  # #3080FF
            palette.setColor(QPalette.ColorRole.LinkVisited, QColor(48, 128, 255))  # #3080FF
            palette.setColor(QPalette.ColorRole.Disabled, QPalette.ColorRole.Text, QColor(255, 255, 255, 92))  # #FFFFFF5C
            palette.setColor(QPalette.ColorRole.Disabled, QPalette.ColorRole.ButtonText, QColor(255, 255, 255, 92))  # #FFFFFF5C
        else:
            # 亮色主题调色板
            palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))  # #FFFFFF
            palette.setColor(QPalette.ColorRole.WindowText, QColor(29, 33, 41))  # #1D2129
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))  # #FFFFFF
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(247, 248, 250))  # #F7F8FA
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))  # #FFFFFF
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(29, 33, 41))  # #1D2129
            palette.setColor(QPalette.ColorRole.Text, QColor(29, 33, 41))  # #1D2129
            palette.setColor(QPalette.ColorRole.Button, QColor(247, 248, 250))  # #F7F8FA
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(29, 33, 41))  # #1D2129
            palette.setColor(QPalette.ColorRole.Highlight, QColor(22, 93, 255))  # #165DFF
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))  # #FFFFFF
            palette.setColor(QPalette.ColorRole.Link, QColor(22, 93, 255))  # #165DFF
            palette.setColor(QPalette.ColorRole.LinkVisited, QColor(22, 93, 255))  # #165DFF
            palette.setColor(QPalette.ColorRole.Disabled, QPalette.ColorRole.Text, QColor(201, 205, 212))  # #C9CDD4
            palette.setColor(QPalette.ColorRole.Disabled, QPalette.ColorRole.ButtonText, QColor(201, 205, 212))  # #C9CDD4
        
        app.setPalette(palette)

    def get_available_themes(self) -> list[str]:
        """获取可用主题

        Returns:
            list[str]: 可用主题列表
        """
        return list(self._themes.keys())

    def get_current_theme(self) -> str:
        """获取当前主题

        Returns:
            str: 当前主题
        """
        return self._current_theme

    def get_stylesheet(self, theme_name: str) -> str:
        """获取样式表

        Args:
            theme_name: 主题名称

        Returns:
            str: 样式表
        """
        return self._themes.get(theme_name, self._themes["light"])

    def register_theme(self, theme_name: str, stylesheet: str) -> None:
        """注册主题

        Args:
            theme_name: 主题名称
            stylesheet: 样式表
        """
        self._themes[theme_name] = stylesheet

    def _get_light_theme_stylesheet(self) -> str:
        """获取亮色主题样式表

        Returns:
            str: 亮色主题样式表
        """
        return """
        /* 亮色主题样式表 */
        
        /* 全局样式 */
        QWidget {
            background-color: #FFFFFF;
            color: #1D2129;
            font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans SC", sans-serif;
            font-size: 14px;
        }
        
        /* 按钮样式 */
        QPushButton {
            background-color: #F7F8FA;
            border: 1px solid #E5E6EB;
            border-radius: 8px;
            padding: 6px 12px;
            color: #1D2129;
        }
        
        QPushButton:hover {
            background-color: #E8F3FF;
            border-color: #165DFF;
        }
        
        QPushButton:pressed {
            background-color: #E5E6EB;
        }
        
        QPushButton:disabled {
            background-color: #F2F3F5;
            color: #C9CDD4;
            border-color: #E5E6EB;
        }
        
        /* 输入框样式 */
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
            background-color: #FFFFFF;
            border: 1px solid #E5E6EB;
            border-radius: 8px;
            padding: 6px 12px;
            color: #1D2129;
        }
        
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {
            border-color: #165DFF;
            outline: none;
            background-color: #FFFFFF;
        }
        
        /* 标签样式 */
        QLabel {
            color: #1D2129;
        }
        
        /* 表格样式 */
        QTableView, QTreeView, QListWidget {
            background-color: #FFFFFF;
            border: 1px solid #E5E6EB;
            border-radius: 4px;
        }
        
        QHeaderView::section {
            background-color: #F2F3F5;
            color: #1D2129;
            padding: 6px;
            border: 1px solid #E5E6EB;
            font-weight: bold;
        }
        
        QTableView::item {
            padding: 4px;
        }
        
        QTableView::item:selected {
            background-color: #E8F3FF;
            color: #165DFF;
        }
        
        /* 分组框样式 */
        QGroupBox {
            border: 1px solid #E5E6EB;
            border-radius: 8px;
            margin-top: 24px;
            padding: 16px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 16px;
            top: -12px;
            background-color: #FFFFFF;
            padding: 0 8px;
            color: #1D2129;
            font-weight: bold;
        }
        
        /* 滚动条样式 */
        QScrollBar:vertical {
            background: #F2F3F5;
            width: 10px;
            margin: 0px;
            border-radius: 5px;
        }
        
        QScrollBar:horizontal {
            background: #F2F3F5;
            height: 10px;
            margin: 0px;
            border-radius: 5px;
        }
        
        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
            background: #C9CDD4;
            border-radius: 5px;
        }
        
        QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
            background: #86909C;
        }
        
        /* 状态栏样式 */
        QStatusBar {
            background-color: #F7F8FA;
            border-top: 1px solid #E5E6EB;
            color: #4E5969;
        }
        
        /* 菜单样式 */
        QMenuBar {
            background-color: #F7F8FA;
            border-bottom: 1px solid #E5E6EB;
        }
        
        QMenuBar::item {
            padding: 8px 16px;
            color: #1D2129;
        }
        
        QMenuBar::item:selected {
            background-color: #E8F3FF;
            color: #165DFF;
        }
        
        QMenu {
            background-color: #FFFFFF;
            border: 1px solid #E5E6EB;
            border-radius: 8px;
            padding: 4px 0;
        }
        
        QMenu::item {
            padding: 6px 24px;
            color: #1D2129;
        }
        
        QMenu::item:selected {
            background-color: #E8F3FF;
            color: #165DFF;
        }
        """

    def _get_dark_theme_stylesheet(self) -> str:
        """获取暗色主题样式表

        Returns:
            str: 暗色主题样式表
        """
        return """
        /* 暗色主题样式表 */
        
        /* 全局样式 */
        QWidget {
            background-color: #17171A;
            color: #FFFFFFD9;
            font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans SC", sans-serif;
            font-size: 14px;
        }
        
        /* 按钮样式 */
        QPushButton {
            background-color: #262629;
            border: 1px solid #3D3D3D;
            border-radius: 8px;
            padding: 6px 12px;
            color: #FFFFFFD9;
        }
        
        QPushButton:hover {
            background-color: #1A2332;
            border-color: #3080FF;
        }
        
        QPushButton:pressed {
            background-color: #3D3D3D;
        }
        
        QPushButton:disabled {
            background-color: #262629;
            color: #FFFFFF5C;
            border-color: #3D3D3D;
        }
        
        /* 输入框样式 */
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
            background-color: #1D1D20;
            border: 1px solid #3D3D3D;
            border-radius: 8px;
            padding: 6px 12px;
            color: #FFFFFFD9;
        }
        
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {
            border-color: #3080FF;
            outline: none;
            background-color: #1D1D20;
        }
        
        /* 标签样式 */
        QLabel {
            color: #FFFFFFD9;
        }
        
        /* 表格样式 */
        QTableView, QTreeView, QListWidget {
            background-color: #1D1D20;
            border: 1px solid #3D3D3D;
            border-radius: 4px;
        }
        
        QHeaderView::section {
            background-color: #262629;
            color: #FFFFFFD9;
            padding: 6px;
            border: 1px solid #3D3D3D;
            font-weight: bold;
        }
        
        QTableView::item {
            padding: 4px;
        }
        
        QTableView::item:selected {
            background-color: #1A2332;
            color: #3080FF;
        }
        
        /* 分组框样式 */
        QGroupBox {
            border: 1px solid #3D3D3D;
            border-radius: 8px;
            margin-top: 24px;
            padding: 16px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 16px;
            top: -12px;
            background-color: #17171A;
            padding: 0 8px;
            color: #FFFFFFD9;
            font-weight: bold;
        }
        
        /* 滚动条样式 */
        QScrollBar:vertical {
            background: #262629;
            width: 10px;
            margin: 0px;
            border-radius: 5px;
        }
        
        QScrollBar:horizontal {
            background: #262629;
            height: 10px;
            margin: 0px;
            border-radius: 5px;
        }
        
        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
            background: #4E5969;
            border-radius: 5px;
        }
        
        QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
            background: #86909C;
        }
        
        /* 状态栏样式 */
        QStatusBar {
            background-color: #1D1D20;
            border-top: 1px solid #3D3D3D;
            color: #FFFFFF8C;
        }
        
        /* 菜单样式 */
        QMenuBar {
            background-color: #1D1D20;
            border-bottom: 1px solid #3D3D3D;
        }
        
        QMenuBar::item {
            padding: 8px 16px;
            color: #FFFFFFD9;
        }
        
        QMenuBar::item:selected {
            background-color: #1A2332;
            color: #3080FF;
        }
        
        QMenu {
            background-color: #1D1D20;
            border: 1px solid #3D3D3D;
            border-radius: 8px;
            padding: 4px 0;
        }
        
        QMenu::item {
            padding: 6px 24px;
            color: #FFFFFFD9;
        }
        
        QMenu::item:selected {
            background-color: #1A2332;
            color: #3080FF;
        }
        """
