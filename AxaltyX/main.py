import sys
import time
import logging
from PyQt6.QtWidgets import QApplication
from src.axaltyx_gui.splash.splash_screen import AxaltyXSplashScreen
from src.axaltyx_gui.main_window.main_window import AxaltyXMainWindow

# 配置日志系统
def configure_logging():
    """配置应用日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            # 可以添加文件处理器
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info("Application started")

class AxaltyXApp:
    """AxaltyX 应用入口"""

    def __init__(self):
        # 配置日志
        configure_logging()
        
        self.app = QApplication(sys.argv)
        self.splash = AxaltyXSplashScreen()
        self.main_window = None

    def run(self):
        """运行应用"""
        # 显示启动页
        self.splash.show()
        self.app.processEvents()

        # 模拟加载过程
        self.load_core_modules()

        # 创建并显示主窗口
        self.main_window = AxaltyXMainWindow()
        self.main_window.show()

        # 关闭启动页
        self.splash.finish_animation()

        # 运行应用事件循环
        sys.exit(self.app.exec())

    def load_core_modules(self):
        """模拟加载核心模块"""
        modules = [
            "Loading core modules...",
            "Initializing data engine...",
            "Setting up analysis modules...",
            "Loading UI components...",
            "Preparing workspace..."
        ]

        for i, module in enumerate(modules):
            self.splash.set_loading_step(module)
            self.splash.set_progress((i + 1) * 20)
            time.sleep(0.5)  # 模拟加载时间
            self.app.processEvents()

if __name__ == "__main__":
    app = AxaltyXApp()
    app.run()