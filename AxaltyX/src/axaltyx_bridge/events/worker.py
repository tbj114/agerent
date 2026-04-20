from PyQt6.QtCore import QThread, pyqtSignal
from concurrent.futures import ThreadPoolExecutor, Future


class AnalysisWorker(QThread):
    """分析工作线程"""

    sig_finished = pyqtSignal(str, dict)   # (analysis_name, result)
    sig_error = pyqtSignal(str, str)       # (analysis_name, error_msg)
    sig_progress = pyqtSignal(int, int)    # (current, total)

    def __init__(self, analysis_func: callable, params: dict):
        """
        初始化分析工作线程
        
        Args:
            analysis_func: 分析函数
            params: 分析参数
        """
        super().__init__()
        self.analysis_func = analysis_func
        self.params = params
        self.analysis_name = params.get('analysis_name', 'unknown')
        self._is_cancelled = False

    def run(self) -> None:
        """运行分析任务"""
        try:
            # 执行分析
            result = self.analysis_func(**self.params)
            
            # 发射完成信号
            if not self._is_cancelled:
                self.sig_finished.emit(self.analysis_name, result)
        except Exception as e:
            # 发射错误信号
            if not self._is_cancelled:
                self.sig_error.emit(self.analysis_name, str(e))

    def cancel(self) -> None:
        """取消任务"""
        self._is_cancelled = True
        # 这里可以添加取消逻辑


class ThreadPoolManager:
    """线程池管理"""

    def __init__(self, max_workers: int = 4):
        """
        初始化线程池管理器
        
        Args:
            max_workers: 最大工作线程数
        """
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.workers = []  # 存储分析工作线程

    def submit(self, func: callable, *args, **kwargs) -> Future:
        """
        提交任务到线程池
        
        Args:
            func: 任务函数
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            Future 对象
        """
        return self.executor.submit(func, *args, **kwargs)

    def submit_analysis(self, analysis_name: str, func: callable, params: dict) -> AnalysisWorker:
        """
        提交分析任务
        
        Args:
            analysis_name: 分析名称
            func: 分析函数
            params: 分析参数
        
        Returns:
            AnalysisWorker 对象
        """
        # 创建分析工作线程
        worker = AnalysisWorker(func, params)
        # 存储工作线程
        self.workers.append(worker)
        # 启动线程
        worker.start()
        return worker

    def cancel_all(self) -> None:
        """取消所有任务"""
        # 取消所有分析工作线程
        for worker in self.workers:
            worker.cancel()
        # 清空工作线程列表
        self.workers.clear()
        # 关闭线程池
        self.executor.shutdown(wait=False)
        # 重新创建线程池
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)

    def active_count(self) -> int:
        """
        获取活跃线程数
        
        Returns:
            活跃线程数
        """
        return len([worker for worker in self.workers if worker.isRunning()])

    def wait_all(self) -> None:
        """
        等待所有任务完成
        """
        # 等待所有分析工作线程完成
        for worker in self.workers:
            worker.waitForFinished()
        # 清空工作线程列表
        self.workers.clear()
        # 关闭线程池
        self.executor.shutdown(wait=True)
        # 重新创建线程池
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
