from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtGui import QIcon, QFont, QColor, QPainter, QBrush
from PyQt6.QtCore import pyqtSignal, Qt, QPoint

class AxaltyXTitleBar(QWidget):
    """自定义标题栏（无边框窗口）"""

    sig_minimize = pyqtSignal()
    sig_maximize = pyqtSignal()
    sig_close = pyqtSignal()

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(32)
        self.mouse_pos = QPoint()
        self.is_pressing = False
        self.init_ui()

    def init_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 8, 0)
        layout.setSpacing(0)

        # Logo
        self.logo_label = QLabel(self)
        self.logo_label.setFixedSize(24, 24)
        layout.addWidget(self.logo_label)

        # 标题
        self.title_label = QLabel("AxaltyX", self)
        font = QFont("Microsoft YaHei", 16, QFont.Weight.Medium)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color: #1D2129;")  # --color-text-primary
        layout.addWidget(self.title_label)

        # 占位符
        layout.addStretch()

        # 窗口控制按钮
        self.minimize_btn = QPushButton("-", self)
        self.maximize_btn = QPushButton("[]", self)
        self.close_btn = QPushButton("x", self)

        for btn in [self.minimize_btn, self.maximize_btn, self.close_btn]:
            btn.setFixedSize(32, 32)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    font-family: 'Microsoft YaHei';
                    font-size: 14px;
                    color: #4E5969;
                }
                QPushButton:hover {
                    background: #F2F3F5;
                }
            """)
            layout.addWidget(btn)

        # 关闭按钮特殊样式
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-family: 'Microsoft YaHei';
                font-size: 14px;
                color: #4E5969;
            }
            QPushButton:hover {
                background: #F53F3F;
                color: white;
            }
        """)

        # 信号连接
        self.minimize_btn.clicked.connect(self.sig_minimize.emit)
        self.maximize_btn.clicked.connect(self.sig_maximize.emit)
        self.close_btn.clicked.connect(self.sig_close.emit)

    def set_title(self, title: str) -> None:
        self.title_label.setText(title)

    def set_icon(self, icon: QIcon) -> None:
        self.logo_label.setPixmap(icon.pixmap(24, 24))

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_pressing = True
            self.mouse_pos = event.globalPosition().toPoint() - self.parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        if self.is_pressing:
            self.parent.move(event.globalPosition().toPoint() - self.mouse_pos)
            event.accept()

    def mouseReleaseEvent(self, event) -> None:
        self.is_pressing = False

    def mouseDoubleClickEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.sig_maximize.emit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawRect(self.rect())
        # 绘制底部边框
        painter.setPen(QColor(229, 230, 235))  # --color-border
        painter.drawLine(0, self.height() - 1, self.width(), self.height() - 1)