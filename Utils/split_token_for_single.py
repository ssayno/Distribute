#!/usr/bin/env python3
import os
from PyQt5.QtCore import QThread
import json


class Split_Token_for_Single(QThread):
    def __init__(self, distribute_path, command, parent=None):
        super(Split_Token_for_Single, self).__init__(parent=parent)
        self.dp = distribute_path
        self.command = command

    def run(self) -> None:
        pass
