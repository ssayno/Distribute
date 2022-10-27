#!/usr/bin/env python3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QTextEdit, QVBoxLayout, QWidget
from .titlebar import Titlebar
from settings import DELIMITER, TOKEN_SIZE


class UIWidget(QWidget):
    def __init__(self, parent=None):
        super(UIWidget, self).__init__(parent=parent)
        self._layout = QVBoxLayout()
        self.title_bar = Titlebar(self)
        self._layout.addWidget(self.title_bar)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)
        self.setUI()

    def setUI(self):
        ## arguments layout
        arguments_layout = QHBoxLayout()
        # comamnd input
        command_layout = QVBoxLayout()
        command_layout.setSpacing(0)
        self.command_input_label = QLabel("指令输入")
        self.command_input_label.setAlignment(Qt.AlignCenter)
        self.command_input_list = QTextEdit()
        command_layout.addWidget(self.command_input_label)
        command_layout.addWidget(self.command_input_list)
        arguments_layout.addLayout(command_layout, stretch= 3)
        # delimiter select
        td_layout = QVBoxLayout()
        td_layout.setSpacing(0)
        self.delimiter_label = QLabel("Delimiter")
        self.delimiter_label.setAlignment(Qt.AlignCenter)
        self.delimiter_lineedit = QLineEdit(DELIMITER)
        self.delimiter_lineedit.setAlignment(Qt.AlignCenter)
        td_layout.addWidget(self.delimiter_label)
        td_layout.addWidget(self.delimiter_lineedit)
        arguments_layout.addLayout(td_layout, stretch=1)
        # Token size
        token_layout = QVBoxLayout()
        token_layout.setSpacing(0)
        self.token_size_label = QLabel("Token Size")
        self.token_size_label.setAlignment(Qt.AlignCenter)
        self.token_size_spinbox = QSpinBox()
        self.token_size_spinbox.setAlignment(Qt.AlignCenter)
        self.token_size_spinbox.setMinimum(5)
        self.token_size_spinbox.setMaximum(100)
        # set default value
        self.token_size_spinbox.setValue(TOKEN_SIZE)
        td_layout.addWidget(self.token_size_label)
        td_layout.addWidget(self.token_size_spinbox)
        self._layout.addLayout(arguments_layout)
        # distribute_path
        distribute_layout = QVBoxLayout()
        self.dfoldpath_button = QPushButton("Distribute fold path select")
        self.dfoldpath_lineedit = QLineEdit()
        distribute_layout.addWidget(self.dfoldpath_button)
        distribute_layout.addWidget(self.dfoldpath_lineedit)
        self._layout.addLayout(distribute_layout)
        # input_path
        input_layout = QVBoxLayout()
        self.input_path_button = QPushButton("Split token path select")
        self.input_path_lineedit = QLineEdit()
        input_layout.addWidget(self.input_path_button)
        input_layout.addWidget(self.input_path_lineedit)
        self._layout.addLayout(input_layout)
        # startu button
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)
        self.show_dialog_button = QPushButton("Show")
        self.start_button = QPushButton("Start Distributed")
        self.hide_dialog_button = QPushButton("Hide")
        button_layout.addWidget(self.show_dialog_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.hide_dialog_button)
        self._layout.addLayout(button_layout)
