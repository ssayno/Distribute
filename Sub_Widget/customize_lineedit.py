#!/usr/bin/env python3
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QFocusEvent
from PyQt5.QtWidgets import QLineEdit


class Customize_QLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(Customize_QLineEdit, self).__init__(parent=parent)

    def focusInEvent(self, a0: QFocusEvent) -> None:
        self.selectAll()
        return super().focusInEvent(a0)
