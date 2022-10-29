#!/usr/bin/env python3
import sys
import os
from PyQt5.QtCore import QMetaEnum, QPoint, QThread, QTimer, Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QWidget
import fileinput
import re
from UiWidgets.Main_Widgets.mainui import UIWidget
from UiWidgets.Main_Widgets.progressQialog import Process_dialog
from Utils.split_token import Split_Token
from settings import DELIMITER, TOKEN_SIZE, TIMER_GAP


basic_style = '''  \
QWidget{
font: 20px;
}
QLabel{
font: 20px;
}
QTextEdit{
font: 20px;
}
'''
class Distribute_Command(QMainWindow):
    def __init__(self) -> None:
        super(Distribute_Command, self).__init__()
        self.setFixedSize(800, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(basic_style)
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
        distribute_path = os.path.normpath(self.cw.dfoldpath_lineedit.text().strip())
        input_path = os.path.normpath(self.cw.input_path_lineedit.text().strip())
        delimiter = self.cw.delimiter_lineedit.text().strip()
        token_size = self.cw.token_size_spinbox.value()
        command = re.sub(r'\s+', '', self.cw.command_input_list.toPlainText())
        if not os.path.isdir(distribute_path) or not os.path.isdir(input_path):
            # dir path not correct
            QMessageBox.warning(self, "Warning", "Path is invalid, please input correct path to continue.")
            return
        else:
            self.show_dialog()
            split_token_thread = Split_Token(
                distribute_path=distribute_path, input_path=input_path, command=command, dialong_update_signal=self.dialog.update_tree_signal,
                token_size=token_size, delimiter=delimiter, parent=self
            )
            split_token_thread.start()
            split_token_thread.finished.connect(
                lambda: self.connect_and_start_dialog_timer(distribute_path)
            )

    def connect_and_start_dialog_timer(self, d_path):
        if d_path != self.dialog.listened_path:
            self.dialog.listened_path = d_path
        else:
            QMessageBox.warning(self, 'Warning', '不要设置同一个目录跑两次')

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not hasattr(self, 'oldPos'):
            self.oldPos = event.globalPos()
        else:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
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
        self.close()
        app.instance().quit()

    def closeEvent(self, a0: QCloseEvent) -> None:
        target_dict = {
            "DISTRIBUTE_PATH": self.cw.dfoldpath_lineedit.text().strip(),
            "COMMAND": re.sub('\n', '', self.cw.command_input_list.toPlainText()),
            "INPUT_PATH": self.cw.input_path_lineedit.text().strip(),
            "TOKEN_SIZE": self.cw.token_size_spinbox.value(),
            "DELIMITER": self.cw.delimiter_lineedit.text().strip()
        }
        with fileinput.input("settings.py", inplace=True, encoding='U8') as f:
            for row in f:
                key = row.split('=')[0].strip()
                if key in target_dict.keys():
                    if key == "TOKEN_SIZE":
                        print(f"{key} = {target_dict.get(key)}")
                    else:
                        print(f"{key} = r'''{target_dict.get(key)}'''")
                else:
                    print(row, end='')
        return super().closeEvent(a0)



class Test(QWidget):
    def __init__(self):
        super(Test, self).__init__()
        tim = QTimer(self)
        # single_ = QTestThread(self, "", "", "")
        single_ = Split_Token("", "", "", "")
        single_.start()
        tim.timeout.connect(lambda: print(single_.isFinished()))
        tim.start(2000)

class QTestThread(QThread):
    def __init__(self, distribute_path, input_path, command, token_size=TOKEN_SIZE, delimiter=DELIMITER, parent=None):
        super(QTestThread, self).__init__()
        self.dp = distribute_path
        self._ip = input_path
        self.tk_size = token_size
        self.delimiter = delimiter
        self.command = command

    def run(self):
        print('a')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #t = Test()
    #t.show()
    dc = Distribute_Command()
    dc.show()
    sys.exit(app.exec_())
