#!/usr/bin/env python3
import sys
import os
import json
from PyQt5.QtCore import QPoint, QThread, Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QFileDialog
from UiWidgets.mainui import UIWidget
from settings import DELIMITER, TOKEN_SIZE
from Utils.config import Config


class Distribute_Command(QMainWindow):
    def __init__(self) -> None:
        super(Distribute_Command, self).__init__()
        self.resize(600, 300)
        self.setMaximumSize(800, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.cw = UIWidget(self)
        self.setCentralWidget(self.cw)
        # connect button with their function
        self.connect_button_with_func()
        # process show dialog
        self.dialog = Process_dialog(self)


    def connect_button_with_func(self):
        self.cw.dfoldpath_button.clicked.connect(
            lambda checked, x=0: self.ask_directory(x)
        )
        self.cw.input_path_button.clicked.connect(
            lambda checked, x=1: self.ask_directory(x)
        )
        self.cw.start_button.clicked.connect(
            self.add_dialog_show_info
        )
        # title bar button
        self.cw.title_bar.close_button.clicked.connect(
            self.quit_this_app
        )
        self.cw.title_bar.minimum_button.clicked.connect(
            self.titlebar_minimize_app
        )
        self.cw.title_bar.maximum_button.clicked.connect(
            self.titlebar_maximize_app
        )
        #
        self.cw.show_dialog_button.clicked.connect(
            self.show_dialog
        )
        self.cw.hide_dialog_button.clicked.connect(
            self.hide_dialog
        )

    def ask_directory(self, cate_number: int):
        gets_ = QFileDialog().getExistingDirectory(self, caption='Get Directory',
                                                   directory=os.path.join(os.path.expanduser('~'), 'Desktop'))
        if gets_ == "":
            return
        _directory = gets_
        if cate_number == 0:
            self.cw.dfoldpath_lineedit.setText(_directory)
        elif cate_number == 1:
            self.cw.input_path_lineedit.setText(_directory)
        else:
            print("What are you doing")

    def show_dialog(self):
        if not self.dialog.isVisible():
            self.dialog.show()

    def hide_dialog(self):
        if self.dialog.isVisible():
            self.dialog.hide()

    def add_dialog_show_info(self):
        self.show_dialog()
        distribute_path = self.cw.dfoldpath_lineedit.text().strip()
        input_path = self.cw.input_path_lineedit.text().strip()
        delimiter = self.cw.delimiter_lineedit.text().strip()
        token_size= self.cw.token_size_spinbox.value()
        command = re.sub('\n', '', self.cw.command_input_list.toPlainText())
        if not os.path.isdir(distribute_path) or not os.path.isdir(input_path):
            return
        else:
            self.cw.start_button.setEnabled(False)
            split_token_thread = Split_Token(
                distribute_path=distribute_path, input_path=input_path, command=command, token_size=token_size, delimiter=delimiter, parent=self
            )
            split_token_thread.start()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not hasattr(self, 'oldPos'):
            self.oldPos =  event.globalPos()
        else:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.dialog.follow_signal.emit()
            self.oldPos = event.globalPos()
        return super().mouseMoveEvent(event)

    def titlebar_minimize_app(self):
        self.showMinimized()

    def titlebar_maximize_app(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def quit_this_app(self):
        app.instance().quit()


class Process_dialog(QDialog):
    follow_signal = pyqtSignal()
    def __init__(self, parent=None):
        super(Process_dialog, self).__init__(parent=parent)
        self.w_width = 400
        self.w_height = 600
        #
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.follow_signal.connect(self._setPosition)

    def _setPosition(self):
        left = self.parent().x() + self.parent().width()
        top = self.parent().y() - self.w_height / 2 + self.parent().height() / 2
        self.setGeometry(
            int(left), int(top), self.w_width, self.w_height
        )

    def show(self) -> None:
        self.follow_signal.emit()
        return super().show()


class Split_Token(QThread):
    def __init__(self, distribute_path, input_path, command, token_size= TOKEN_SIZE, delimiter=DELIMITER, parent=None):
        self.dp = distribute_path
        self.ip = input_path
        self.tk_size = token_size
        self.delimiter = delimiter
        self.command = command
        super(Split_Token, self).__init__(parent=parent)

    def run(self) -> None:
        _config = Config(
            company_path=self.ip, command=self.command, token_size=self.tk_size
        )
        for item in os.listdir(self.ip):
            item_path = os.path.join(self.ip, item)
            if item.startswith('.') or not os.path.isdir(item_path):
                continue
            _config._append(item_path)
        company_config_path = os.path.join(self.dp, _config.company_name)
        if not os.path.exists(company_config_path):
            os.mkdir(company_config_path)
        for index_, content in enumerate(_config.file_path_list):
            single_config_path = os.path.join(company_config_path, f'token-{index_ + 1}.json')
            with open(single_config_path, 'w+', encoding='U8') as f:
                command = content['command']
                file_list_argument = f'{DELIMITER}'.join(content['file_list'])
                image_dst_distributed = content['distination']
                passed_command = f'{command} --file-list "{file_list_argument}" --image-dst-distributed "{image_dst_distributed}"'
                json.dump({'command': passed_command}, f, indent='\t', ensure_ascii=False)



        return super().run()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dc = Distribute_Command()
    dc.show()
    sys.exit(app.exec_())
