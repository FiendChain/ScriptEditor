from PySide2 import QtGui, QtCore, QtWidgets
from .Tag import Tag

class LabelView(Tag):
    def __init__(self, label, browser):
        super().__init__(left=False, browser=browser)
        self._label = label
        self.browser.addLabel(self._label.name, self)
        self.calculateRect()

    @property
    def tag(self):
        return self._label.name

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)