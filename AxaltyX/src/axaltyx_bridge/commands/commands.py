class CommandBase:
    """命令基类（支持撤销/重做）"""

    def __init__(self):
        pass

    def execute(self) -> dict:
        """执行命令"""
        raise NotImplementedError

    def undo(self) -> dict:
        """撤销命令"""
        raise NotImplementedError

    def redo(self) -> dict:
        """重做命令"""
        return self.execute()

    def get_description(self) -> str:
        """获取命令描述"""
        raise NotImplementedError


class LoadDataCommand(CommandBase):
    """加载数据命令"""

    def __init__(self, path: str, file_type: str):
        super().__init__()
        self.path = path
        self.file_type = file_type
        self.previous_data = None  # 保存之前的数据状态

    def execute(self) -> dict:
        """执行命令，返回 {success, data, ...}"""
        # 这里简化处理，实际应调用核心引擎加载数据
        # 保存之前的数据状态
        # 执行加载操作
        return {
            "success": True,
            "path": self.path,
            "file_type": self.file_type,
            "message": f"Loaded data from {self.path}"
        }

    def undo(self) -> dict:
        """撤销命令，恢复之前的数据状态"""
        # 这里简化处理，实际应恢复之前的数据状态
        return {
            "success": True,
            "message": "Undo load data operation",
            "restored_data": self.previous_data
        }

    def get_description(self) -> str:
        return f"Load data from {self.path}"


class EditCellCommand(CommandBase):
    """编辑单元格命令"""

    def __init__(self, row: int, col: int, old_value, new_value):
        super().__init__()
        self.row = row
        self.col = col
        self.old_value = old_value
        self.new_value = new_value

    def execute(self) -> dict:
        """执行命令"""
        # 这里简化处理，实际应更新单元格值
        return {
            "success": True,
            "row": self.row,
            "col": self.col,
            "new_value": self.new_value,
            "message": f"Edited cell ({self.row}, {self.col})"
        }

    def undo(self) -> dict:
        """撤销命令，恢复 old_value"""
        # 这里简化处理，实际应恢复旧值
        return {
            "success": True,
            "row": self.row,
            "col": self.col,
            "old_value": self.old_value,
            "message": f"Undo edit cell ({self.row}, {self.col})"
        }

    def get_description(self) -> str:
        return f"Edit cell ({self.row}, {self.col})"


class InsertColumnCommand(CommandBase):
    """插入列命令"""

    def __init__(self, position: int, name: str):
        super().__init__()
        self.position = position
        self.name = name

    def execute(self) -> dict:
        """执行命令"""
        # 这里简化处理，实际应插入列
        return {
            "success": True,
            "position": self.position,
            "name": self.name,
            "message": f"Inserted column '{self.name}' at position {self.position}"
        }

    def undo(self) -> dict:
        """撤销命令，删除插入的列"""
        # 这里简化处理，实际应删除插入的列
        return {
            "success": True,
            "position": self.position,
            "message": f"Undo insert column '{self.name}'"
        }

    def get_description(self) -> str:
        return f"Insert column '{self.name}'"


class InsertRowCommand(CommandBase):
    """插入行命令"""

    def __init__(self, position: int):
        super().__init__()
        self.position = position

    def execute(self) -> dict:
        """执行命令"""
        # 这里简化处理，实际应插入行
        return {
            "success": True,
            "position": self.position,
            "message": f"Inserted row at position {self.position}"
        }

    def undo(self) -> dict:
        """撤销命令，删除插入的行"""
        # 这里简化处理，实际应删除插入的行
        return {
            "success": True,
            "position": self.position,
            "message": f"Undo insert row at position {self.position}"
        }

    def get_description(self) -> str:
        return f"Insert row at position {self.position}"


class DeleteColumnsCommand(CommandBase):
    """删除列命令"""

    def __init__(self, columns: list[int], data_backup):
        super().__init__()
        self.columns = columns
        self.data_backup = data_backup  # 备份数据，用于撤销操作

    def execute(self) -> dict:
        """执行命令"""
        # 这里简化处理，实际应删除列
        return {
            "success": True,
            "columns": self.columns,
            "message": f"Deleted columns {self.columns}"
        }

    def undo(self) -> dict:
        """撤销命令，从备份恢复"""
        # 这里简化处理，实际应从备份恢复列
        return {
            "success": True,
            "columns": self.columns,
            "message": f"Undo delete columns {self.columns}",
            "restored_data": self.data_backup
        }

    def get_description(self) -> str:
        return f"Delete columns {self.columns}"


class DeleteRowsCommand(CommandBase):
    """删除行命令"""

    def __init__(self, rows: list[int], data_backup):
        super().__init__()
        self.rows = rows
        self.data_backup = data_backup  # 备份数据，用于撤销操作

    def execute(self) -> dict:
        """执行命令"""
        # 这里简化处理，实际应删除行
        return {
            "success": True,
            "rows": self.rows,
            "message": f"Deleted rows {self.rows}"
        }

    def undo(self) -> dict:
        """撤销命令，从备份恢复"""
        # 这里简化处理，实际应从备份恢复行
        return {
            "success": True,
            "rows": self.rows,
            "message": f"Undo delete rows {self.rows}",
            "restored_data": self.data_backup
        }

    def get_description(self) -> str:
        return f"Delete rows {self.rows}"
