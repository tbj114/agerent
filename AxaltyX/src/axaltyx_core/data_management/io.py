
import os
import pandas as pd
import pyreadstat
import json
from typing import Dict, Any, List, Union, Optional


def load_csv(
    path: str,
    encoding: str = "utf-8",
    delimiter: str = ",",
    header: bool = True,
    na_values: list = None
) -> dict:
    """
    加载CSV文件
    
    Args:
        path: CSV文件绝对路径
        encoding: 文件编码（utf-8/gbk/latin1）
        delimiter: 分隔符
        header: 首行是否为表头
        na_values: 自定义缺失值标记列表
    
    Returns:
        包含数据和元数据的字典
    """
    try:
        # 读取文件
        data = pd.read_csv(
            path,
            encoding=encoding,
            delimiter=delimiter,
            header=0 if header else None,
            na_values=na_values
        )
        
        # 计算缺失值总数
        missing_count = data.isnull().sum().sum()
        
        # 获取文件大小
        file_size = os.path.getsize(path)
        
        # 生成列名（如果没有表头）
        if not header:
            columns = [f"VAR{str(i+1).zfill(5)}" for i in range(data.shape[1])]
            data.columns = columns
        else:
            columns = data.columns.tolist()
        
        return {
            "success": True,
            "results": {
                "data": data,
                "columns": columns,
                "dtypes": data.dtypes.astype(str).to_dict(),
                "shape": data.shape,
                "missing_count": missing_count,
                "file_size": file_size
            },
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }


def load_excel(
    path: str,
    sheet_name: Union[str, int, list] = 0,
    header: bool = True,
    na_values: list = None
) -> dict:
    """
    加载Excel文件
    
    Args:
        path: Excel文件路径
        sheet_name: 工作表名或索引
        header: 首行是否为表头
        na_values: 缺失值标记
    
    Returns:
        包含数据和元数据的字典
    """
    try:
        # 读取文件
        data = pd.read_excel(
            path,
            sheet_name=sheet_name,
            header=0 if header else None,
            na_values=na_values
        )
        
        results = {}
        
        if isinstance(data, dict):
            # 多表情况
            results["sheets"] = data
            # 取第一个表的信息
            first_sheet_name = list(data.keys())[0]
            first_sheet = data[first_sheet_name]
            columns = first_sheet.columns.tolist() if header else [f"VAR{str(i+1).zfill(5)}" for i in range(first_sheet.shape[1])]
            dtypes = first_sheet.dtypes.astype(str).to_dict()
            shape = first_sheet.shape
            missing_count = sum(df.isnull().sum().sum() for df in data.values())
        else:
            # 单表情况
            columns = data.columns.tolist() if header else [f"VAR{str(i+1).zfill(5)}" for i in range(data.shape[1])]
            dtypes = data.dtypes.astype(str).to_dict()
            shape = data.shape
            missing_count = data.isnull().sum().sum()
            results["data"] = data
        
        file_size = os.path.getsize(path)
        
        results.update({
            "columns": columns,
            "dtypes": dtypes,
            "shape": shape,
            "missing_count": missing_count,
            "file_size": file_size
        })
        
        return {
            "success": True,
            "results": results,
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }


def load_sav(path: str) -> dict:
    """
    加载SPSS .sav文件
    
    Args:
        path: SPSS .sav文件路径
    
    Returns:
        包含数据和元数据的字典
    """
    try:
        # 使用pyreadstat读取sav文件
        data, meta = pyreadstat.read_sav(path)
        
        # 提取元数据
        value_labels = meta.variable_value_labels
        variable_labels = meta.column_names_to_labels
        missing_values = meta.missing_values
        measure = meta.measure
        file_label = meta.file_label
        
        return {
            "success": True,
            "results": {
                "data": data,
                "columns": data.columns.tolist(),
                "dtypes": data.dtypes.astype(str).to_dict(),
                "shape": data.shape,
                "value_labels": value_labels,
                "variable_labels": variable_labels,
                "missing_values": missing_values,
                "measure": measure,
                "file_label": file_label
            },
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }


def load_dta(path: str) -> dict:
    """
    加载Stata .dta文件
    
    Args:
        path: Stata .dta文件路径
    
    Returns:
        包含数据和元数据的字典
    """
    try:
        # 使用pyreadstat读取dta文件
        data, meta = pyreadstat.read_dta(path)
        
        # 提取元数据
        value_labels = meta.variable_value_labels
        variable_labels = meta.column_names_to_labels
        missing_values = meta.missing_values
        measure = meta.measure
        file_label = meta.file_label
        
        return {
            "success": True,
            "results": {
                "data": data,
                "columns": data.columns.tolist(),
                "dtypes": data.dtypes.astype(str).to_dict(),
                "shape": data.shape,
                "value_labels": value_labels,
                "variable_labels": variable_labels,
                "missing_values": missing_values,
                "measure": measure,
                "file_label": file_label
            },
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }


def load_json(path: str, encoding: str = "utf-8", orient: str = "records") -> dict:
    """
    加载JSON文件
    
    Args:
        path: JSON文件路径
        encoding: 编码
        orient: 数据方向（records/columns/index）
    
    Returns:
        包含数据和元数据的字典
    """
    try:
        # 读取JSON文件
        with open(path, "r", encoding=encoding) as f:
            json_data = json.load(f)
        
        # 转换为DataFrame
        data = pd.DataFrame(json_data, orient=orient)
        
        # 计算缺失值总数
        missing_count = data.isnull().sum().sum()
        
        # 获取文件大小
        file_size = os.path.getsize(path)
        
        return {
            "success": True,
            "results": {
                "data": data,
                "columns": data.columns.tolist(),
                "dtypes": data.dtypes.astype(str).to_dict(),
                "shape": data.shape,
                "missing_count": missing_count,
                "file_size": file_size
            },
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }


def save_csv(
    data: pd.DataFrame,
    path: str,
    encoding: str = "utf-8",
    delimiter: str = ",",
    index: bool = False,
    na_rep: str = ""
) -> dict:
    """
    保存CSV文件
    
    Args:
        data: 数据DataFrame
        path: 保存路径
        encoding: 编码
        delimiter: 分隔符
        index: 是否保存索引
        na_rep: 缺失值表示
    
    Returns:
        保存结果
    """
    try:
        # 保存文件
        data.to_csv(
            path,
            encoding=encoding,
            sep=delimiter,
            index=index,
            na_rep=na_rep
        )
        
        # 获取文件大小
        file_size = os.path.getsize(path)
        
        return {
            "success": True,
            "results": {
                "path": path,
                "rows": data.shape[0],
                "columns": data.shape[1],
                "file_size": file_size
            },
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }


def save_excel(
    data: pd.DataFrame,
    path: str,
    sheet_name: str = "Sheet1",
    index: bool = False
) -> dict:
    """
    保存Excel文件
    
    Args:
        data: 数据DataFrame
        path: 保存路径
        sheet_name: 工作表名
        index: 是否保存索引
    
    Returns:
        保存结果
    """
    try:
        # 保存文件
        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            data.to_excel(writer, sheet_name=sheet_name, index=index)
        
        # 获取文件大小
        file_size = os.path.getsize(path)
        
        return {
            "success": True,
            "results": {
                "path": path,
                "rows": data.shape[0],
                "columns": data.shape[1],
                "file_size": file_size
            },
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }


def save_sav(
    data: pd.DataFrame,
    path: str,
    variable_labels: dict = None,
    value_labels: dict = None
) -> dict:
    """
    保存SPSS .sav文件
    
    Args:
        data: 数据DataFrame
        path: 保存路径
        variable_labels: 变量标签
        value_labels: 值标签
    
    Returns:
        保存结果
    """
    try:
        # 保存文件
        pyreadstat.write_sav(
            data,
            path,
            variable_labels=variable_labels,
            value_labels=value_labels
        )
        
        # 获取文件大小
        file_size = os.path.getsize(path)
        
        return {
            "success": True,
            "results": {
                "path": path,
                "rows": data.shape[0],
                "columns": data.shape[1],
                "file_size": file_size
            },
            "warnings": [],
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }

