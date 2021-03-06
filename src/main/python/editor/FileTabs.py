from PySide2 import QtGui, QtCore, QtWidgets
from .graphview import GraphView

import os

class FileTabs(QtWidgets.QTabWidget):
    def __init__(self, editor, parent):
        super().__init__(parent=parent)
        self.editor = editor
        self.tabs = self # TODO: Decouple into a widget as composite
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.openedFiles = {}

        self.currentChanged.connect(self._onTabChange)
        self.tabCloseRequested.connect(self._onTabClose)

    def openLabels(self, labels, filepath):
        filepath = os.path.normpath(filepath)
        if filepath in self.openedFiles:
            widget = self.openedFiles.get(filepath)
            index = self.tabs.indexOf(widget)
            self.tabs.setCurrentIndex(index)
            return

        graphView = GraphView(editor=self.editor, parent=self.tabs)
        graphView.open(labels)
        title = os.path.basename(filepath)
        index = self.tabs.addTab(graphView, title)
        self.openedFiles.setdefault(filepath, graphView)
        self.tabs.setCurrentIndex(index)
    
    def getCurrentGraphScene(self):
        index = self.tabs.currentIndex()
        graphView = self.tabs.widget(index)
        return graphView

    def _onTabChange(self, index=None):
        self.editor.updateGraphScene()
    
    def _onTabClose(self, index):
        widget = self.tabs.widget(index)
        self.tabs.removeTab(index)
        key = None
        for _key, _widget in self.openedFiles.items():
            if _widget == widget:
                key = _key
                break
        if key is not None:
            self.openedFiles.pop(key)
            self.editor.updateGraphScene()