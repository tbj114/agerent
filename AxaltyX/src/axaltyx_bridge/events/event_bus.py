from PyQt6.QtCore import QObject, QTimer
import uuid


class EventBus(QObject):
    """事件总线，支持发布-订阅模式"""

    def __init__(self):
        super().__init__()
        # 存储事件订阅者，格式: {event_name: {subscription_id: handler}}
        self._subscribers = {}

    def subscribe(self, event_name: str, handler: callable) -> str:
        """订阅事件，返回订阅 ID"""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = {}
        
        # 生成唯一的订阅 ID
        subscription_id = str(uuid.uuid4())
        self._subscribers[event_name][subscription_id] = handler
        
        return subscription_id

    def unsubscribe(self, subscription_id: str) -> None:
        """取消订阅"""
        # 遍历所有事件，查找并移除订阅
        for event_name, subscribers in self._subscribers.items():
            if subscription_id in subscribers:
                del subscribers[subscription_id]
                # 如果事件没有订阅者了，删除事件
                if not subscribers:
                    del self._subscribers[event_name]
                break

    def publish(self, event_name: str, data: dict = None) -> None:
        """发布事件"""
        if event_name in self._subscribers:
            # 遍历所有订阅者并调用处理函数
            for handler in self._subscribers[event_name].values():
                try:
                    if data is None:
                        handler()
                    else:
                        handler(data)
                except Exception as e:
                    print(f"Error handling event {event_name}: {str(e)}")

    def publish_delayed(self, event_name: str, data: dict, delay_ms: int) -> None:
        """延迟发布事件"""
        # 创建定时器，延迟后发布事件
        timer = QTimer(self)
        timer.setSingleShot(True)
        
        def on_timeout():
            self.publish(event_name, data)
            timer.deleteLater()
        
        timer.timeout.connect(on_timeout)
        timer.start(delay_ms)
