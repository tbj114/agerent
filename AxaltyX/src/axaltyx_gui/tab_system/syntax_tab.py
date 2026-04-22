from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import pyqtSignal, Qt, QRegularExpression

class SyntaxHighlighter(QSyntaxHighlighter):
    """语法高亮器"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlight_rules = []

        # 关键字格式
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(128, 0, 128))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = ["DATA", "ANALYZE", "GRAPH", "SAVE", "LOAD", "SELECT", "SORT", "COMPUTE", "RECODE", "IF", "ELSE", "ENDIF", "DO", "ENDDO", "LOOP", "ENDLOOP", "BY", "WITH", "BY", "CASE", "VARIABLE", "VALUE", "LABEL", "MISSING", "WEIGHT", "SPLIT", "AGGREGATE", "MERGE", "TRANSPOSE"]
        for keyword in keywords:
            pattern = QRegularExpression(f"\\b{keyword}\\b")
            self.highlight_rules.append((pattern, keyword_format))

        # 注释格式
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(0, 128, 0))
        pattern = QRegularExpression("/\*[\\s\\S]*?\*/|//.*")
        self.highlight_rules.append((pattern, comment_format))

        # 字符串格式
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(163, 21, 21))
        pattern = QRegularExpression('"[^"]*"')
        self.highlight_rules.append((pattern, string_format))

    def highlightBlock(self, text):
        """高亮文本块"""
        for pattern, format in self.highlight_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class SyntaxTab(QWidget):
    """语法视图标签页"""

    sig_execute_syntax = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.text_edit = QTextEdit()
        self.text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.text_edit.setFontFamily("Consolas, Source Code Pro, Courier New, monospace")
        self.text_edit.setFontPointSize(13)

        # 添加语法高亮
        self.highlighter = SyntaxHighlighter(self.text_edit.document())

        # 执行按钮
        self.execute_all_button = QPushButton("执行全部")
        self.execute_all_button.clicked.connect(self.execute_all)

        self.execute_selection_button = QPushButton("执行选中")
        self.execute_selection_button.clicked.connect(self.execute_selection)

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.execute_all_button)
        button_layout.addWidget(self.execute_selection_button)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.text_edit)

    def get_syntax(self) -> str:
        """获取语法文本

        Returns:
            str: 语法文本
        """
        return self.text_edit.toPlainText()

    def set_syntax(self, text: str) -> None:
        """设置语法文本

        Args:
            text: 语法文本
        """
        self.text_edit.setPlainText(text)

    def insert_syntax(self, text: str) -> None:
        """插入语法文本

        Args:
            text: 要插入的语法文本
        """
        cursor = self.text_edit.textCursor()
        cursor.insertText(text)

    def execute_all(self) -> None:
        """执行全部语法"""
        syntax = self.get_syntax()
        if syntax:
            self.sig_execute_syntax.emit(syntax)

    def execute_selection(self) -> None:
        """执行选中的语法"""
        selected_text = self.text_edit.textCursor().selectedText()
        if selected_text:
            self.sig_execute_syntax.emit(selected_text)
        else:
            # 如果没有选中，执行全部
            self.execute_all()
