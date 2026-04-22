from PyQt6.QtCore import QObject, pyqtSignal


class BridgeSignals(QObject):
    """全局信号集合"""

    # ---- 数据操作信号 ----
    sig_data_load_requested = pyqtSignal(str, str)        # (path, file_type)
    sig_data_load_completed = pyqtSignal(dict)            # {success, data, columns, shape, ...}
    sig_data_save_requested = pyqtSignal(str, str, str)   # (path, file_type, encoding)
    sig_data_save_completed = pyqtSignal(dict)            # {success, path, ...}
    sig_data_new_requested = pyqtSignal(int, int)         # (rows, cols)
    sig_data_new_completed = pyqtSignal(dict)             # {success, data, shape}
    sig_data_changed = pyqtSignal(dict)                   # {action, row, col, value}
    sig_variable_changed = pyqtSignal(str, dict)          # (var_name, metadata)

    # ---- 分析操作信号 ----
    sig_analysis_requested = pyqtSignal(str, dict)        # (analysis_name, params)
    sig_analysis_started = pyqtSignal(str)                # analysis_name
    sig_analysis_progress = pyqtSignal(str, int, int)     # (analysis_name, current, total)
    sig_analysis_completed = pyqtSignal(str, dict)        # (analysis_name, results)
    sig_analysis_failed = pyqtSignal(str, str)            # (analysis_name, error_msg)

    # ---- 图表操作信号 ----
    sig_chart_requested = pyqtSignal(str, dict)           # (chart_type, params)
    sig_chart_created = pyqtSignal(str, object)           # (chart_id, figure)
    sig_chart_export_requested = pyqtSignal(str, str, str) # (chart_id, path, format)
    sig_chart_export_completed = pyqtSignal(dict)

    # ---- UI 操作信号 ----
    sig_language_changed = pyqtSignal(str)                # lang_code
    sig_theme_changed = pyqtSignal(str)                   # theme_name
    sig_settings_changed = pyqtSignal(dict)               # settings_dict
    sig_status_message = pyqtSignal(str, int)             # (message, timeout)
    sig_notification = pyqtSignal(str, str, str)          # (type, title, message)
    sig_dialog_open = pyqtSignal(str, dict)               # (dialog_name, params)
    sig_dialog_close = pyqtSignal(str)                    # dialog_name

    # ---- 语法操作信号 ----
    sig_syntax_execute = pyqtSignal(str)                  # syntax_string
    sig_syntax_generated = pyqtSignal(str, str)           # (analysis_name, syntax)
