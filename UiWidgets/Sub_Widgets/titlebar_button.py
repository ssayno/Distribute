#!/usr/bin/env python3

from PyQt5.QtWidgets import QPushButton


class TitlebarButton(QPushButton):
    def __init__(self, parent=None):
        super(TitlebarButton, self).__init__(parent=parent)
        self.setFixedHeight(self.parent().height())
        self.setFixedWidth(40)
        self.setStyleSheet(
            '''
            QPushButton{
            border-radius: 0;
            }
            '''
        )
