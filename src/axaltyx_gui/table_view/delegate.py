from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import QStyledItemDelegate, QLineEdit

class DataTableDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setFrame(False)
        return editor
    
    def setEditorData(self, editor, index):
        value = index.data(Qt.ItemDataRole.EditRole)
        if value:
            editor.setText(str(value))
        else:
            editor.setText("")
    
    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, Qt.ItemDataRole.EditRole)
    
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class HeaderDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setFrame(False)
        return editor
    
    def setEditorData(self, editor, index):
        value = index.data(Qt.ItemDataRole.EditRole)
        if value:
            editor.setText(str(value))
        else:
            editor.setText("")
    
    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setHeaderData(index.column(), Qt.Orientation.Horizontal, value, Qt.ItemDataRole.EditRole)
    
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)