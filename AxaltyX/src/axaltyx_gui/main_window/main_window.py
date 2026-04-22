from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QStatusBar
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import pyqtSignal, Qt
from .title_bar import AxaltyXTitleBar
from .menu_bar import AxaltyXMenuBar
from src.axaltyx_gui.toolbar.toolbar import AxaltyXToolBar
from src.axaltyx_gui.tab_system.tab_widget import AxaltyXTabWidget
from src.axaltyx_gui.tab_system.data_tab import DataTab
from src.axaltyx_gui.tab_system.variable_tab import VariableTab
from src.axaltyx_gui.tab_system.output_tab import OutputTab
from src.axaltyx_gui.tab_system.syntax_tab import SyntaxTab

class AxaltyXMainWindow(QMainWindow):
    """主窗口，承载所有子组件"""

    # 信号
    sig_data_loaded = pyqtSignal(dict)           # 数据加载完成
    sig_analysis_requested = pyqtSignal(str, dict) # 分析请求
    sig_language_changed = pyqtSignal(str)        # 语言切换
    sig_theme_changed = pyqtSignal(str)           # 主题切换

    def __init__(self, config: dict = None):
        super().__init__()
        self.config = config or {}
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(1024, 600)
        self.setGeometry(100, 100, 1280, 800)
        self.title_bar = AxaltyXTitleBar(self)
        self.init_ui()

    def init_ui(self) -> None:
        # 设置主窗口布局
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 添加自定义标题栏
        main_layout.addWidget(self.title_bar)

        # 主内容区域
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # 左侧导航面板
        self.setup_left_panel()
        content_layout.addWidget(self.left_panel)

        # 中央数据编辑区
        self.setup_central_widget()
        content_layout.addWidget(self.central_widget)

        # 右侧属性面板
        self.setup_right_panel()
        content_layout.addWidget(self.right_panel)

        main_layout.addWidget(content_widget, 1)

        # 添加状态栏
        self.setup_status_bar()

        self.setCentralWidget(central_widget)

        # 添加菜单栏和工具栏
        self.setup_menu_bar()
        self.setup_toolbar()

        # 连接标题栏信号
        self.title_bar.sig_minimize.connect(self.showMinimized)
        self.title_bar.sig_maximize.connect(self.toggle_maximize)
        self.title_bar.sig_close.connect(self.close)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def setup_menu_bar(self) -> None:
        self.menu_bar = AxaltyXMenuBar(self)
        main_layout = self.centralWidget().layout()
        main_layout.insertWidget(1, self.menu_bar)

    def setup_toolbar(self) -> None:
        self.toolbar = AxaltyXToolBar(self)
        main_layout = self.centralWidget().layout()
        main_layout.insertWidget(2, self.toolbar)

    def setup_status_bar(self) -> None:
        self.status_bar = QStatusBar()
        self.status_bar.setFixedHeight(24)
        self.status_bar.showMessage("就绪")
        self.setStatusBar(self.status_bar)

    def setup_left_panel(self) -> None:
        self.left_panel = QWidget()
        self.left_panel.setFixedWidth(200)
        self.left_panel.setStyleSheet("background-color: #FFFFFF; border-right: 1px solid #E5E6EB;")

    def setup_right_panel(self) -> None:
        self.right_panel = QWidget()
        self.right_panel.setFixedWidth(240)
        self.right_panel.setStyleSheet("background-color: #FFFFFF; border-left: 1px solid #E5E6EB;")

    def setup_central_widget(self) -> None:
        # 创建标签页系统
        self.tab_widget = AxaltyXTabWidget()
        
        # 创建数据视图标签页
        self.data_tab = DataTab()
        self.tab_widget.add_tab(self.data_tab, "data_view", "数据视图", closable=False)
        
        # 创建变量视图标签页
        self.variable_tab = VariableTab(self.data_tab.get_data())
        self.tab_widget.add_tab(self.variable_tab, "variable_view", "变量视图", closable=False)
        
        # 创建输出视图标签页
        self.output_tab = OutputTab()
        self.tab_widget.add_tab(self.output_tab, "output_view", "输出视图", closable=False)
        
        # 创建语法视图标签页
        self.syntax_tab = SyntaxTab()
        self.tab_widget.add_tab(self.syntax_tab, "syntax_view", "语法视图", closable=False)
        
        # 设置标签页切换信号
        self.tab_widget.sig_tab_changed.connect(self._on_tab_changed)
        
        # 设置中心组件
        self.central_widget = QWidget()
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tab_widget)
        self.central_widget.setStyleSheet("background-color: #F7F8FA;")

    def load_data(self, path: str, file_type: str) -> None:
        # 数据加载实现
        pass

    def save_data(self, path: str, file_type: str) -> None:
        # 数据保存实现
        pass

    def new_dataset(self, rows: int = 100, cols: int = 100) -> None:
        # 新建数据集实现
        pass

    def show_analysis_dialog(self, analysis_name: str) -> None:
        # 显示分析对话框实现
        pass

    def switch_tab(self, tab_id: str) -> None:
        # 切换标签页实现
        pass

    def set_language(self, lang_code: str) -> None:
        # 语言切换实现
        self.sig_language_changed.emit(lang_code)

    def set_theme(self, theme_name: str) -> None:
        # 主题切换实现
        self.sig_theme_changed.emit(theme_name)

    def closeEvent(self, event) -> None:
        # 关闭事件处理
        event.accept()

    def get_current_data(self):
        # 获取当前数据实现
        return None

    def get_selected_variables(self) -> list[str]:
        # 获取选中变量实现
        return []

    def update_status(self, message: str, timeout: int = 0) -> None:
        # 更新状态栏消息
        self.status_bar.showMessage(message, timeout)

    def _on_tab_changed(self, tab_id: str):
        """标签页切换处理

        Args:
            tab_id: 标签页ID
        """
        self.update_status(f"切换到 {tab_id} 视图")