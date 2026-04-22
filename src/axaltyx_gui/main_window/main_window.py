from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QMenuBar, QStatusBar, QMenu
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import pyqtSignal, Qt
from .title_bar import AxaltyXTitleBar

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

        # 添加菜单栏
        self.setup_menu_bar()
        main_layout.addWidget(self.menu_bar)

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
        self.menu_bar = QMenuBar()
        self.menu_bar.setFixedHeight(28)
        
        # 创建菜单项
        menu_names = ["文件(F)", "编辑(E)", "视图(V)", "数据(D)", "分析(A)", "图形(G)", "工具(T)", "帮助(H)"]
        
        for name in menu_names:
            menu = QMenu(name, self)
            self.menu_bar.addMenu(menu)

    def setup_toolbar(self) -> None:
        """设置工具栏"""
        from src.axaltyx_gui.toolbar.toolbar import AxaltyXToolBar
        self.toolbar = AxaltyXToolBar(self)
        self.addToolBar(self.toolbar)
        
        # 连接工具栏信号
        self.toolbar.sig_action_triggered.connect(self._on_action_triggered)

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
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #F7F8FA;")

    def load_data(self, path: str, file_type: str) -> None:
        """加载数据

        Args:
            path: 文件路径
            file_type: 文件类型
        """
        try:
            # 实际的数据加载逻辑
            import pandas as pd
            import os
            
            # 确保文件存在
            if not os.path.exists(path):
                raise FileNotFoundError(f"文件不存在: {path}")
            
            # 根据文件类型读取数据
            if file_type == "csv":
                data = pd.read_csv(path)
            elif file_type == "excel" or file_type == "xlsx" or file_type == "xls":
                data = pd.read_excel(path)
            elif file_type == "json":
                data = pd.read_json(path)
            elif file_type == "txt":
                data = pd.read_csv(path, delimiter='\t')
            else:
                raise ValueError(f"不支持的文件类型: {file_type}")
            
            # 转换数据为字典格式
            data_dict = {
                "data": data.to_dict('records'),
                "columns": list(data.columns),
                "path": path,
                "file_type": file_type,
                "rows": len(data),
                "columns_count": len(data.columns)
            }
            
            # 更新数据标签页
            if hasattr(self, 'data_tab'):
                self.data_tab.set_data(data)
            
            # 更新变量标签页
            if hasattr(self, 'variable_tab'):
                self.variable_tab.set_data(data)
            
            # 发出数据加载完成信号
            self.sig_data_loaded.emit(data_dict)
            
            # 更新状态栏
            self.update_status(f"成功加载数据文件: {path} ({len(data)}行 × {len(data.columns)}列)")
            
            # 更新状态栏数据信息
            if hasattr(self, 'status_bar'):
                self.status_bar.update_data_info(len(data), len(data.columns))
            
        except Exception as e:
            # 处理异常
            error_message = f"加载数据失败: {str(e)}"
            print(error_message)
            self.update_status(error_message)
            
            # 发出错误信号
            self.sig_data_loaded.emit({"error": error_message})

    def save_data(self, path: str, file_type: str) -> None:
        """保存数据

        Args:
            path: 文件路径
            file_type: 文件类型
        """
        try:
            # 获取当前数据
            current_data = self.get_current_data()
            
            if current_data is None:
                # 尝试从数据标签页获取数据
                if hasattr(self, 'data_tab'):
                    current_data = self.data_tab.get_data()
                else:
                    raise ValueError("没有数据可保存")
            
            # 实际的数据保存逻辑
            import pandas as pd
            import os
            
            # 确保目录存在
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # 处理数据格式
            if isinstance(current_data, pd.DataFrame):
                data = current_data
            elif isinstance(current_data, dict) and "data" in current_data and "columns" in current_data:
                data = pd.DataFrame(current_data["data"], columns=current_data["columns"])
            else:
                raise ValueError("数据格式不正确")
            
            # 根据文件类型保存数据
            if file_type == "csv":
                data.to_csv(path, index=False, encoding='utf-8-sig')
            elif file_type == "excel" or file_type == "xlsx":
                data.to_excel(path, index=False)
            elif file_type == "json":
                data.to_json(path, orient='records', force_ascii=False)
            elif file_type == "txt":
                data.to_csv(path, sep='\t', index=False, encoding='utf-8-sig')
            else:
                raise ValueError(f"不支持的文件类型: {file_type}")
            
            # 更新状态栏
            self.update_status(f"成功保存数据文件: {path} ({len(data)}行 × {len(data.columns)}列)")
            
        except Exception as e:
            # 处理异常
            error_message = f"保存数据失败: {str(e)}"
            print(error_message)
            self.update_status(error_message)

    def new_dataset(self, rows: int = 100, cols: int = 100) -> None:
        """新建数据集

        Args:
            rows: 行数
            cols: 列数
        """
        try:
            # 生成新的数据集
            import pandas as pd
            import numpy as np
            
            # 创建列名
            columns = [f"Var{i+1}" for i in range(cols)]
            
            # 创建随机数据
            data = np.random.randn(rows, cols)
            df = pd.DataFrame(data, columns=columns)
            
            # 转换数据为字典格式
            data_dict = {
                "data": df.to_dict('records'),
                "columns": columns,
                "path": None,
                "file_type": "new"
            }
            
            # 发出数据加载完成信号
            self.sig_data_loaded.emit(data_dict)
            
            # 更新状态栏
            self.update_status(f"成功创建新数据集: {rows}行 x {cols}列")
            
        except Exception as e:
            # 处理异常
            error_message = f"创建新数据集失败: {str(e)}"
            print(error_message)
            self.update_status(error_message)
            
            # 发出空数据信号
            self.sig_data_loaded.emit({"error": error_message})

    def show_analysis_dialog(self, analysis_name: str) -> None:
        """显示分析对话框

        Args:
            analysis_name: 分析名称
        """
        try:
            # 实际的分析对话框显示逻辑
            print(f"显示分析对话框: {analysis_name}")
            
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
            dialog = None
            if "descriptive" in analysis_name.lower():
                dialog = DescriptiveDialog(self)
            elif "frequency" in analysis_name.lower():
                dialog = FrequencyDialog(self)
            elif "correlation" in analysis_name.lower():
                dialog = CorrelationDialog(self)
            elif "anova" in analysis_name.lower():
                dialog = AnovaDialog(self)
            elif "t_test" in analysis_name.lower() or "t-test" in analysis_name.lower():
                dialog = TTestDialog(self)
            elif "regression" in analysis_name.lower():
                dialog = RegressionDialog(self)
            elif "clustering" in analysis_name.lower():
                dialog = ClusteringDialog(self)
            elif "crosstab" in analysis_name.lower():
                dialog = CrosstabsDialog(self)
            elif "nonparametric" in analysis_name.lower():
                dialog = NonparametricDialog(self)
            elif "reliability" in analysis_name.lower():
                dialog = ReliabilityDialog(self)
            elif "survival" in analysis_name.lower():
                dialog = SurvivalDialog(self)
            elif "factor" in analysis_name.lower():
                dialog = FactorDialog(self)
            
            # 执行对话框
            if dialog:
                # 连接对话框信号
                dialog.sig_analysis_requested.connect(lambda name, params: self.sig_analysis_requested.emit(name, params))
                # 显示对话框
                dialog.exec()
            
            # 获取选中变量
            selected_vars = self.get_selected_variables()
            
            # 发出分析请求信号
            analysis_params = {
                "variables": selected_vars,
                "options": {}
            }
            self.sig_analysis_requested.emit(analysis_name, analysis_params)
            
            # 更新状态栏
            if selected_vars:
                self.update_status(f"准备进行{analysis_name}分析，选中变量: {', '.join(selected_vars[:3])}{'...' if len(selected_vars) > 3 else ''}")
            else:
                self.update_status(f"准备进行{analysis_name}分析")
            
        except Exception as e:
            # 处理异常
            error_message = f"显示分析对话框失败: {str(e)}"
            print(error_message)
            self.update_status(error_message)

    def switch_tab(self, tab_id: str) -> None:
        """切换标签页

        Args:
            tab_id: 标签页ID
        """
        try:
            # 实际的标签页切换逻辑
            print(f"切换到标签页: {tab_id}")
            
            # 检查是否有标签页组件
            if not hasattr(self, 'tab_widget'):
                raise AttributeError("标签页组件未初始化")
            
            # 切换到对应的标签页
            success = self.tab_widget.set_current_tab(tab_id)
            
            if success:
                # 获取标签页名称
                tab_name = self.tab_widget.get_tab_name(tab_id)
                if tab_name:
                    self.update_status(f"切换到{tab_name}视图")
                else:
                    self.update_status(f"切换到{tab_id}视图")
            else:
                # 标签页不存在
                raise ValueError(f"标签页ID不存在: {tab_id}")
            
        except Exception as e:
            # 处理异常
            error_message = f"切换标签页失败: {str(e)}"
            print(error_message)
            self.update_status(error_message)

    def set_language(self, lang_code: str) -> None:
        # 语言切换实现
        self.sig_language_changed.emit(lang_code)

    def set_theme(self, theme_name: str) -> None:
        # 主题切换实现
        self.sig_theme_changed.emit(theme_name)

    def _on_action_triggered(self, action_id: str) -> None:
        """处理动作触发

        Args:
            action_id: 动作ID
        """
        try:
            # 根据动作ID执行不同的操作
            print(f"动作触发: {action_id}")
            
            # 处理文件操作
            if action_id == "new":
                self.new_dataset()
            elif action_id == "open":
                # 打开文件对话框
                from PyQt6.QtWidgets import QFileDialog
                file_filter = "CSV files (*.csv);;Excel files (*.xlsx);;Text files (*.txt);;JSON files (*.json);;All files (*.*)"
                path, _ = QFileDialog.getOpenFileName(self, "打开文件", "", file_filter)
                if path:
                    import os
                    _, ext = os.path.splitext(path)
                    file_type = ext.lower().lstrip('.')
                    self.load_data(path, file_type)
            elif action_id == "save":
                # 保存文件对话框
                from PyQt6.QtWidgets import QFileDialog
                file_filter = "CSV files (*.csv);;Excel files (*.xlsx);;Text files (*.txt);;JSON files (*.json)"
                path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", file_filter)
                if path:
                    import os
                    _, ext = os.path.splitext(path)
                    file_type = ext.lower().lstrip('.')
                    if not file_type:
                        # 默认保存为CSV
                        path += ".csv"
                        file_type = "csv"
                    self.save_data(path, file_type)
            
            # 处理视图操作
            elif action_id == "data_view":
                self.switch_tab("data_view")
            elif action_id == "variable_view":
                self.switch_tab("variable_view")
            elif action_id == "output_view":
                self.switch_tab("output_view")
            elif action_id == "syntax_view":
                self.switch_tab("syntax_view")
            
            # 处理分析操作
            elif action_id == "descriptive":
                self.show_analysis_dialog("descriptive")
            elif action_id == "frequency":
                self.show_analysis_dialog("frequency")
            elif action_id == "correlation":
                self.show_analysis_dialog("correlation")
            
            # 处理工具操作
            elif action_id == "options":
                # 打开设置对话框
                from src.axaltyx_gui.dialogs.settings_dialog import SettingsDialog
                dialog = SettingsDialog(self)
                dialog.sig_settings_changed.connect(self._on_settings_changed)
                dialog.exec()
            
            # 处理帮助操作
            elif action_id == "help":
                # 打开帮助对话框
                from src.axaltyx_gui.dialogs.help_dialog import HelpDialog
                dialog = HelpDialog(self)
                dialog.exec()
            
            else:
                # 处理其他动作
                self.update_status(f"执行操作: {action_id}")
                
        except Exception as e:
            # 处理异常
            error_message = f"执行操作失败: {str(e)}"
            print(error_message)
            self.update_status(error_message)

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