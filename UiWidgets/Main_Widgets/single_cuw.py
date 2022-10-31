#!/usr/bin/env python3
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget
from settings import COMMAND, STATIC

qss_style_file = os.path.join(STATIC, 'Qss', 'single_cuw.qss')
with open(qss_style_file, 'r', encoding='U8') as f:
    singel_cuw_style = f.read()

class SingleUIWidget(QWidget):
    def __init__(self, parent=None):
        super(SingleUIWidget, self).__init__(parent=parent)
        self.setStyleSheet(singel_cuw_style)
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.setAlignment(Qt.AlignTop)
        self.setLayout(self._layout)
        self.setUI()

    def setUI(self):
        ## arguments layout
        arguments_layout = QHBoxLayout()
        # comamnd input
        command_layout = QVBoxLayout()
        #command_layout.setSpacing(0)
        # self.command_input_label = QLabel("指令输入")
        self.command_input_list = QTextEdit()
        if COMMAND is not None:
            self.command_input_list.append(COMMAND)
        # command_layout.addWidget(self.command_input_label)
        command_layout.addWidget(self.command_input_list)
        arguments_layout.addLayout(command_layout, stretch=5)
        #
        self.check_to_complex_command_ui = QPushButton("传递复杂命令")
        self._layout.addWidget(self.check_to_complex_command_ui)
        # start button
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)
        self.show_dialog_button = QPushButton("Show")
        self.start_button = QPushButton("Start Distributed")
        self.hide_dialog_button = QPushButton("Hide")
        button_layout.addWidget(self.show_dialog_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.hide_dialog_button)
        self._layout.addLayout(button_layout, stretch=1)
        #
        self.single_command_text = QTextEdit(self)
        self._layout.addWidget(self.single_command_text)
