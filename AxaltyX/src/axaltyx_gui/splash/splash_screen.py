from PyQt6.QtWidgets import QSplashScreen, QApplication
from PyQt6.QtGui import QPainter, QColor, QFont, QLinearGradient, QBrush
from PyQt6.QtCore import Qt, QRect

class AxaltyXSplashScreen(QSplashScreen):
    """启动页，显示Logo和加载进度"""

    def __init__(self):
        super().__init__()
        self.setFixedSize(520, 360)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.progress = 0
        self.loading_step = "Loading core modules..."
        self.init_ui()

    def init_ui(self) -> None:
        self.setObjectName("AxaltyXSplashScreen")

    def draw_logo(self, painter: QPainter) -> None:
        # 绘制品牌渐变色Logo
        gradient = QLinearGradient(220, 100, 300, 180)
        gradient.setColorAt(0, QColor(20, 201, 201))  # #14C9C9
        gradient.setColorAt(1, QColor(22, 93, 255))   # #165DFF
        painter.setBrush(QBrush(gradient))
        painter.drawRect(QRect(220, 100, 80, 80))

    def draw_progress_bar(self, painter: QPainter, progress: float) -> None:
        # 绘制进度条背景
        painter.setBrush(QColor(242, 243, 245))  # --color-fill-2
        painter.drawRoundedRect(QRect(100, 240, 320, 4), 2, 2)
        
        # 绘制进度条填充
        if progress > 0:
            gradient = QLinearGradient(100, 240, 100 + 320 * progress, 244)
            gradient.setColorAt(0, QColor(20, 201, 201))  # #14C9C9
            gradient.setColorAt(1, QColor(22, 93, 255))   # #165DFF
            painter.setBrush(QBrush(gradient))
            painter.drawRoundedRect(QRect(100, 240, int(320 * progress), 4), 2, 2)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制白色背景
        painter.fillRect(self.rect(), QColor(255, 255, 255))
        
        # 绘制Logo
        self.draw_logo(painter)
        
        # 绘制标题
        painter.setFont(QFont("Microsoft YaHei", 36, QFont.Weight.Bold))
        painter.setPen(QColor(29, 33, 41))  # --color-text-primary
        painter.drawText(QRect(0, 190, 520, 44), Qt.AlignmentFlag.AlignCenter, "AxaltyX")
        
        # 绘制版本号
        painter.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Regular))
        painter.setPen(QColor(134, 144, 156))  # --color-text-tertiary
        painter.drawText(QRect(0, 220, 520, 22), Qt.AlignmentFlag.AlignCenter, "v1.0.0")
        
        # 绘制进度条
        self.draw_progress_bar(painter, self.progress / 100)
        
        # 绘制加载文字
        painter.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Regular))
        painter.setPen(QColor(134, 144, 156))  # --color-text-tertiary
        painter.drawText(QRect(0, 250, 520, 20), Qt.AlignmentFlag.AlignCenter, self.loading_step)
        
        # 绘制版权信息
        painter.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Regular))
        painter.setPen(QColor(201, 205, 212))  # --color-text-disabled
        painter.drawText(QRect(0, 280, 520, 20), Qt.AlignmentFlag.AlignCenter, "Copyright (c) TBJ114")

    def set_loading_step(self, step_name: str) -> None:
        self.loading_step = step_name
        self.update()

    def set_progress(self, value: int) -> None:
        self.progress = max(0, min(100, value))
        self.update()

    def finish_animation(self) -> None:
        # 简单的淡出动画
        for i in range(100, -1, -10):
            self.setWindowOpacity(i / 100)
            QApplication.processEvents()
        self.hide()