class CommandBase:
    """命令基类（支持撤销/重做）"""

    def __init__(self):
        """初始化命令"""
        pass

    def execute(self) -> dict:
        """执行命令"""
        raise NotImplementedError("Subclasses must implement execute method")

    def undo(self) -> dict:
        """撤销命令"""
        raise NotImplementedError("Subclasses must implement undo method")

    def redo(self) -> dict:
        """重做命令"""
        # 默认调用 execute 方法
        return self.execute()

    def get_description(self) -> str:
        """获取命令描述"""
        return "Command"


class LoadDataCommand(CommandBase):
    """加载数据命令"""

    def __init__(self, path: str, file_type: str):
        """
        初始化加载数据命令
        
        Args:
            path: 数据文件路径
            file_type: 文件类型
        """
        super().__init__()
        self.path = path
        self.file_type = file_type
        self.previous_data = None  # 用于撤销时恢复之前的数据

    def execute(self) -> dict:
        """执行命令"""
        # 这里需要调用核心引擎加载数据
        # 暂时返回模拟结果
        return {
            "success": True,
            "path": self.path,
            "file_type": self.file_type
        }

    def undo(self) -> dict:
        """撤销命令，恢复之前的数据状态"""
        # 这里需要恢复之前的数据
        # 暂时返回模拟结果
        return {
            "success": True,
            "message": "Data load undone"
        }

    def get_description(self) -> str:
        """获取命令描述"""
        return f"Load data from {self.path}"


class EditCellCommand(CommandBase):
    """编辑单元格命令"""

    def __init__(self, row: int, col: int, old_value, new_value):
        """
        初始化编辑单元格命令
        
        Args:
            row: 行索引
            col: 列索引
            old_value: 旧值
            new_value: 新值
        """
        super().__init__()
        self.row = row
        self.col = col
        self.old_value = old_value
        self.new_value = new_value

    def execute(self) -> dict:
        """执行命令"""
        # 这里需要更新单元格值
        # 暂时返回模拟结果
        return {
            "success": True,
            "row": self.row,
            "col": self.col,
            "new_value": self.new_value
        }

    def undo(self) -> dict:
        """撤销命令，恢复旧值"""
        # 这里需要恢复旧值
        # 暂时返回模拟结果
        return {
            "success": True,
            "row": self.row,
            "col": self.col,
            "old_value": self.old_value
        }

    def redo(self) -> dict:
        """重做命令，重新设置新值"""
        # 重新执行命令
        return self.execute()

    def get_description(self) -> str:
        """获取命令描述"""
        return f"Edit cell at ({self.row}, {self.col})"


class InsertColumnCommand(CommandBase):
    """插入列命令"""

    def __init__(self, position: int, name: str):
        """
        初始化插入列命令
        
        Args:
            position: 插入位置
            name: 列名
        """
        super().__init__()
        self.position = position
        self.name = name

    def execute(self) -> dict:
        """执行命令"""
        # 这里需要插入列
        # 暂时返回模拟结果
        return {
            "success": True,
            "position": self.position,
            "name": self.name
        }

    def undo(self) -> dict:
        """撤销命令，删除插入的列"""
        # 这里需要删除插入的列
        # 暂时返回模拟结果
        return {
            "success": True,
            "position": self.position,
            "message": "Column insertion undone"
        }

    def get_description(self) -> str:
        """获取命令描述"""
        return f"Insert column {self.name} at position {self.position}"


class InsertRowCommand(CommandBase):
    """插入行命令"""

    def __init__(self, position: int):
        """
        初始化插入行命令
        
        Args:
            position: 插入位置
        """
        super().__init__()
        self.position = position

    def execute(self) -> dict:
        """执行命令"""
        # 这里需要插入行
        # 暂时返回模拟结果
        return {
            "success": True,
            "position": self.position
        }

    def undo(self) -> dict:
        """撤销命令，删除插入的行"""
        # 这里需要删除插入的行
        # 暂时返回模拟结果
        return {
            "success": True,
            "position": self.position,
            "message": "Row insertion undone"
        }

    def get_description(self) -> str:
        """获取命令描述"""
        return f"Insert row at position {self.position}"


class DeleteColumnsCommand(CommandBase):
    """删除列命令"""

    def __init__(self, columns: list[int], data_backup):
        """
        初始化删除列命令
        
        Args:
            columns: 要删除的列索引列表
            data_backup: 数据备份，用于撤销时恢复
        """
        super().__init__()
        self.columns = columns
        self.data_backup = data_backup

    def execute(self) -> dict:
        """执行命令"""
        # 这里需要删除列
        # 暂时返回模拟结果
        return {
            "success": True,
            "columns": self.columns
        }

    def undo(self) -> dict:
        """撤销命令，从备份恢复"""
        # 这里需要从备份恢复
        # 暂时返回模拟结果
        return {
            "success": True,
            "columns": self.columns,
            "message": "Columns deletion undone"
        }

    def get_description(self) -> str:
        """获取命令描述"""
        return f"Delete columns {self.columns}"


class DeleteRowsCommand(CommandBase):
    """删除行命令"""

    def __init__(self, rows: list[int], data_backup):
        """
        初始化删除行命令
        
        Args:
            rows: 要删除的行索引列表
            data_backup: 数据备份，用于撤销时恢复
        """
        super().__init__()
        self.rows = rows
        self.data_backup = data_backup

    def execute(self) -> dict:
        """执行命令"""
        # 这里需要删除行
        # 暂时返回模拟结果
        return {
            "success": True,
            "rows": self.rows
        }

    def undo(self) -> dict:
        """撤销命令，从备份恢复"""
        # 这里需要从备份恢复
        # 暂时返回模拟结果
        return {
            "success": True,
            "rows": self.rows,
            "message": "Rows deletion undone"
        }

    def get_description(self) -> str:
        """获取命令描述"""
        return f"Delete rows {self.rows}"
