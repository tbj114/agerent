import json
import os
from typing import Any, Dict, Optional


class AppSettings:
    """应用设置管理"""

    def __init__(self, config_path: str = None):
        """初始化应用设置

        Args:
            config_path: 配置文件路径，默认为None
        """
        if config_path is None:
            # 默认配置路径
            config_path = os.path.join(
                os.path.dirname(__file__),
                "..", "..", "..", "configs", "app_settings.json"
            )
        self.config_path = config_path
        self._settings = self.load()

    def load(self) -> dict:
        """加载设置

        Returns:
            dict: 设置字典
        """
        # 确保配置目录存在
        config_dir = os.path.dirname(self.config_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        # 如果配置文件不存在，创建默认配置
        if not os.path.exists(self.config_path):
            default_settings = self._get_default_settings()
            self.save(default_settings)
            return default_settings

        # 加载配置文件
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            # 加载失败，返回默认配置
            print(f"Failed to load settings: {e}")
            return self._get_default_settings()

    def save(self, settings: dict) -> None:
        """保存设置

        Args:
            settings: 要保存的设置
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            self._settings = settings
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def get(self, key: str, default=None) -> Any:
        """获取设置值

        Args:
            key: 设置键
            default: 默认值

        Returns:
            Any: 设置值
        """
        keys = key.split('.')
        value = self._settings
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """设置设置值

        Args:
            key: 设置键
            value: 设置值
        """
        keys = key.split('.')
        settings = self._settings
        
        # 遍历键，直到倒数第二个键
        for k in keys[:-1]:
            if k not in settings:
                settings[k] = {}
            settings = settings[k]
        
        # 设置值
        settings[keys[-1]] = value
        
        # 保存设置
        self.save(self._settings)

    def reset_to_default(self) -> None:
        """重置为默认设置"""
        default_settings = self._get_default_settings()
        self.save(default_settings)

    def get_all(self) -> dict:
        """获取所有设置

        Returns:
            dict: 所有设置
        """
        return self._settings

    def _get_default_settings(self) -> dict:
        """获取默认设置

        Returns:
            dict: 默认设置
        """
        return {
            "general": {
                "language": "zh_CN",
                "theme": "light",
                "startup_action": "show_empty",
                "auto_save": True,
                "auto_save_interval": 5,
                "recent_files_count": 10,
                "decimal_places": 2
            },
            "appearance": {
                "font_size": 14,
                "table_font": "Consolas",
                "zoom_level": 100
            },
            "data": {
                "default_rows": 100,
                "default_cols": 100,
                "decimal_separator": ".",
                "thousand_separator": ","
            },
            "output": {
                "chart_format": "png",
                "chart_dpi": 150,
                "table_format": "markdown"
            },
            "performance": {
                "max_threads": 4,
                "virtual_scroll": True,
                "cache_size": 100
            }
        }
