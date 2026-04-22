from PyQt6.QtWidgets import QStatusBar, QLabel, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
import psutil
import platform
from src.axaltyx_i18n.manager import I18nManager


class AxaltyXStatusBar(QStatusBar):
    """状态栏"""

    def __init__(self, parent: QWidget = None):
        """初始化状态栏

        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.i18n = I18nManager()
        self._init_ui()
        self._start_system_monitor()

    def _init_ui(self):
        """初始化状态栏UI"""
        # 左侧区域：主要消息
        self.message_label = QLabel("", self)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.message_label.setMinimumWidth(200)
        
        # 中间区域：数据信息
        self.data_info_label = QLabel("", self)
        self.data_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        
        # 右侧区域：系统信息和语言
        right_widget = QWidget(self)
        right_layout = QHBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(16)
        
        # 系统信息
        self.system_info_label = QLabel("", self)
        self.system_info_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        # 语言指示器
        self.language_label = QLabel("中文", self)
        self.language_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.language_label.setMinimumWidth(60)
        
        right_layout.addWidget(self.system_info_label)
        right_layout.addWidget(self.language_label)
        
        # 添加到状态栏
        self.addWidget(self.message_label, 1)
        self.addWidget(self.data_info_label, 1)
        self.addWidget(right_widget, 1)
        
        # 设置样式
        self.setStyleSheet("""
            QStatusBar {
                background-color: #F7F8FA;
                border-top: 1px solid #E5E6EB;
                color: #4E5969;
                font-size: 12px;
                padding: 0 8px;
            }
            QStatusBar QLabel {
                color: #4E5969;
                padding: 0 4px;
            }
        """)

    def show_message(self, message: str, timeout: int = 0) -> None:
        """显示消息

        Args:
            message: 消息内容
            timeout: 显示时间（毫秒），0表示一直显示
        """
        self.message_label.setText(message)
        if timeout > 0:
            QTimer.singleShot(timeout, lambda: self.message_label.setText(""))

    def update_data_info(self, rows: int, cols: int) -> None:
        """更新数据信息

        Args:
            rows: 行数
            cols: 列数
        """
        text = self.i18n.get_text("status.rows_cols", rows=rows, cols=cols)
        self.data_info_label.setText(text)

    def update_system_info(self, cpu: float = None, memory: float = None) -> None:
        """更新系统信息

        Args:
            cpu: CPU使用率
            memory: 内存使用量（MB）
        """
        if cpu is None:
            cpu = psutil.cpu_percent(interval=0.1)
        if memory is None:
            memory = psutil.virtual_memory().used / (1024 * 1024)
        
        cpu_text = self.i18n.get_text("status.cpu", percent=round(cpu, 1))
        memory_text = self.i18n.get_text("status.memory", value=round(memory, 1))
        
        self.system_info_label.setText(f"{cpu_text} | {memory_text}")

    def update_language_indicator(self, lang: str) -> None:
        """更新语言指示器

        Args:
            lang: 语言代码
        """
        lang_map = {
            "zh_CN": "中文",
            "en_US": "English",
            "ja_JP": "日本語"
        }
        self.language_label.setText(lang_map.get(lang, lang))

    def _start_system_monitor(self):
        """启动系统监控"""
        self.system_timer = QTimer(self)
        self.system_timer.timeout.connect(self.update_system_info)
        self.system_timer.start(1000)  # 每秒更新一次

    def closeEvent(self, event):
        """关闭事件"""
        self.system_timer.stop()
        super().closeEvent(event)
