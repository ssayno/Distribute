#!/usr/bin/env python3
from os.path import isdir
import sys
import os
import json
from PyQt5.QtCore import QCalendar, QDateTime, QPoint, QRectF, QThread, QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QCloseEvent, QCursor, QFont, QPainterPath, QRegion
from PyQt5.QtWidgets import QDialog, QHeaderView, QLabel, QMainWindow, QApplication, QFileDialog, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
from UiWidgets.mainui import UIWidget
from settings import DELIMITER, TOKEN_SIZE, TIMER_GAP, NAME_DELIMITER
from Utils.config import Config
import qdarkstyle
import fileinput
import re
import glob
import shutil


class Distribute_Command(QMainWindow):
    def __init__(self) -> None:
        super(Distribute_Command, self).__init__()
        self.setFixedSize(800, 350)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.cw = UIWidget(self)
        self.cw.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
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
        token_size = self.cw.token_size_spinbox.value()
        command = re.sub('\n', '', self.cw.command_input_list.toPlainText())
        if not os.path.isdir(distribute_path) or not os.path.isdir(input_path):
            # dir path not correct
            return
        else:
            self.cw.start_button.setEnabled(False)
            split_token_thread = Split_Token(
                distribute_path=distribute_path, input_path=input_path, command=command, dialong_update_signal=self.dialog.update_tree_signal,
                token_size=token_size, delimiter=delimiter, parent=self
            )
            split_token_thread.start()
            split_token_thread.finished.connect(
                lambda: self.connect_and_start_dialog_timer(distribute_path)
            )

    def connect_and_start_dialog_timer(self, d_path):
        self.dialog.listened_path = d_path
        self.dialog._timer.start(TIMER_GAP)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not hasattr(self, 'oldPos'):
            self.oldPos = event.globalPos()
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
        with fileinput.input("settings.py", inplace=True) as f:
            for row in f:
                key = row.split('=')[0].strip()
                if key in target_dict.keys():
                    if key == "TOKEN_SIZE":
                        print(f"{key} = {target_dict.get(key)}")
                    else:
                        print(f"{key} = '''{target_dict.get(key)}'''")
                else:
                    print(row, end='')
        return super().closeEvent(a0)


class Process_dialog(QDialog):
    follow_signal = pyqtSignal()
    update_tree_signal = pyqtSignal(str, str, str, bool)

    def __init__(self, parent=None):
        super(Process_dialog, self).__init__(parent=parent)
        # self.setStyleSheet("QDialog{background-color: red;}")
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        # set QDialog size
        self.w_width = 400
        self.w_height = 600
        self.radius = 20
        self.resize(self.w_width, self.w_height)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), self.radius, self.radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)
        #
        self.q_layout = QVBoxLayout()
        self.q_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.q_layout)
        #
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.follow_signal.connect(self._setPosition)
        self.addUIWidget()
        # timer
        self._timer = QTimer(self)
        # connect signal with slot func
        self.connect_signal_with_slot_func()
        # need a map represent the parent item
        self.map_name_item = {}
        self.listened_path = None

    def addUIWidget(self):
        banner = QLabel("动态显示")
        banner.setAlignment(Qt.AlignCenter)
        self.q_layout.addWidget(banner)
        self.timeLabel = QLabel("Not Start")
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.q_layout.addWidget(self.timeLabel)
        # tree show
        self.dir_tree = QTreeWidget(self)
        # basic configuration for tree dir
        self.dir_tree.setHeaderLabels(["Dir Or File", "Status"])
        self.dir_tree.header().setDefaultAlignment(Qt.AlignCenter)
        self.dir_tree.header().setSectionResizeMode(QHeaderView.Stretch)
        # dir tree qss style
        self.dir_tree.setStyleSheet("QTreeWidget{font: 16px;} QTreeWidget QHeaderView:section{font-size: 16px;}")
        # self.dir_tree_root = QTreeWidgetItem(self.dir_tree)
        # self.dir_tree_root.setTextAlignment(Qt.AlignCenter, Qt.AlignCenter)
        # self.dir_tree_root.setText(0, "aaa")
        # self.dir_tree_root.setText(1, "Normal")
        self.q_layout.addWidget(self.dir_tree)

    def _setPosition(self):
        left = self.parent().x() + self.parent().width()
        top = self.parent().y()
        self.setGeometry(
            int(left), int(top), self.w_width, self.w_height
        )

    def update_time_func(self):
        time_ = QDateTime.currentDateTime()
        format_time_ = time_.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.timeLabel.setText(f'{format_time_}')
        # first item
        first_item = self.dir_tree.itemAt(0, 0)
        self.dir_tree.setCurrentItem(first_item)
        if self.dir_tree.itemsExpandable():
            self.dir_tree.expandItem(first_item)


    def show(self) -> None:
        self.follow_signal.emit()
        return super().show()

    def connect_signal_with_slot_func(self):
        print('connect slot func')
        self.update_tree_signal.connect(self.update_tree_widget)
        self._timer.timeout.connect(self.listen_dir)

    def update_tree_widget(self, name, status, company_name, modify):
        if modify:
            need_modify_item = self.map_name_item[company_name]['JSON-FILES'].get(name, None)
            if need_modify_item is None:
                print("没有这个节点")
                return
            old_status = need_modify_item.text(1)
            print(old_status)
            if old_status != status:
                need_modify_item.setText(1, status)
        else:
            if company_name not in self.map_name_item:
                header_item = QTreeWidgetItem(self.dir_tree)
                header_item.setText(0, company_name)
                header_item.setText(1, "Pending")
                self.map_name_item[company_name] = {"company_name": header_item}
            parent = self.map_name_item[company_name]["company_name"]
            name_item_widget = QTreeWidgetItem(parent)
            name_item_widget.setText(0, name)
            name_item_widget.setText(1, status)
            if self.map_name_item[company_name].get("JSON-FILES", None) is None:
                self.map_name_item[company_name]['JSON-FILES'] = {
                    name: name_item_widget
                }
            else:
                self.map_name_item[company_name]['JSON-FILES'][name] = name_item_widget

    def listen_dir(self):
        # update time
        self.update_time_func()
        if self.listened_path is None or not os.path.isdir(self.listened_path):
            print('Listen Dir is invalid')
            return
        all_json_file_path = glob.glob(self.listened_path+ "/**/*.json", recursive=True)
        for json_file in all_json_file_path:
            temp_list = json_file.split(os.sep)
            company_name = temp_list[-2]
            if 'running' in company_name or 'done' in company_name:
                continue
            json_file_name = temp_list[-1]
            if 'DONE' in json_file_name:
                origin_name = f"{json_file_name.split(NAME_DELIMITER)[0]}.json"
                company_done_path = os.path.join(os.sep.join(temp_list[:-2]), f'{company_name}-done')
                if not os.path.exists(company_done_path):
                    os.mkdir(company_done_path)
                shutil.move(json_file, company_done_path)
                self.update_tree_signal.emit(origin_name, "DONE", company_name, True)
                print('done')
            elif NAME_DELIMITER in json_file_name:
                origin_name = f"{json_file_name.split(NAME_DELIMITER)[0]}.json"
                self.update_tree_signal.emit(origin_name, "Running", company_name, True)


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

class Split_Token(QThread):
    def __init__(self, distribute_path, input_path, command, dialong_update_signal, token_size=TOKEN_SIZE, delimiter=DELIMITER, parent=None):
        super(Split_Token, self).__init__(parent=parent)
        self.dp = distribute_path
        self.ip = input_path
        self.tk_size = token_size
        self.delimiter = delimiter
        self.command = command
        self.dus = dialong_update_signal

    def run(self) -> None:
        try:
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
                temp_list = single_config_path.split(os.sep)
                self.dus.emit(temp_list[-1], 'Pending', temp_list[-2], False)
        except Exception as e:
            print(e)
        finally:
            print('finished')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #t = Test()
    #t.show()
    dc = Distribute_Command()
    dc.show()
    sys.exit(app.exec_())
