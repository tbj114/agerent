class CommandHistory:
    """命令历史管理（撤销/重做栈）"""

    def __init__(self, max_size: int = 100):
        """初始化命令历史"""
        self.max_size = max_size
        self.undo_stack = []  # 撤销栈
        self.redo_stack = []  # 重做栈

    def push(self, command) -> None:
        """添加命令到历史栈"""
        # 清空重做栈
        self.redo_stack.clear()
        
        # 添加命令到撤销栈
        self.undo_stack.append(command)
        
        # 限制栈的大小
        if len(self.undo_stack) > self.max_size:
            self.undo_stack.pop(0)

    def undo(self) -> dict:
        """撤销上一个命令"""
        if not self.undo_stack:
            return {"success": False, "message": "Nothing to undo"}
        
        # 弹出撤销栈顶命令
        command = self.undo_stack.pop()
        
        # 执行撤销操作
        result = command.undo()
        
        # 将命令添加到重做栈
        self.redo_stack.append(command)
        
        return result

    def redo(self) -> dict:
        """重做上一个撤销的命令"""
        if not self.redo_stack:
            return {"success": False, "message": "Nothing to redo"}
        
        # 弹出重做栈顶命令
        command = self.redo_stack.pop()
        
        # 执行重做操作
        result = command.redo()
        
        # 将命令添加到撤销栈
        self.undo_stack.append(command)
        
        return result

    def can_undo(self) -> bool:
        """检查是否可以撤销"""
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        """检查是否可以重做"""
        return len(self.redo_stack) > 0

    def clear(self) -> None:
        """清空历史记录"""
        self.undo_stack.clear()
        self.redo_stack.clear()

    def get_history(self) -> list[str]:
        """获取历史记录列表"""
        # 构建历史记录描述列表
        history = []
        for command in reversed(self.undo_stack):
            history.append(command.get_description())
        
        # 添加分隔符
        if history and self.redo_stack:
            history.append("--- Redo Stack ---")
        
        # 添加重做栈中的命令
        for command in self.redo_stack:
            history.append(command.get_description())
        
        return history
