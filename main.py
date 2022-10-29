#!/usr/bin/env python3
import sys
import os
from PyQt5.QtCore import QPoint, QThread, QTimer, Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QStackedWidget, QVBoxLayout, QWidget
import fileinput
import re
from UiWidgets.Main_Widgets.complex_cuw import ComplexUIWidget
from UiWidgets.Main_Widgets.single_cuw import SingleUIWidget
from UiWidgets.Main_Widgets.progressQialog import Process_dialog
from UiWidgets.Main_Widgets.titlebar import Titlebar
from Utils.split_token import Split_Token
from settings import DELIMITER, TOKEN_SIZE


basic_style = '''\
QMainWindow{
background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #1BDAF9,
                stop: 0.5 #5FEEB8,
                stop:1 #1BDAF9);
font-family: "Times New Roman", Times, serif;
font: 24px;
}
'''
class Distribute_Command(QMainWindow):
    def __init__(self) -> None:
        super(Distribute_Command, self).__init__()
        self.setFixedSize(800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # set centeral widget
        self.cw = QWidget()
        self.cw_layout = QVBoxLayout()
        self.cw_layout.setSpacing(0)
        self.setCentralWidget(self.cw)
        self.cw.setLayout(self.cw_layout)
        # set basic style
        self.setStyleSheet(basic_style)
        self._stack = QStackedWidget()
        # add widget
        self.complex_command_uw = ComplexUIWidget(self)
        self.single_command_uw = SingleUIWidget(self)
        self._stack.addWidget(self.complex_command_uw)
        self._stack.addWidget(self.single_command_uw)
        # add widget
        self.title_bar = Titlebar(self)
        self.cw_layout.addWidget(self.title_bar)
        self.cw_layout.addWidget(self._stack)
        #self.setCentralWidget(self.complex_command_uw)
        # connect button with their function
        self.connect_button_with_func()
        # process show dialog
        self.dialog = Process_dialog(self)

    def connect_button_with_func(self):
        self.complex_command_uw.dfoldpath_button.clicked.connect(
            lambda checked, x=0: self.ask_directory(x)
        )
        self.complex_command_uw.input_path_button.clicked.connect(
            lambda checked, x=1: self.ask_directory(x)
        )
        self.complex_command_uw.start_button.clicked.connect(
            self.add_dialog_show_info
        )
        # title bar button
        self.title_bar.close_button.clicked.connect(
            self.quit_this_app

        )
        self.title_bar.minimum_button.clicked.connect(
            self.titlebar_minimize_app
        )
        self.title_bar.maximum_button.clicked.connect(
            self.titlebar_maximize_app
        )
        #
        self.complex_command_uw.show_dialog_button.clicked.connect(
            self.show_dialog
        )
        self.complex_command_uw.hide_dialog_button.clicked.connect(
            self.hide_dialog
        )
        # Sat Oct 29 20:08:08 2022
        self.complex_command_uw.check_to_single_command_ui.clicked.connect(
            lambda: self._stack.setCurrentWidget(self.single_command_uw)
        )
        self.single_command_uw.check_to_complex_command_ui.clicked.connect(
            lambda: self._stack.setCurrentWidget(self.complex_command_uw)
        )
        #
        self._stack.currentChanged.connect(self.titlebar_info_show)

    def ask_directory(self, cate_number: int):
        gets_ = QFileDialog().getExistingDirectory(self, caption='Get Directory',
                                                   directory=os.path.join(os.path.expanduser('~'), 'Desktop'))
        if gets_ == "":
            return
        _directory = gets_
        if cate_number == 0:
            self.complex_command_uw.dfoldpath_lineedit.setText(_directory)
        elif cate_number == 1:
            self.complex_command_uw.input_path_lineedit.setText(_directory)
        else:
            print("What are you doing")

    def show_dialog(self):
        if not self.dialog.show_dialog():
            if not self.dialog.isVisible():
                self.dialog.show()

    def hide_dialog(self):
        if not self.dialog.hide_dialog():
            if self.dialog.isVisible():
                self.dialog.hide()

    def add_dialog_show_info(self):
        distribute_path = os.path.normpath(self.complex_command_uw.dfoldpath_lineedit.text().strip())
        input_path = os.path.normpath(self.complex_command_uw.input_path_lineedit.text().strip())
        delimiter = self.complex_command_uw.delimiter_lineedit.text().strip()
        token_size = self.complex_command_uw.token_size_spinbox.value()
        command = re.sub(r'\s+', ' ', self.complex_command_uw.command_input_list.toPlainText())
        if not os.path.isdir(distribute_path) or not os.path.isdir(input_path):
            # dir path not correct
            QMessageBox.warning(self, "Warning", "Path is invalid, please input correct path to continue.")
            return
        else:
            self.show_dialog()
            split_token_thread = Split_Token(
                distribute_path=distribute_path, input_path=input_path, command=command,
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

    def titlebar_info_show(self):
        current_widget = self._stack.currentWidget()
        if current_widget == self.complex_command_uw:
            self.title_bar.info_label.setText("Complex Command")
        elif current_widget == self.single_command_uw:
            self.title_bar.info_label.setText("Single Command")

    def quit_this_app(self):
        self.close()
        app.instance().quit()

    def closeEvent(self, a0: QCloseEvent) -> None:
        target_dict = {
            "DISTRIBUTE_PATH": self.complex_command_uw.dfoldpath_lineedit.text().strip(),
            "COMMAND": re.sub('\n', '', self.complex_command_uw.command_input_list.toPlainText()),
            "INPUT_PATH": self.complex_command_uw.input_path_lineedit.text().strip(),
            "TOKEN_SIZE": self.complex_command_uw.token_size_spinbox.value(),
            "DELIMITER": self.complex_command_uw.delimiter_lineedit.text().strip()
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
