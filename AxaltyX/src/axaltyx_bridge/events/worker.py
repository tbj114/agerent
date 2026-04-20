from PyQt6.QtCore import QThread, pyqtSignal
from concurrent.futures import ThreadPoolExecutor, Future


class AnalysisWorker(QThread):
    """分析工作线程"""

    sig_finished = pyqtSignal(str, dict)   # (analysis_name, result)
    sig_error = pyqtSignal(str, str)       # (analysis_name, error_msg)
    sig_progress = pyqtSignal(int, int)    # (current, total)

    def __init__(self, analysis_func: callable, params: dict):
        super().__init__()
        self.analysis_func = analysis_func
        self.params = params
        self.analysis_name = params.get('analysis_name', 'unknown')
        self._is_cancelled = False

    def run(self) -> None:
        """执行分析任务"""
        try:
            # 执行分析函数
            result = self.analysis_func(self.params)
            
            # 检查是否被取消
            if self._is_cancelled:
                return
            
            # 发射完成信号
            self.sig_finished.emit(self.analysis_name, result)
            
        except Exception as e:
            # 检查是否被取消
            if self._is_cancelled:
                return
            
            # 发射错误信号
            self.sig_error.emit(self.analysis_name, str(e))

    def cancel(self) -> None:
        """取消任务"""
        self._is_cancelled = True


class ThreadPoolManager:
    """线程池管理"""

    def __init__(self, max_workers: int = 4):
        """初始化线程池"""
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_workers = []

    def submit(self, func: callable, *args, **kwargs) -> Future:
        """提交任务到线程池"""
        future = self.executor.submit(func, *args, **kwargs)
        return future

    def submit_analysis(self, analysis_name: str, func: callable, params: dict) -> AnalysisWorker:
        """提交分析任务到工作线程"""
        # 创建工作线程
        worker = AnalysisWorker(func, params)
        
        # 存储工作线程
        self.active_workers.append(worker)
        
        # 连接信号
        def on_finished(name, result):
            if worker in self.active_workers:
                self.active_workers.remove(worker)
        
        def on_error(name, error):
            if worker in self.active_workers:
                self.active_workers.remove(worker)
        
        worker.sig_finished.connect(on_finished)
        worker.sig_error.connect(on_error)
        
        # 启动线程
        worker.start()
        
        return worker

    def cancel_all(self) -> None:
        """取消所有任务"""
        # 取消所有活跃的工作线程
        for worker in self.active_workers:
            worker.cancel()
        
        # 清空活跃工作线程列表
        self.active_workers.clear()

    def active_count(self) -> int:
        """获取活跃线程数"""
        return len(self.active_workers)

    def wait_all(self) -> None:
        """等待所有任务完成"""
        # 等待所有活跃的工作线程完成
        for worker in self.active_workers:
            worker.waitForFinished()
