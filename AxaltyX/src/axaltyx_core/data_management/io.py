
import os
import pandas as pd
import pyreadstat
from typing import Dict, Any, List, Optional, Union


def load_csv(
    path: str,
    encoding: str = "utf-8",
    delimiter: str = ",",
    header: bool = True,
    na_values: list = None
) -> dict:
    """加载 CSV 文件"""
    try:
        data = pd.read_csv(
            path,
            encoding=encoding,
            delimiter=delimiter,
            header=0 if header else None,
            na_values=na_values
        )
        
        if not header:
            data.columns = [f"VAR{str(i+1).zfill(5)}" for i in range(len(data.columns))]
        
        columns = list(data.columns)
        dtypes = data.dtypes.astype(str).to_dict()
        shape = data.shape
        missing_count = data.isnull().sum().sum()
        file_size = os.path.getsize(path)
        
        return {
            "success": True,
            "results": {
                "data": data,
                "columns": columns,
                "dtypes": dtypes,
                "shape": shape,
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
    """加载 Excel 文件"""
    try:
        data = pd.read_excel(
            path,
            sheet_name=sheet_name,
            header=0 if header else None,
            na_values=na_values
        )
        
        if isinstance(data, dict):
            # 多表情况
            sheets = {}
            all_columns = []
            all_missing = 0
            
            for sheet, df in data.items():
                if not header:
                    df.columns = [f"VAR{str(i+1).zfill(5)}" for i in range(len(df.columns))]
                sheets[sheet] = df
                all_columns.extend(list(df.columns))
                all_missing += df.isnull().sum().sum()
            
            return {
                "success": True,
                "results": {
                    "sheets": sheets,
                    "columns": list(set(all_columns)),
                    "file_size": os.path.getsize(path)
                },
                "warnings": [],
                "error": None
            }
        else:
            # 单表情况
            if not header:
                data.columns = [f"VAR{str(i+1).zfill(5)}" for i in range(len(data.columns))]
            
            columns = list(data.columns)
            dtypes = data.dtypes.astype(str).to_dict()
            shape = data.shape
            missing_count = data.isnull().sum().sum()
            file_size = os.path.getsize(path)
            
            return {
                "success": True,
                "results": {
                    "data": data,
                    "columns": columns,
                    "dtypes": dtypes,
                    "shape": shape,
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


def load_sav(path: str) -> dict:
    """加载 SPSS .sav 文件"""
    try:
        data, meta = pyreadstat.read_sav(path)
        
        columns = list(data.columns)
        dtypes = data.dtypes.astype(str).to_dict()
        shape = data.shape
        value_labels = meta.value_labels
        variable_labels = meta.column_labels
        missing_values = meta.missing_values
        measure = meta.measure
        file_label = meta.file_label
        
        return {
            "success": True,
            "results": {
                "data": data,
                "columns": columns,
                "dtypes": dtypes,
                "shape": shape,
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
    """加载 Stata .dta 文件"""
    try:
        data, meta = pyreadstat.read_dta(path)
        
        columns = list(data.columns)
        dtypes = data.dtypes.astype(str).to_dict()
        shape = data.shape
        value_labels = meta.value_labels
        variable_labels = meta.column_labels
        missing_values = meta.missing_values
        measure = meta.measure
        file_label = meta.file_label
        
        return {
            "success": True,
            "results": {
                "data": data,
                "columns": columns,
                "dtypes": dtypes,
                "shape": shape,
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
    """加载 JSON 文件"""
    try:
        data = pd.read_json(
            path,
            encoding=encoding,
            orient=orient
        )
        
        columns = list(data.columns)
        dtypes = data.dtypes.astype(str).to_dict()
        shape = data.shape
        missing_count = data.isnull().sum().sum()
        file_size = os.path.getsize(path)
        
        return {
            "success": True,
            "results": {
                "data": data,
                "columns": columns,
                "dtypes": dtypes,
                "shape": shape,
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
    """保存为 CSV 文件"""
    try:
        data.to_csv(
            path,
            encoding=encoding,
            delimiter=delimiter,
            index=index,
            na_rep=na_rep
        )
        
        file_size = os.path.getsize(path)
        
        return {
            "success": True,
            "results": {
                "path": path,
                "rows": len(data),
                "columns": len(data.columns),
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
    """保存为 Excel 文件"""
    try:
        with pd.ExcelWriter(path) as writer:
            data.to_excel(writer, sheet_name=sheet_name, index=index)
        
        file_size = os.path.getsize(path)
        
        return {
            "success": True,
            "results": {
                "path": path,
                "rows": len(data),
                "columns": len(data.columns),
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
    """保存为 SPSS .sav 文件"""
    try:
        pyreadstat.write_sav(
            data,
            path,
            variable_labels=variable_labels,
            value_labels=value_labels
        )
        
        file_size = os.path.getsize(path)
        
        return {
            "success": True,
            "results": {
                "path": path,
                "rows": len(data),
                "columns": len(data.columns),
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
