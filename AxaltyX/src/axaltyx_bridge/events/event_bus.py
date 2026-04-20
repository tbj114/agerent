from PyQt6.QtCore import QObject, QTimer
import uuid


class EventBus(QObject):
    """事件总线，支持发布-订阅模式"""

    def __init__(self):
        """初始化事件总线"""
        super().__init__()
        # 存储订阅信息，格式：{event_name: {subscription_id: handler}}
        self._subscriptions = {}

    def subscribe(self, event_name: str, handler: callable) -> str:
        """
        订阅事件
        
        Args:
            event_name: 事件名称
            handler: 事件处理函数
        
        Returns:
            订阅 ID
        """
        # 生成唯一的订阅 ID
        subscription_id = str(uuid.uuid4())
        
        # 如果事件名称不存在，创建一个新的订阅字典
        if event_name not in self._subscriptions:
            self._subscriptions[event_name] = {}
        
        # 添加订阅
        self._subscriptions[event_name][subscription_id] = handler
        
        return subscription_id

    def unsubscribe(self, subscription_id: str) -> None:
        """
        取消订阅
        
        Args:
            subscription_id: 订阅 ID
        """
        # 遍历所有事件，查找并删除订阅
        for event_name, subscriptions in list(self._subscriptions.items()):
            if subscription_id in subscriptions:
                del subscriptions[subscription_id]
                # 如果事件没有订阅者，删除事件
                if not subscriptions:
                    del self._subscriptions[event_name]
                break

    def publish(self, event_name: str, data: dict = None) -> None:
        """
        发布事件
        
        Args:
            event_name: 事件名称
            data: 事件数据
        """
        # 检查事件是否有订阅者
        if event_name in self._subscriptions:
            # 复制订阅者列表，避免在处理过程中修改
            subscriptions = list(self._subscriptions[event_name].values())
            # 调用所有订阅者的处理函数
            for handler in subscriptions:
                try:
                    handler(data)
                except Exception as e:
                    print(f"Error handling event {event_name}: {str(e)}")

    def publish_delayed(self, event_name: str, data: dict, delay_ms: int) -> None:
        """
        延迟发布事件
        
        Args:
            event_name: 事件名称
            data: 事件数据
            delay_ms: 延迟时间（毫秒）
        """
        # 创建一个定时器
        timer = QTimer(self)
        timer.setSingleShot(True)
        
        # 定义定时器回调函数
        def on_timeout():
            self.publish(event_name, data)
        
        # 连接信号和槽
        timer.timeout.connect(on_timeout)
        # 启动定时器
        timer.start(delay_ms)
