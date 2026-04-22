
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


class I18nManager:
    """国际化管理器，负责加载语言文件和提供文本翻译功能"""

    def __init__(self, locales_dir: Optional[str] = None):
        """
        初始化国际化管理器

        Args:
            locales_dir: 语言文件目录的路径，默认为当前文件所在目录的 locales 子目录
        """
        if locales_dir is None:
            # 默认使用当前文件所在目录的 locales 子目录
            current_dir = Path(__file__).parent
            self.locales_dir = current_dir / "locales"
        else:
            self.locales_dir = Path(locales_dir)

        self.current_language = "zh_CN"  # 默认使用简体中文
        self.translations: Dict[str, Any] = {}
        self.fallback_language = "en_US"  # 默认回退语言为英语
        self._load_available_languages()
        self.load_language(self.current_language)

    def _load_available_languages(self) -> None:
        """加载所有可用的语言文件"""
        self.available_languages = []

        if not self.locales_dir.exists():
            return

        for lang_file in self.locales_dir.glob("*.json"):
            try:
                with open(lang_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "meta" in data and "language" in data["meta"]:
                        self.available_languages.append(
                            {
                                "code": data["meta"]["language"],
                                "name": data["meta"].get("language_name", data["meta"]["language"]),
                                "version": data["meta"].get("version", ""),
                            }
                        )
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load language file {lang_file}: {e}")

    def load_language(self, lang_code: str) -> None:
        """
        加载指定的语言文件

        Args:
            lang_code: 语言代码，如 'zh_CN', 'en_US'
        """
        # 防止无限递归
        if lang_code == self.current_language:
            return
            
        lang_file = self.locales_dir / f"{lang_code}.json"

        if lang_file.exists():
            try:
                with open(lang_file, "r", encoding="utf-8") as f:
                    self.translations = json.load(f)
                    self.current_language = lang_code
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading language file {lang_file}: {e}")
                # 加载失败时尝试回退语言
                if lang_code != self.fallback_language:
                    print(f"Falling back to {self.fallback_language}")
                    # 防止无限递归
                    if self.fallback_language != self.current_language:
                        self.load_language(self.fallback_language)
        else:
            print(f"Warning: Language file not found: {lang_file}")
            if lang_code != self.fallback_language:
                # 防止无限递归
                if self.fallback_language != self.current_language:
                    self.load_language(self.fallback_language)

    def get_text(self, key: str, **kwargs) -> str:
        """
        获取指定键的翻译文本

        Args:
            key: 翻译键，格式为 'section.subsection.key'
            **kwargs: 用于替换占位符的参数

        Returns:
            翻译后的文本，如果找不到则返回键本身
        """
        keys = key.split(".")
        value = self.translations

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                # 如果当前语言找不到，尝试回退语言
                if self.current_language != self.fallback_language:
                    return self._get_fallback_text(key, **kwargs)
                return key

        if isinstance(value, str):
            try:
                return value.format(**kwargs)
            except (KeyError, IndexError) as e:
                print(f"Warning: Placeholder error for key {key}: {e}")
                return value
        return key

    def _get_fallback_text(self, key: str, **kwargs) -> str:
        """从回退语言中获取文本"""
        # 临时保存当前翻译
        current_translations = self.translations
        current_lang = self.current_language

        # 加载回退语言
        self.load_language(self.fallback_language)
        fallback_value = self.translations

        keys = key.split(".")
        for k in keys:
            if isinstance(fallback_value, dict) and k in fallback_value:
                fallback_value = fallback_value[k]
            else:
                # 回退语言也找不到，返回键本身
                self.translations = current_translations
                self.current_language = current_lang
                return key

        # 恢复当前语言
        self.translations = current_translations
        self.current_language = current_lang

        if isinstance(fallback_value, str):
            try:
                return fallback_value.format(**kwargs)
            except (KeyError, IndexError) as e:
                print(f"Warning: Placeholder error for key {key} (fallback): {e}")
                return fallback_value
        return key

    def get_current_language(self) -> str:
        """
        获取当前语言代码

        Returns:
            当前语言代码
        """
        return self.current_language

    def get_available_languages(self) -> List[Dict[str, str]]:
        """
        获取所有可用语言的列表

        Returns:
            语言列表，每个元素包含 'code', 'name', 'version'
        """
        return self.available_languages

    def set_language(self, lang_code: str) -> None:
        """
        设置当前语言

        Args:
            lang_code: 语言代码
        """
        if lang_code != self.current_language:
            self.load_language(lang_code)

    def register_fallback(self, lang_code: str) -> None:
        """
        注册回退语言

        Args:
            lang_code: 回退语言代码
        """
        self.fallback_language = lang_code

