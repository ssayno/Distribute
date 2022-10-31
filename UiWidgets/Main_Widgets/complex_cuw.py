#!/usr/bin/env python3
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QImageReader, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QTextEdit, QVBoxLayout, QWidget
from settings import DELIMITER, TOKEN_SIZE, COMMAND, INPUT_PATH, DISTRIBUTE_PATH, STATIC
qss_style_file = os.path.join(STATIC, 'Qss', 'complex_cuw.qss')
with open(qss_style_file, 'r', encoding='U8') as f:
    complex_cuw_style = f.read()

class ComplexUIWidget(QWidget):
    def __init__(self, parent=None):
        super(ComplexUIWidget, self).__init__(parent=parent)
        self.setStyleSheet(complex_cuw_style)
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
        # delimiter select
        td_layout = QVBoxLayout()
        td_layout.setAlignment(Qt.AlignTop)
        td_layout.setSpacing(0)
        self.check_to_single_command_ui = QPushButton("传递单条命令")
        self.delimiter_label = QLabel("Delimiter")
        self.delimiter_lineedit = QLineEdit(DELIMITER)
        self.delimiter_lineedit.setObjectName('delimiter')
        td_layout.addWidget(self.check_to_single_command_ui)
        td_layout.addWidget(self.delimiter_label)
        td_layout.addWidget(self.delimiter_lineedit)
        arguments_layout.addLayout(td_layout, stretch=1)
        # Token size
        token_layout = QVBoxLayout()
        token_layout.setSpacing(0)
        self.token_size_label = QLabel("Token Size")
        self.token_size_spinbox = QSpinBox()
        self.token_size_spinbox.setAlignment(Qt.AlignCenter)
        self.token_size_spinbox.setMinimum(5)
        self.token_size_spinbox.setMaximum(100)
        # set default value
        self.token_size_spinbox.setValue(int(TOKEN_SIZE))
        td_layout.addWidget(self.token_size_label)
        td_layout.addWidget(self.token_size_spinbox)
        self._layout.addLayout(arguments_layout, stretch=2)
        # distribute_path
        distribute_layout = QVBoxLayout()
        self.dfoldpath_button = QPushButton("Distribute fold path select")
        self.dfoldpath_lineedit = QLineEdit()
        if DISTRIBUTE_PATH is not None:
            self.dfoldpath_lineedit.setText(DISTRIBUTE_PATH)
        distribute_layout.addWidget(self.dfoldpath_button)
        distribute_layout.addWidget(self.dfoldpath_lineedit)
        self._layout.addLayout(distribute_layout, stretch=1)
        # input_path
        input_layout = QVBoxLayout()
        self.input_path_button = QPushButton("Split token path select")
        self.input_path_lineedit = QLineEdit()
        if INPUT_PATH is not None:
            self.input_path_lineedit.setText(INPUT_PATH)
        input_layout.addWidget(self.input_path_button)
        input_layout.addWidget(self.input_path_lineedit)
        self._layout.addLayout(input_layout, stretch=1)
        # start button
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(2)
        self.show_dialog_button = QPushButton("Show")
        self.start_button = QPushButton("Start Distributed")
        self.hide_dialog_button = QPushButton("Hide")
        button_layout.addWidget(self.show_dialog_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.hide_dialog_button)
        self._layout.addLayout(button_layout, stretch=1)
