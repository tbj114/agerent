from PyQt6.QtWidgets import QWidget, QTabWidget, QTabBar, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import pyqtSignal, Qt

class AxaltyXTabWidget(QWidget):
    """自定义标签页组件"""

    sig_tab_changed = pyqtSignal(str)
    sig_tab_close_requested = pyqtSignal(str)
    sig_tab_moved = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        self.tab_widget.tabBar().tabMoved.connect(self._on_tab_moved)

        # 存储 tab_id 与 index 的映射
        self.tab_id_map = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tab_widget)

    def add_tab(self, widget: QWidget, tab_id: str, label: str, closable: bool = False) -> int:
        """添加标签页

        Args:
            widget: 标签页内容
            tab_id: 标签页ID
            label: 标签页标题
            closable: 是否可关闭

        Returns:
            int: 标签页索引
        """
        index = self.tab_widget.addTab(widget, label)
        self.tab_id_map[tab_id] = index
        # 设置标签页是否可关闭
        if not closable:
            self.tab_widget.tabBar().setTabButton(index, QTabBar.ButtonPosition.RightSide, None)
        return index

    def remove_tab(self, tab_id: str) -> None:
        """移除标签页

        Args:
            tab_id: 标签页ID
        """
        if tab_id in self.tab_id_map:
            index = self.tab_id_map[tab_id]
            self.tab_widget.removeTab(index)
            del self.tab_id_map[tab_id]
            # 更新映射
            new_map = {}
            for tid, idx in self.tab_id_map.items():
                if idx > index:
                    new_map[tid] = idx - 1
                else:
                    new_map[tid] = idx
            self.tab_id_map = new_map

    def set_tab_label(self, tab_id: str, label: str) -> None:
        """设置标签页标题

        Args:
            tab_id: 标签页ID
            label: 新标题
        """
        if tab_id in self.tab_id_map:
            index = self.tab_id_map[tab_id]
            self.tab_widget.setTabText(index, label)

    def get_current_tab_id(self) -> str:
        """获取当前标签页ID

        Returns:
            str: 当前标签页ID
        """
        current_index = self.tab_widget.currentIndex()
        for tab_id, index in self.tab_id_map.items():
            if index == current_index:
                return tab_id
        return None

    def set_current_tab(self, tab_id: str) -> None:
        """设置当前标签页

        Args:
            tab_id: 标签页ID
        """
        if tab_id in self.tab_id_map:
            index = self.tab_id_map[tab_id]
            self.tab_widget.setCurrentIndex(index)

    def get_all_tab_ids(self) -> list[str]:
        """获取所有标签页ID

        Returns:
            list[str]: 标签页ID列表
        """
        return list(self.tab_id_map.keys())

    def set_tab_icon(self, tab_id: str, icon: QIcon) -> None:
        """设置标签页图标

        Args:
            tab_id: 标签页ID
            icon: 图标
        """
        if tab_id in self.tab_id_map:
            index = self.tab_id_map[tab_id]
            self.tab_widget.setTabIcon(index, icon)

    def _on_tab_close_requested(self, index: int):
        """标签页关闭请求处理

        Args:
            index: 标签页索引
        """
        for tab_id, idx in self.tab_id_map.items():
            if idx == index:
                self.sig_tab_close_requested.emit(tab_id)
                break

    def _on_tab_changed(self, index: int):
        """标签页切换处理

        Args:
            index: 标签页索引
        """
        for tab_id, idx in self.tab_id_map.items():
            if idx == index:
                self.sig_tab_changed.emit(tab_id)
                break

    def _on_tab_moved(self, from_index: int, to_index: int):
        """标签页移动处理

        Args:
            from_index: 源索引
            to_index: 目标索引
        """
        self.sig_tab_moved.emit(from_index, to_index)
        # 更新映射
        new_map = {}
        for tab_id, idx in self.tab_id_map.items():
            if idx == from_index:
                new_map[tab_id] = to_index
            elif idx > from_index and idx < to_index:
                new_map[tab_id] = idx - 1
            elif idx < from_index and idx > to_index:
                new_map[tab_id] = idx + 1
            else:
                new_map[tab_id] = idx
        self.tab_id_map = new_map
