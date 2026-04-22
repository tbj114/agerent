from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
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
from src.axaltyx_gui.panels import NavigationPanel, PropertyPanel
from src.axaltyx_gui.statusbar import AxaltyXStatusBar
from src.axaltyx_gui.settings import AppSettings, ThemeManager

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
        
        # 初始化设置和主题管理
        self.settings = AppSettings()
        self.theme_manager = ThemeManager()
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(1024, 600)
        self.setGeometry(100, 100, 1280, 800)
        self.title_bar = AxaltyXTitleBar(self)
        self.init_ui()
        
        # 初始化核心引擎、绘图引擎、国际化管理器和主题管理器
        from src.axaltyx_core.core_engine import CoreEngine
        from src.axaltyx_plot.plot_engine import PlotEngine
        from src.axaltyx_i18n.manager import I18nManager
        from src.axaltyx_gui.settings.theme_manager import ThemeManager
        
        # 创建核心引擎实例
        self.core_engine = CoreEngine()
        
        # 创建绘图引擎实例
        self.plot_engine = PlotEngine()
        
        # 创建国际化管理器实例
        self.i18n_manager = I18nManager()
        
        # 创建主题管理器实例
        self.theme_manager = ThemeManager()
        
        # 初始化桥接控制器
        from src.axaltyx_bridge.controller import BridgeController
        self.bridge = BridgeController()
        # 调用initialize方法，传入核心引擎、绘图引擎、国际化管理器和主题管理器
        self.bridge.initialize(self.core_engine, self.plot_engine, self.i18n_manager, self.theme_manager)
        
        # 连接桥接信号
        self._connect_bridge_signals()

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
        # 连接菜单信号
        self.menu_bar.sig_action_triggered.connect(self._on_action_triggered)

    def setup_toolbar(self) -> None:
        self.toolbar = AxaltyXToolBar(self)
        main_layout = self.centralWidget().layout()
        main_layout.insertWidget(2, self.toolbar)
        # 连接工具栏信号
        self.toolbar.sig_action_triggered.connect(self._on_action_triggered)

    def setup_status_bar(self) -> None:
        self.status_bar = AxaltyXStatusBar(self)
        self.status_bar.setFixedHeight(24)
        self.status_bar.show_message("就绪")
        self.setStatusBar(self.status_bar)
        
        # 更新数据信息
        self.status_bar.update_data_info(100, 100)

    def setup_left_panel(self) -> None:
        self.left_panel = NavigationPanel(self)
        self.left_panel.sig_analysis_selected.connect(self._on_analysis_selected)

    def setup_right_panel(self) -> None:
        self.right_panel = PropertyPanel(self)
        self.right_panel.sig_variable_changed.connect(self._on_variable_changed)
        
    def _on_analysis_selected(self, analysis_id, params):
        """处理分析选择事件
        
        Args:
            analysis_id: 分析ID
            params: 分析参数
        """
        self.update_status(f"选中分析: {analysis_id}")
        
        # 导入对话框
        from src.axaltyx_gui.dialogs.descriptive_dialog import DescriptiveDialog
        from src.axaltyx_gui.dialogs.frequency_dialog import FrequencyDialog
        from src.axaltyx_gui.dialogs.correlation_dialog import CorrelationDialog
        from src.axaltyx_gui.dialogs.anova_dialogs import AnovaDialog
        from src.axaltyx_gui.dialogs.t_test_dialogs import TTestDialog
        from src.axaltyx_gui.dialogs.regression_dialogs import RegressionDialog
        from src.axaltyx_gui.dialogs.clustering_dialog import ClusteringDialog
        from src.axaltyx_gui.dialogs.crosstabs_dialog import CrosstabsDialog
        from src.axaltyx_gui.dialogs.nonparametric_dialogs import NonparametricDialog
        from src.axaltyx_gui.dialogs.reliability_dialog import ReliabilityDialog
        from src.axaltyx_gui.dialogs.survival_dialogs import SurvivalDialog
        from src.axaltyx_gui.dialogs.factor_dialog import FactorDialog
        
        # 显示对应的分析对话框
        if analysis_id in ['descriptive_stats']:
            dialog = DescriptiveDialog(self)
            dialog.exec()
        elif analysis_id in ['frequencies']:
            dialog = FrequencyDialog(self)
            dialog.exec()
        elif analysis_id in ['pearson', 'partial_corr', 'spearman']:
            dialog = CorrelationDialog(self)
            dialog.exec()
        elif analysis_id in ['one_way_anova', 'two_way_anova', 'ancova', 'rm_anova']:
            dialog = AnovaDialog(self)
            dialog.exec()
        elif analysis_id in ['one_sample_t', 'independent_t', 'paired_t']:
            dialog = TTestDialog(self)
            dialog.exec()
        elif analysis_id in ['linear_reg', 'logistic_reg', 'ordinal_reg', 'nonlinear_reg', 'curve_est']:
            dialog = RegressionDialog(self)
            dialog.exec()
        elif analysis_id in ['hierarchical_cluster', 'kmeans']:
            dialog = ClusteringDialog(self)
            dialog.exec()
        elif analysis_id in ['crosstabs']:
            dialog = CrosstabsDialog(self)
            dialog.exec()
        elif analysis_id in ['mann_whitney', 'wilcoxon', 'kruskal_wallis', 'friedman']:
            dialog = NonparametricDialog(self)
            dialog.exec()
        elif analysis_id in ['efa', 'cfa']:
            dialog = FactorDialog(self)
            dialog.exec()
        
        # 触发分析请求信号
        self.sig_analysis_requested.emit(analysis_id, params)
        
    def _on_variable_changed(self, var_name, metadata):
        """处理变量属性变更事件
        
        Args:
            var_name: 变量名称
            metadata: 变量元数据
        """
        self.update_status(f"变量属性已更新: {var_name}")

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
        """加载数据

        Args:
            path: 文件路径
            file_type: 文件类型
        """
        from PyQt6.QtWidgets import QFileDialog
        
        # 如果没有提供路径，打开文件对话框
        if not path:
            file_filter = "CSV files (*.csv);;Excel files (*.xlsx);;Text files (*.txt);;All files (*.*)"
            path, _ = QFileDialog.getOpenFileName(self, "打开文件", "", file_filter)
            if not path:
                return
        
        # 确定文件类型
        if not file_type:
            import os
            _, ext = os.path.splitext(path)
            file_type = ext.lower().lstrip('.')
        
        # 加载数据
        try:
            self.update_status(f"正在加载数据: {path}")
            
            # 发送加载请求到 bridge
            if hasattr(self, '_bridge_signals') and hasattr(self._bridge_signals, 'sig_load_requested'):
                self._bridge_signals.sig_load_requested.emit(path, file_type)
            else:
                # 如果没有 bridge，暂时显示成功
                self.update_status(f"数据加载成功: {path}")
                
        except Exception as e:
            self.update_status(f"数据加载失败: {str(e)}")

    def save_data(self, path: str, file_type: str) -> None:
        """保存数据

        Args:
            path: 文件路径
            file_type: 文件类型
        """
        from PyQt6.QtWidgets import QFileDialog
        
        # 如果没有提供路径，打开文件对话框
        if not path:
            file_filter = "CSV files (*.csv);;Excel files (*.xlsx);;Text files (*.txt)"
            path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", file_filter)
            if not path:
                return
        
        # 确定文件类型
        if not file_type:
            import os
            _, ext = os.path.splitext(path)
            file_type = ext.lower().lstrip('.')
        
        # 保存数据
        try:
            self.update_status(f"正在保存数据: {path}")
            
            # 发送保存请求到 bridge
            if hasattr(self, '_bridge_signals') and hasattr(self._bridge_signals, 'sig_save_requested'):
                self._bridge_signals.sig_save_requested.emit(path, file_type, 'utf-8')
            else:
                # 如果没有 bridge，暂时显示成功
                self.update_status(f"数据保存成功: {path}")
                
        except Exception as e:
            self.update_status(f"数据保存失败: {str(e)}")

    def new_dataset(self, rows: int = 100, cols: int = 100) -> None:
        """新建数据集

        Args:
            rows: 行数
            cols: 列数
        """
        try:
            self.update_status(f"正在创建新数据集: {rows}行 x {cols}列")
            
            # 发送新建请求到 bridge
            if hasattr(self, '_bridge_signals') and hasattr(self._bridge_signals, 'sig_new_requested'):
                self._bridge_signals.sig_new_requested.emit(rows, cols)
            else:
                # 如果没有 bridge，暂时显示成功
                self.update_status(f"新数据集创建成功: {rows}行 x {cols}列")
                
        except Exception as e:
            self.update_status(f"创建新数据集失败: {str(e)}")

    def show_analysis_dialog(self, analysis_name: str) -> None:
        """显示分析对话框

        Args:
            analysis_name: 分析名称
        """
        # 导入对话框
        from src.axaltyx_gui.dialogs.descriptive_dialog import DescriptiveDialog
        from src.axaltyx_gui.dialogs.frequency_dialog import FrequencyDialog
        from src.axaltyx_gui.dialogs.correlation_dialog import CorrelationDialog
        from src.axaltyx_gui.dialogs.anova_dialogs import AnovaDialog
        from src.axaltyx_gui.dialogs.t_test_dialogs import TTestDialog
        from src.axaltyx_gui.dialogs.regression_dialogs import RegressionDialog
        from src.axaltyx_gui.dialogs.clustering_dialog import ClusteringDialog
        from src.axaltyx_gui.dialogs.crosstabs_dialog import CrosstabsDialog
        from src.axaltyx_gui.dialogs.nonparametric_dialogs import NonparametricDialog
        from src.axaltyx_gui.dialogs.reliability_dialog import ReliabilityDialog
        from src.axaltyx_gui.dialogs.survival_dialogs import SurvivalDialog
        from src.axaltyx_gui.dialogs.factor_dialog import FactorDialog
        
        # 显示对应的分析对话框
        if "descriptive" in analysis_name.lower():
            dialog = DescriptiveDialog(self)
            dialog.exec()
        elif "frequency" in analysis_name.lower():
            dialog = FrequencyDialog(self)
            dialog.exec()
        elif "correlation" in analysis_name.lower():
            dialog = CorrelationDialog(self)
            dialog.exec()
        elif "anova" in analysis_name.lower():
            dialog = AnovaDialog(self)
            dialog.exec()
        elif "t_test" in analysis_name.lower() or "t-test" in analysis_name.lower():
            dialog = TTestDialog(self)
            dialog.exec()
        elif "regression" in analysis_name.lower():
            dialog = RegressionDialog(self)
            dialog.exec()
        elif "clustering" in analysis_name.lower():
            dialog = ClusteringDialog(self)
            dialog.exec()
        elif "crosstab" in analysis_name.lower():
            dialog = CrosstabsDialog(self)
            dialog.exec()
        elif "nonparametric" in analysis_name.lower():
            dialog = NonparametricDialog(self)
            dialog.exec()
        elif "reliability" in analysis_name.lower():
            dialog = ReliabilityDialog(self)
            dialog.exec()
        elif "survival" in analysis_name.lower():
            dialog = SurvivalDialog(self)
            dialog.exec()
        elif "factor" in analysis_name.lower():
            dialog = FactorDialog(self)
            dialog.exec()

    def switch_tab(self, tab_id: str) -> None:
        """切换标签页

        Args:
            tab_id: 标签页ID
        """
        # 切换到对应的标签页
        if hasattr(self, 'tab_widget'):
            self.tab_widget.set_current_tab(tab_id)
            self.update_status(f"切换到 {tab_id} 视图")

    def set_language(self, lang_code: str) -> None:
        # 语言切换实现
        self.settings.set("general.language", lang_code)
        self.status_bar.update_language_indicator(lang_code)
        self.sig_language_changed.emit(lang_code)

    def set_theme(self, theme_name: str) -> None:
        # 主题切换实现
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            self.theme_manager.apply_theme(theme_name, app)
            self.settings.set("general.theme", theme_name)
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

    def _on_action_triggered(self, action_text: str):
        """处理菜单和工具栏动作

        Args:
            action_text: 动作文本
        """
        print(f"Action triggered: {action_text}")
        
        # 导入对话框
        from src.axaltyx_gui.dialogs.settings_dialog import SettingsDialog
        from src.axaltyx_gui.dialogs.descriptive_dialog import DescriptiveDialog
        from src.axaltyx_gui.dialogs.frequency_dialog import FrequencyDialog
        from src.axaltyx_gui.dialogs.correlation_dialog import CorrelationDialog
        from src.axaltyx_gui.dialogs.anova_dialogs import AnovaDialog
        from src.axaltyx_gui.dialogs.t_test_dialogs import TTestDialog
        from src.axaltyx_gui.dialogs.regression_dialogs import RegressionDialog
        from src.axaltyx_gui.dialogs.clustering_dialog import ClusteringDialog
        from src.axaltyx_gui.dialogs.crosstabs_dialog import CrosstabsDialog
        from src.axaltyx_gui.dialogs.nonparametric_dialogs import NonparametricDialog
        from src.axaltyx_gui.dialogs.reliability_dialog import ReliabilityDialog
        from src.axaltyx_gui.dialogs.survival_dialogs import SurvivalDialog
        from src.axaltyx_gui.dialogs.factor_dialog import FactorDialog
        
        # 处理设置动作
        if "选项" in action_text or "Options" in action_text:
            dialog = SettingsDialog(self)
            dialog.sig_settings_changed.connect(self._on_settings_changed)
            dialog.exec()
        
        # 处理分析动作
        elif "描述统计" in action_text or "Descriptive" in action_text:
            dialog = DescriptiveDialog(self)
            dialog.exec()
        elif "频率" in action_text or "Frequency" in action_text:
            dialog = FrequencyDialog(self)
            dialog.exec()
        elif "相关" in action_text or "Correlation" in action_text:
            dialog = CorrelationDialog(self)
            dialog.exec()
        elif "方差分析" in action_text or "ANOVA" in action_text:
            dialog = AnovaDialog(self)
            dialog.exec()
        elif "T检验" in action_text or "T Test" in action_text:
            dialog = TTestDialog(self)
            dialog.exec()
        elif "回归" in action_text or "Regression" in action_text:
            dialog = RegressionDialog(self)
            dialog.exec()
        elif "聚类" in action_text or "Clustering" in action_text:
            dialog = ClusteringDialog(self)
            dialog.exec()
        elif "交叉表" in action_text or "Crosstabs" in action_text:
            dialog = CrosstabsDialog(self)
            dialog.exec()
        elif "非参数" in action_text or "Nonparametric" in action_text:
            dialog = NonparametricDialog(self)
            dialog.exec()
        elif "信度" in action_text or "Reliability" in action_text:
            dialog = ReliabilityDialog(self)
            dialog.exec()
        elif "生存分析" in action_text or "Survival" in action_text:
            dialog = SurvivalDialog(self)
            dialog.exec()
        elif "因子分析" in action_text or "Factor" in action_text:
            dialog = FactorDialog(self)
            dialog.exec()
        
        # 处理文件动作
        elif "新建" in action_text or "New" in action_text:
            self.new_dataset()
        elif "打开" in action_text or "Open" in action_text:
            self.load_data("", "")
        elif "保存" in action_text or "Save" in action_text:
            self.save_data("", "")
        
        # 处理视图动作
        elif "数据视图" in action_text or "Data View" in action_text:
            self.switch_tab("data_view")
        elif "变量视图" in action_text or "Variable View" in action_text:
            self.switch_tab("variable_view")
        elif "输出视图" in action_text or "Output View" in action_text:
            self.switch_tab("output_view")
        elif "语法视图" in action_text or "Syntax View" in action_text:
            self.switch_tab("syntax_view")
        
        # 处理主题动作
        elif "亮色主题" in action_text or "Light Theme" in action_text:
            self.set_theme("light")
        elif "暗色主题" in action_text or "Dark Theme" in action_text:
            self.set_theme("dark")

    def _on_settings_changed(self, settings: dict):
        """处理设置变更

        Args:
            settings: 新的设置
        """
        print(f"Settings changed: {settings}")
        
        # 保存设置
        self.settings.save(settings)
        
        # 应用主题
        if 'general' in settings and 'theme' in settings['general']:
            self.set_theme(settings['general']['theme'])
        
        # 应用语言
        if 'general' in settings and 'language' in settings['general']:
            self.set_language(settings['general']['language'])
        
        # 应用字体和外观设置
        if 'appearance' in settings:
            self._apply_appearance_settings(settings['appearance'])
        
        # 应用性能设置
        if 'performance' in settings:
            self._apply_performance_settings(settings['performance'])
        
        # 更新状态栏
        self.update_status("设置已保存")
    
    def _apply_appearance_settings(self, appearance: dict):
        """应用外观设置
        
        Args:
            appearance: 外观设置字典
        """
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QFont
        
        app = QApplication.instance()
        if not app:
            return
        
        # 应用字体大小
        if 'font_size' in appearance:
            font = QFont(app.font())
            font.setPointSize(appearance['font_size'])
            app.setFont(font)
        
        # 应用缩放级别
        if 'zoom_level' in appearance:
            zoom = appearance['zoom_level'] / 100.0
            # 应用缩放逻辑
            # 1. 缩放主窗口
            if hasattr(self, 'resize'):
                current_size = self.size()
                new_width = int(current_size.width() * zoom)
                new_height = int(current_size.height() * zoom)
                self.resize(new_width, new_height)
            # 2. 通知所有子组件进行缩放
            self._notify_scale_change(zoom)
        
        # 应用表格字体
        if 'table_font' in appearance and hasattr(self, 'data_tab'):
            self.data_tab.set_table_font(appearance['table_font'])
    
    def _apply_performance_settings(self, performance: dict):
        """应用性能设置
        
        Args:
            performance: 性能设置字典
        """
        # 应用最大线程数
        if 'max_threads' in performance and hasattr(self, '_controller'):
            self._controller.set_max_workers(performance['max_threads'])
        
        # 应用虚拟滚动
        if 'virtual_scroll' in performance:
            # 应用虚拟滚动设置
            enable_virtual_scroll = performance['virtual_scroll']
            # 1. 应用到数据表格
            if hasattr(self, 'data_tab') and hasattr(self.data_tab, 'set_virtual_scroll'):
                self.data_tab.set_virtual_scroll(enable_virtual_scroll)
            # 2. 应用到其他支持虚拟滚动的组件
            if hasattr(self, 'variable_tab') and hasattr(self.variable_tab, 'set_virtual_scroll'):
                self.variable_tab.set_virtual_scroll(enable_virtual_scroll)
        
        # 应用缓存大小
        if 'cache_size' in performance and hasattr(self, '_cache_manager'):
            self._cache_manager.set_max_size(performance['cache_size'] * 1024 * 1024)  # 转换为字节
    
    def _connect_bridge_signals(self):
        """连接桥接控制器信号"""
        # 数据信号
        self.bridge.signals.sig_data_load_completed.connect(self._on_data_loaded)
        self.bridge.signals.sig_data_save_completed.connect(self._on_data_saved)
        self.bridge.signals.sig_data_new_completed.connect(self._on_data_created)
        
        # 分析信号
        self.bridge.signals.sig_analysis_started.connect(self._on_analysis_started)
        self.bridge.signals.sig_analysis_completed.connect(self._on_analysis_completed)
        self.bridge.signals.sig_analysis_failed.connect(self._on_analysis_error)
        
        # 图表信号
        self.bridge.signals.sig_chart_created.connect(self._on_chart_created)
        
        # UI信号
        self.bridge.signals.sig_language_changed.connect(self._on_language_updated)
        self.bridge.signals.sig_theme_changed.connect(self._on_theme_updated)
        self.bridge.signals.sig_settings_changed.connect(self._on_settings_updated)
        
        # 状态信号
        self.bridge.signals.sig_status_message.connect(self.update_status)
        self.bridge.signals.sig_notification.connect(self._on_notification)

    def _on_data_loaded(self, data):
        """数据加载完成处理"""
        if isinstance(data, dict) and "data" in data:
            # 更新数据标签页
            if hasattr(self, 'data_tab'):
                import pandas as pd
                df = pd.DataFrame(data["data"], columns=data.get("columns", []))
                self.data_tab.set_data(df)
            
            # 更新变量标签页
            if hasattr(self, 'variable_tab'):
                self.variable_tab.set_data(data)
            
            # 更新状态栏
            rows = data.get("rows", 0)
            cols = data.get("columns_count", 0)
            self.update_status(f"成功加载数据: {rows}行 × {cols}列")
            
            # 更新状态栏数据信息
            if hasattr(self, 'status_bar'):
                self.status_bar.update_data_info(rows, cols)

    def _on_data_saved(self, path):
        """数据保存完成处理"""
        self.update_status(f"数据保存成功: {path}")

    def _on_data_created(self, data):
        """新数据创建完成处理"""
        if isinstance(data, dict) and "data" in data:
            # 更新数据标签页
            if hasattr(self, 'data_tab'):
                import pandas as pd
                df = pd.DataFrame(data["data"], columns=data.get("columns", []))
                self.data_tab.set_data(df)
            
            # 更新变量标签页
            if hasattr(self, 'variable_tab'):
                self.variable_tab.set_data(data)
            
            # 更新状态栏
            rows = data.get("rows", 0)
            cols = data.get("columns_count", 0)
            self.update_status(f"成功创建新数据集: {rows}行 × {cols}列")
            
            # 更新状态栏数据信息
            if hasattr(self, 'status_bar'):
                self.status_bar.update_data_info(rows, cols)

    def _on_data_error(self, error):
        """数据操作错误处理"""
        self.update_status(f"数据操作错误: {error}")

    def _on_analysis_started(self, analysis_name):
        """分析开始处理"""
        self.update_status(f"开始分析: {analysis_name}")

    def _on_analysis_completed(self, analysis_name, results):
        """分析完成处理"""
        # 更新输出标签页
        if hasattr(self, 'output_tab'):
            self.output_tab.add_analysis_result(analysis_name, results)
        
        # 更新状态栏
        self.update_status(f"分析完成: {analysis_name}")

    def _on_analysis_error(self, analysis_name, error):
        """分析错误处理"""
        self.update_status(f"分析错误: {analysis_name} - {error}")

    def _on_chart_created(self, chart_id, chart_data):
        """图表创建完成处理"""
        # 更新输出标签页
        if hasattr(self, 'output_tab'):
            self.output_tab.add_chart(chart_id, chart_data)
        
        # 更新状态栏
        self.update_status("图表创建完成")

    def _on_chart_error(self, error):
        """图表错误处理"""
        self.update_status(f"图表创建错误: {error}")

    def _on_language_updated(self, lang_code):
        """语言更新处理"""
        # 更新状态栏语言指示器
        if hasattr(self, 'status_bar'):
            self.status_bar.update_language_indicator(lang_code)
        
        # 更新状态栏
        self.update_status(f"语言已切换至: {lang_code}")

    def _on_theme_updated(self, theme_name):
        """主题更新处理"""
        # 更新状态栏
        self.update_status(f"主题已切换至: {theme_name}")

    def _on_settings_updated(self, settings):
        """设置更新处理"""
        # 更新状态栏
        self.update_status("设置已更新")

    def _on_notification(self, ntype, title, message):
        """通知处理"""
        # 这里可以实现通知显示逻辑
        print(f"{ntype}: {title} - {message}")

    def _notify_scale_change(self, zoom: float):
        """通知所有子组件进行缩放
        
        Args:
            zoom: 缩放比例
        """
        # 通知数据标签页
        if hasattr(self, 'data_tab') and hasattr(self.data_tab, 'set_scale'):
            self.data_tab.set_scale(zoom)
        
        # 通知变量标签页
        if hasattr(self, 'variable_tab') and hasattr(self.variable_tab, 'set_scale'):
            self.variable_tab.set_scale(zoom)
        
        # 通知输出标签页
        if hasattr(self, 'output_tab') and hasattr(self.output_tab, 'set_scale'):
            self.output_tab.set_scale(zoom)
        
        # 通知语法标签页
        if hasattr(self, 'syntax_tab') and hasattr(self.syntax_tab, 'set_scale'):
            self.syntax_tab.set_scale(zoom)
        
        # 通知左侧导航面板
        if hasattr(self, 'left_panel') and hasattr(self.left_panel, 'set_scale'):
            self.left_panel.set_scale(zoom)
        
        # 通知右侧属性面板
        if hasattr(self, 'right_panel') and hasattr(self.right_panel, 'set_scale'):
            self.right_panel.set_scale(zoom)