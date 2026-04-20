class CommandHistory:
    """命令历史管理（撤销/重做栈）"""

    def __init__(self, max_size: int = 100):
        """
        初始化命令历史
        
        Args:
            max_size: 历史记录的最大长度
        """
        self.max_size = max_size
        self.undo_stack = []  # 撤销栈
        self.redo_stack = []  # 重做栈

    def push(self, command) -> None:
        """
        推送命令到历史记录
        
        Args:
            command: 命令对象
        """
        # 执行命令
        command.execute()
        
        # 将命令添加到撤销栈
        self.undo_stack.append(command)
        
        # 清空重做栈
        self.redo_stack.clear()
        
        # 限制栈的大小
        if len(self.undo_stack) > self.max_size:
            self.undo_stack.pop(0)

    def undo(self) -> dict:
        """
        执行撤销操作
        
        Returns:
            撤销结果
        """
        if not self.undo_stack:
            return {"success": False, "message": "No commands to undo"}
        
        # 从撤销栈中弹出命令
        command = self.undo_stack.pop()
        
        # 执行撤销
        result = command.undo()
        
        # 将命令添加到重做栈
        self.redo_stack.append(command)
        
        return result

    def redo(self) -> dict:
        """
        执行重做操作
        
        Returns:
            重做结果
        """
        if not self.redo_stack:
            return {"success": False, "message": "No commands to redo"}
        
        # 从重做栈中弹出命令
        command = self.redo_stack.pop()
        
        # 执行重做
        result = command.redo()
        
        # 将命令添加到撤销栈
        self.undo_stack.append(command)
        
        return result

    def can_undo(self) -> bool:
        """
        检查是否可以执行撤销操作
        
        Returns:
            是否可以撤销
        """
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        """
        检查是否可以执行重做操作
        
        Returns:
            是否可以重做
        """
        return len(self.redo_stack) > 0

    def clear(self) -> None:
        """
        清空历史记录
        """
        self.undo_stack.clear()
        self.redo_stack.clear()

    def get_history(self) -> list[str]:
        """
        获取历史记录列表
        
        Returns:
            历史记录描述列表
        """
        return [cmd.get_description() for cmd in reversed(self.undo_stack)]
