#!/usr/bin/env python3
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QSizePolicy, QWidget, QPushButton
from UiWidgets.Sub_Widgets.titlebar_button import TitlebarButton
from settings import STATIC

title_bar_style = '''\
QLabel{
font: 24px;
qproperty-alignment: AlignCenter;
padding: 10px 0;
color: black;
}
'''

class Titlebar(QWidget):
    def __init__(self, parent=None):
        super(Titlebar, self).__init__(parent=parent)
        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(0)
        self.title_layout.setAlignment(Qt.AlignRight)
        # set size policy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(self.title_layout)
        # add static path
        self.icon_path = os.path.join(STATIC, 'Icons')
        #
        self.setFixedHeight(45)
        # add title bar button and connect their signal with function
        self.add_title_bar_button()
        self.setStyleSheet(title_bar_style)

    def add_title_bar_button(self):
        self.info_label = QLabel("复杂命令输入")
        self.minimum_button = TitlebarButton(self)
        self.minimum_button.setIcon(QIcon(os.path.join(self.icon_path, 'icons8-minimize-window-16.png')))
        self.maximum_button = TitlebarButton(self)
        self.maximum_button.setIcon(QIcon(os.path.join(self.icon_path, 'icons8-maximize-window-16.png')))
        self.close_button = TitlebarButton(self)
        self.close_button.setIcon(QIcon(os.path.join(self.icon_path, 'icons8-close-50.png')))
        # add button
        self.title_layout.addWidget(self.info_label)
        self.title_layout.addWidget(self.minimum_button, stretch=1)
        self.title_layout.addWidget(self.maximum_button, stretch=1)
        self.title_layout.addWidget(self.close_button, stretch=1)
