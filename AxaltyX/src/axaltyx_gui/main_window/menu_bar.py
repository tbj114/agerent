from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import pyqtSignal
from src.axaltyx_i18n.manager import I18nManager

class AxaltyXMenuBar(QMenuBar):
    """自定义菜单栏"""

    # 信号
    sig_action_triggered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.i18n = I18nManager()
        self.setFixedHeight(28)
        self.init_menu()

    def init_menu(self):
        """初始化菜单"""
        # 文件菜单
        file_menu = self.addMenu(self.i18n.get_text("menu.file.label"))
        self._add_file_menu_items(file_menu)

        # 编辑菜单
        edit_menu = self.addMenu(self.i18n.get_text("menu.edit.label"))
        self._add_edit_menu_items(edit_menu)

        # 视图菜单
        view_menu = self.addMenu(self.i18n.get_text("menu.view.label"))
        self._add_view_menu_items(view_menu)

        # 数据菜单
        data_menu = self.addMenu(self.i18n.get_text("menu.data.label"))
        self._add_data_menu_items(data_menu)

        # 分析菜单
        analysis_menu = self.addMenu(self.i18n.get_text("menu.analysis.label"))
        self._add_analysis_menu_items(analysis_menu)

        # 图形菜单
        graph_menu = self.addMenu(self.i18n.get_text("menu.graph.label"))
        self._add_graph_menu_items(graph_menu)

        # 工具菜单
        tools_menu = self.addMenu(self.i18n.get_text("menu.tools.label"))
        self._add_tools_menu_items(tools_menu)

        # 帮助菜单
        help_menu = self.addMenu(self.i18n.get_text("menu.help.label"))
        self._add_help_menu_items(help_menu)

    def _add_file_menu_items(self, menu):
        """添加文件菜单项"""
        new_action = QAction(self.i18n.get_text("menu.file.new"), self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self._on_menu_action)
        menu.addAction(new_action)

        open_action = QAction(self.i18n.get_text("menu.file.open"), self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self._on_menu_action)
        menu.addAction(open_action)

        menu.addSeparator()

        save_action = QAction(self.i18n.get_text("menu.file.save"), self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self._on_menu_action)
        menu.addAction(save_action)

        save_as_action = QAction(self.i18n.get_text("menu.file.save_as"), self)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.triggered.connect(self._on_menu_action)
        menu.addAction(save_as_action)

        menu.addSeparator()

        close_action = QAction(self.i18n.get_text("menu.file.close"), self)
        close_action.setShortcut(QKeySequence("Ctrl+W"))
        close_action.triggered.connect(self._on_menu_action)
        menu.addAction(close_action)

        menu.addSeparator()

        export_action = QAction(self.i18n.get_text("menu.file.export"), self)
        export_action.triggered.connect(self._on_menu_action)
        menu.addAction(export_action)

        menu.addSeparator()

        recent_files_action = QAction(self.i18n.get_text("menu.file.recent_files"), self)
        recent_files_action.triggered.connect(self._on_menu_action)
        menu.addAction(recent_files_action)

        menu.addSeparator()

        exit_action = QAction(self.i18n.get_text("menu.file.exit"), self)
        exit_action.triggered.connect(self._on_menu_action)
        menu.addAction(exit_action)

    def _add_edit_menu_items(self, menu):
        """添加编辑菜单项"""
        undo_action = QAction(self.i18n.get_text("menu.edit.undo"), self)
        undo_action.setShortcut(QKeySequence("Ctrl+Z"))
        undo_action.triggered.connect(self._on_menu_action)
        menu.addAction(undo_action)

        redo_action = QAction(self.i18n.get_text("menu.edit.redo"), self)
        redo_action.setShortcut(QKeySequence("Ctrl+Y"))
        redo_action.triggered.connect(self._on_menu_action)
        menu.addAction(redo_action)

        menu.addSeparator()

        cut_action = QAction(self.i18n.get_text("menu.edit.cut"), self)
        cut_action.setShortcut(QKeySequence("Ctrl+X"))
        cut_action.triggered.connect(self._on_menu_action)
        menu.addAction(cut_action)

        copy_action = QAction(self.i18n.get_text("menu.edit.copy"), self)
        copy_action.setShortcut(QKeySequence("Ctrl+C"))
        copy_action.triggered.connect(self._on_menu_action)
        menu.addAction(copy_action)

        paste_action = QAction(self.i18n.get_text("menu.edit.paste"), self)
        paste_action.setShortcut(QKeySequence("Ctrl+V"))
        paste_action.triggered.connect(self._on_menu_action)
        menu.addAction(paste_action)

        delete_action = QAction(self.i18n.get_text("menu.edit.delete"), self)
        delete_action.setShortcut(QKeySequence("Delete"))
        delete_action.triggered.connect(self._on_menu_action)
        menu.addAction(delete_action)

        menu.addSeparator()

        find_action = QAction(self.i18n.get_text("menu.edit.find"), self)
        find_action.setShortcut(QKeySequence("Ctrl+F"))
        find_action.triggered.connect(self._on_menu_action)
        menu.addAction(find_action)

        select_all_action = QAction(self.i18n.get_text("menu.edit.select_all"), self)
        select_all_action.setShortcut(QKeySequence("Ctrl+A"))
        select_all_action.triggered.connect(self._on_menu_action)
        menu.addAction(select_all_action)

        menu.addSeparator()

        insert_variable_action = QAction(self.i18n.get_text("menu.edit.insert_variable"), self)
        insert_variable_action.triggered.connect(self._on_menu_action)
        menu.addAction(insert_variable_action)

        insert_case_action = QAction(self.i18n.get_text("menu.edit.insert_case"), self)
        insert_case_action.triggered.connect(self._on_menu_action)
        menu.addAction(insert_case_action)

        menu.addSeparator()

        goto_action = QAction(self.i18n.get_text("menu.edit.goto"), self)
        goto_action.setShortcut(QKeySequence("Ctrl+G"))
        goto_action.triggered.connect(self._on_menu_action)
        menu.addAction(goto_action)

    def _add_view_menu_items(self, menu):
        """添加视图菜单项"""
        data_view_action = QAction(self.i18n.get_text("menu.view.data_view"), self)
        data_view_action.setShortcut(QKeySequence("Ctrl+1"))
        data_view_action.triggered.connect(self._on_menu_action)
        menu.addAction(data_view_action)

        variable_view_action = QAction(self.i18n.get_text("menu.view.variable_view"), self)
        variable_view_action.setShortcut(QKeySequence("Ctrl+2"))
        variable_view_action.triggered.connect(self._on_menu_action)
        menu.addAction(variable_view_action)

        output_view_action = QAction(self.i18n.get_text("menu.view.output_view"), self)
        output_view_action.setShortcut(QKeySequence("Ctrl+3"))
        output_view_action.triggered.connect(self._on_menu_action)
        menu.addAction(output_view_action)

        syntax_view_action = QAction(self.i18n.get_text("menu.view.syntax_view"), self)
        syntax_view_action.setShortcut(QKeySequence("Ctrl+4"))
        syntax_view_action.triggered.connect(self._on_menu_action)
        menu.addAction(syntax_view_action)

        menu.addSeparator()

        toolbar_action = QAction(self.i18n.get_text("menu.view.toolbar"), self)
        toolbar_action.setCheckable(True)
        toolbar_action.setChecked(True)
        toolbar_action.triggered.connect(self._on_menu_action)
        menu.addAction(toolbar_action)

        status_bar_action = QAction(self.i18n.get_text("menu.view.status_bar"), self)
        status_bar_action.setCheckable(True)
        status_bar_action.setChecked(True)
        status_bar_action.triggered.connect(self._on_menu_action)
        menu.addAction(status_bar_action)

        navigation_panel_action = QAction(self.i18n.get_text("menu.view.navigation_panel"), self)
        navigation_panel_action.setCheckable(True)
        navigation_panel_action.setChecked(True)
        navigation_panel_action.triggered.connect(self._on_menu_action)
        menu.addAction(navigation_panel_action)

        property_panel_action = QAction(self.i18n.get_text("menu.view.property_panel"), self)
        property_panel_action.setCheckable(True)
        property_panel_action.setChecked(True)
        property_panel_action.triggered.connect(self._on_menu_action)
        menu.addAction(property_panel_action)

        menu.addSeparator()

        theme_menu = menu.addMenu(self.i18n.get_text("menu.view.theme"))
        light_theme_action = QAction(self.i18n.get_text("menu.view.light_theme"), self)
        light_theme_action.setCheckable(True)
        light_theme_action.setChecked(True)
        light_theme_action.triggered.connect(self._on_menu_action)
        theme_menu.addAction(light_theme_action)

        dark_theme_action = QAction(self.i18n.get_text("menu.view.dark_theme"), self)
        dark_theme_action.setCheckable(True)
        dark_theme_action.triggered.connect(self._on_menu_action)
        theme_menu.addAction(dark_theme_action)

        menu.addSeparator()

        zoom_in_action = QAction(self.i18n.get_text("menu.view.zoom_in"), self)
        zoom_in_action.triggered.connect(self._on_menu_action)
        menu.addAction(zoom_in_action)

        zoom_out_action = QAction(self.i18n.get_text("menu.view.zoom_out"), self)
        zoom_out_action.triggered.connect(self._on_menu_action)
        menu.addAction(zoom_out_action)

        reset_zoom_action = QAction(self.i18n.get_text("menu.view.reset_zoom"), self)
        reset_zoom_action.triggered.connect(self._on_menu_action)
        menu.addAction(reset_zoom_action)

    def _add_data_menu_items(self, menu):
        """添加数据菜单项"""
        define_variables_action = QAction(self.i18n.get_text("menu.data.define_variables"), self)
        define_variables_action.triggered.connect(self._on_menu_action)
        menu.addAction(define_variables_action)

        sort_cases_action = QAction(self.i18n.get_text("menu.data.sort_cases"), self)
        sort_cases_action.triggered.connect(self._on_menu_action)
        menu.addAction(sort_cases_action)

        transpose_action = QAction(self.i18n.get_text("menu.data.transpose"), self)
        transpose_action.triggered.connect(self._on_menu_action)
        menu.addAction(transpose_action)

        merge_files_action = QAction(self.i18n.get_text("menu.data.merge_files"), self)
        merge_files_action.triggered.connect(self._on_menu_action)
        menu.addAction(merge_files_action)

        restructure_action = QAction(self.i18n.get_text("menu.data.restructure"), self)
        restructure_action.triggered.connect(self._on_menu_action)
        menu.addAction(restructure_action)

        aggregate_action = QAction(self.i18n.get_text("menu.data.aggregate"), self)
        aggregate_action.triggered.connect(self._on_menu_action)
        menu.addAction(aggregate_action)

        weight_cases_action = QAction(self.i18n.get_text("menu.data.weight_cases"), self)
        weight_cases_action.triggered.connect(self._on_menu_action)
        menu.addAction(weight_cases_action)

        select_cases_action = QAction(self.i18n.get_text("menu.data.select_cases"), self)
        select_cases_action.triggered.connect(self._on_menu_action)
        menu.addAction(select_cases_action)

        split_file_action = QAction(self.i18n.get_text("menu.data.split_file"), self)
        split_file_action.triggered.connect(self._on_menu_action)
        menu.addAction(split_file_action)

        identify_duplicates_action = QAction(self.i18n.get_text("menu.data.identify_duplicates"), self)
        identify_duplicates_action.triggered.connect(self._on_menu_action)
        menu.addAction(identify_duplicates_action)

        missing_value_analysis_action = QAction(self.i18n.get_text("menu.data.missing_value_analysis"), self)
        missing_value_analysis_action.triggered.connect(self._on_menu_action)
        menu.addAction(missing_value_analysis_action)

    def _add_analysis_menu_items(self, menu):
        """添加分析菜单项"""
        descriptive_action = QAction(self.i18n.get_text("menu.analysis.descriptive"), self)
        descriptive_action.triggered.connect(self._on_menu_action)
        menu.addAction(descriptive_action)

        frequency_action = QAction(self.i18n.get_text("menu.analysis.frequency"), self)
        frequency_action.triggered.connect(self._on_menu_action)
        menu.addAction(frequency_action)

        crosstabs_action = QAction(self.i18n.get_text("menu.analysis.crosstabs"), self)
        crosstabs_action.triggered.connect(self._on_menu_action)
        menu.addAction(crosstabs_action)

        means_action = QAction(self.i18n.get_text("menu.analysis.means"), self)
        means_action.triggered.connect(self._on_menu_action)
        menu.addAction(means_action)

        t_test_action = QAction(self.i18n.get_text("menu.analysis.t_test"), self)
        t_test_action.triggered.connect(self._on_menu_action)
        menu.addAction(t_test_action)

        anova_action = QAction(self.i18n.get_text("menu.analysis.anova"), self)
        anova_action.triggered.connect(self._on_menu_action)
        menu.addAction(anova_action)

        nonparametric_action = QAction(self.i18n.get_text("menu.analysis.nonparametric"), self)
        nonparametric_action.triggered.connect(self._on_menu_action)
        menu.addAction(nonparametric_action)

        correlation_action = QAction(self.i18n.get_text("menu.analysis.correlation"), self)
        correlation_action.triggered.connect(self._on_menu_action)
        menu.addAction(correlation_action)

        regression_action = QAction(self.i18n.get_text("menu.analysis.regression"), self)
        regression_action.triggered.connect(self._on_menu_action)
        menu.addAction(regression_action)

        classification_action = QAction(self.i18n.get_text("menu.analysis.classification"), self)
        classification_action.triggered.connect(self._on_menu_action)
        menu.addAction(classification_action)

        dimension_reduction_action = QAction(self.i18n.get_text("menu.analysis.dimension_reduction"), self)
        dimension_reduction_action.triggered.connect(self._on_menu_action)
        menu.addAction(dimension_reduction_action)

        scale_action = QAction(self.i18n.get_text("menu.analysis.scale"), self)
        scale_action.triggered.connect(self._on_menu_action)
        menu.addAction(scale_action)

        survival_action = QAction(self.i18n.get_text("menu.analysis.survival"), self)
        survival_action.triggered.connect(self._on_menu_action)
        menu.addAction(survival_action)

        multiple_response_action = QAction(self.i18n.get_text("menu.analysis.multiple_response"), self)
        multiple_response_action.triggered.connect(self._on_menu_action)
        menu.addAction(multiple_response_action)

        time_series_action = QAction(self.i18n.get_text("menu.analysis.time_series"), self)
        time_series_action.triggered.connect(self._on_menu_action)
        menu.addAction(time_series_action)

        missing_value_action = QAction(self.i18n.get_text("menu.analysis.missing_value"), self)
        missing_value_action.triggered.connect(self._on_menu_action)
        menu.addAction(missing_value_action)

        advanced_action = QAction(self.i18n.get_text("menu.analysis.advanced"), self)
        advanced_action.triggered.connect(self._on_menu_action)
        menu.addAction(advanced_action)

        machine_learning_action = QAction(self.i18n.get_text("menu.analysis.machine_learning"), self)
        machine_learning_action.triggered.connect(self._on_menu_action)
        menu.addAction(machine_learning_action)

        causal_inference_action = QAction(self.i18n.get_text("menu.analysis.causal_inference"), self)
        causal_inference_action.triggered.connect(self._on_menu_action)
        menu.addAction(causal_inference_action)

        bayesian_action = QAction(self.i18n.get_text("menu.analysis.bayesian"), self)
        bayesian_action.triggered.connect(self._on_menu_action)
        menu.addAction(bayesian_action)

        network_action = QAction(self.i18n.get_text("menu.analysis.network"), self)
        network_action.triggered.connect(self._on_menu_action)
        menu.addAction(network_action)

        spatial_action = QAction(self.i18n.get_text("menu.analysis.spatial"), self)
        spatial_action.triggered.connect(self._on_menu_action)
        menu.addAction(spatial_action)

        text_mining_action = QAction(self.i18n.get_text("menu.analysis.text_mining"), self)
        text_mining_action.triggered.connect(self._on_menu_action)
        menu.addAction(text_mining_action)

    def _add_graph_menu_items(self, menu):
        """添加图形菜单项"""
        chart_builder_action = QAction(self.i18n.get_text("menu.graph.chart_builder"), self)
        chart_builder_action.triggered.connect(self._on_menu_action)
        menu.addAction(chart_builder_action)

        menu.addSeparator()

        bar_action = QAction(self.i18n.get_text("menu.graph.bar"), self)
        bar_action.triggered.connect(self._on_menu_action)
        menu.addAction(bar_action)

        histogram_action = QAction(self.i18n.get_text("menu.graph.histogram"), self)
        histogram_action.triggered.connect(self._on_menu_action)
        menu.addAction(histogram_action)

        scatter_action = QAction(self.i18n.get_text("menu.graph.scatter"), self)
        scatter_action.triggered.connect(self._on_menu_action)
        menu.addAction(scatter_action)

        line_action = QAction(self.i18n.get_text("menu.graph.line"), self)
        line_action.triggered.connect(self._on_menu_action)
        menu.addAction(line_action)

        pie_action = QAction(self.i18n.get_text("menu.graph.pie"), self)
        pie_action.triggered.connect(self._on_menu_action)
        menu.addAction(pie_action)

        boxplot_action = QAction(self.i18n.get_text("menu.graph.boxplot"), self)
        boxplot_action.triggered.connect(self._on_menu_action)
        menu.addAction(boxplot_action)

        heatmap_action = QAction(self.i18n.get_text("menu.graph.heatmap"), self)
        heatmap_action.triggered.connect(self._on_menu_action)
        menu.addAction(heatmap_action)

        qq_plot_action = QAction(self.i18n.get_text("menu.graph.qq_plot"), self)
        qq_plot_action.triggered.connect(self._on_menu_action)
        menu.addAction(qq_plot_action)

        roc_curve_action = QAction(self.i18n.get_text("menu.graph.roc_curve"), self)
        roc_curve_action.triggered.connect(self._on_menu_action)
        menu.addAction(roc_curve_action)

        custom_action = QAction(self.i18n.get_text("menu.graph.custom"), self)
        custom_action.triggered.connect(self._on_menu_action)
        menu.addAction(custom_action)

    def _add_tools_menu_items(self, menu):
        """添加工具菜单项"""
        options_action = QAction(self.i18n.get_text("menu.tools.options"), self)
        options_action.setShortcut(QKeySequence("Ctrl+,", QKeySequence.NativeText))
        options_action.triggered.connect(self._on_menu_action)
        menu.addAction(options_action)

        syntax_editor_action = QAction(self.i18n.get_text("menu.tools.syntax_editor"), self)
        syntax_editor_action.setShortcut(QKeySequence("Ctrl+Shift+N"))
        syntax_editor_action.triggered.connect(self._on_menu_action)
        menu.addAction(syntax_editor_action)

        custom_dialogs_action = QAction(self.i18n.get_text("menu.tools.custom_dialogs"), self)
        custom_dialogs_action.triggered.connect(self._on_menu_action)
        menu.addAction(custom_dialogs_action)

        package_manager_action = QAction(self.i18n.get_text("menu.tools.package_manager"), self)
        package_manager_action.triggered.connect(self._on_menu_action)
        menu.addAction(package_manager_action)

    def _add_help_menu_items(self, menu):
        """添加帮助菜单项"""
        contents_action = QAction(self.i18n.get_text("menu.help.contents"), self)
        contents_action.setShortcut(QKeySequence("F1"))
        contents_action.triggered.connect(self._on_menu_action)
        menu.addAction(contents_action)

        tutorial_action = QAction(self.i18n.get_text("menu.help.tutorial"), self)
        tutorial_action.triggered.connect(self._on_menu_action)
        menu.addAction(tutorial_action)

        menu.addSeparator()

        about_action = QAction(self.i18n.get_text("menu.help.about"), self)
        about_action.triggered.connect(self._on_menu_action)
        menu.addAction(about_action)

        check_update_action = QAction(self.i18n.get_text("menu.help.check_update"), self)
        check_update_action.triggered.connect(self._on_menu_action)
        menu.addAction(check_update_action)

        license_action = QAction(self.i18n.get_text("menu.help.license"), self)
        license_action.triggered.connect(self._on_menu_action)
        menu.addAction(license_action)

    def _on_menu_action(self):
        """菜单动作处理"""
        action = self.sender()
        action_text = action.text()
        print(f"Menu action triggered: {action_text}")
        
        # 发送信号到主窗口
        self.sig_action_triggered.emit(action_text)
        
        # 这里添加具体的菜单处理逻辑
        # 根据菜单文本执行不同的操作
        if action_text == self.i18n.get_text("menu.file.new"):
            # 新建数据集
            if hasattr(self.parent(), 'new_dataset'):
                self.parent().new_dataset()
        elif action_text == self.i18n.get_text("menu.file.open"):
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
        elif action_text == self.i18n.get_text("menu.file.save"):
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
        elif action_text == self.i18n.get_text("menu.file.save_as"):
            # 另存为
            if hasattr(self.parent(), 'save_data'):
                from PyQt6.QtWidgets import QFileDialog
                file_filter = "CSV files (*.csv);;Excel files (*.xlsx);;Text files (*.txt);;JSON files (*.json)"
                path, _ = QFileDialog.getSaveFileName(self.parent(), "另存为", "", file_filter)
                if path:
                    import os
                    _, ext = os.path.splitext(path)
                    file_type = ext.lower().lstrip('.')
                    if not file_type:
                        # 默认保存为CSV
                        path += ".csv"
                        file_type = "csv"
                    self.parent().save_data(path, file_type)
        elif action_text == self.i18n.get_text("menu.file.close"):
            # 关闭文件
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("关闭文件")
        elif action_text == self.i18n.get_text("menu.file.export"):
            # 导出文件
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("导出文件")
        elif action_text == self.i18n.get_text("menu.file.exit"):
            # 退出程序
            if hasattr(self.parent(), 'close'):
                self.parent().close()
        elif action_text == self.i18n.get_text("menu.edit.undo"):
            # 撤销操作
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("撤销操作")
        elif action_text == self.i18n.get_text("menu.edit.redo"):
            # 重做操作
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("重做操作")
        elif action_text == self.i18n.get_text("menu.edit.cut"):
            # 剪切操作
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("剪切操作")
        elif action_text == self.i18n.get_text("menu.edit.copy"):
            # 复制操作
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("复制操作")
        elif action_text == self.i18n.get_text("menu.edit.paste"):
            # 粘贴操作
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("粘贴操作")
        elif action_text == self.i18n.get_text("menu.view.data_view"):
            # 数据视图
            if hasattr(self.parent(), 'switch_tab'):
                self.parent().switch_tab("data_view")
        elif action_text == self.i18n.get_text("menu.view.variable_view"):
            # 变量视图
            if hasattr(self.parent(), 'switch_tab'):
                self.parent().switch_tab("variable_view")
        elif action_text == self.i18n.get_text("menu.view.output_view"):
            # 输出视图
            if hasattr(self.parent(), 'switch_tab'):
                self.parent().switch_tab("output_view")
        elif action_text == self.i18n.get_text("menu.view.syntax_view"):
            # 语法视图
            if hasattr(self.parent(), 'switch_tab'):
                self.parent().switch_tab("syntax_view")
        elif action_text == self.i18n.get_text("menu.view.light_theme"):
            # 亮色主题
            if hasattr(self.parent(), 'set_theme'):
                self.parent().set_theme("light")
        elif action_text == self.i18n.get_text("menu.view.dark_theme"):
            # 暗色主题
            if hasattr(self.parent(), 'set_theme'):
                self.parent().set_theme("dark")
        elif action_text == self.i18n.get_text("menu.analysis.descriptive"):
            # 描述性统计
            if hasattr(self.parent(), 'show_analysis_dialog'):
                self.parent().show_analysis_dialog("descriptive")
        elif action_text == self.i18n.get_text("menu.analysis.frequency"):
            # 频率分析
            if hasattr(self.parent(), 'show_analysis_dialog'):
                self.parent().show_analysis_dialog("frequency")
        elif action_text == self.i18n.get_text("menu.analysis.correlation"):
            # 相关性分析
            if hasattr(self.parent(), 'show_analysis_dialog'):
                self.parent().show_analysis_dialog("correlation")
        elif action_text == self.i18n.get_text("menu.tools.options"):
            # 设置选项
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("打开设置")
            from src.axaltyx_gui.dialogs.settings_dialog import SettingsDialog
            dialog = SettingsDialog(self.parent())
            if hasattr(self.parent(), '_on_settings_changed'):
                dialog.sig_settings_changed.connect(self.parent()._on_settings_changed)
            dialog.exec()
        elif action_text == self.i18n.get_text("menu.help.contents"):
            # 帮助内容
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("打开帮助")
            from src.axaltyx_gui.dialogs.help_dialog import HelpDialog
            dialog = HelpDialog(self.parent())
            dialog.exec()
        elif action_text == self.i18n.get_text("menu.help.about"):
            # 关于
            if hasattr(self.parent(), 'update_status'):
                self.parent().update_status("打开关于")
            from src.axaltyx_gui.dialogs.about_dialog import AboutDialog
            dialog = AboutDialog(self.parent())
            dialog.exec()
