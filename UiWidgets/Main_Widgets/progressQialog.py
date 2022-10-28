#!/usr/bin/env python3
from PyQt5.QtCore import QDateTime, QRectF, QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QPainterPath, QRegion
from PyQt5.QtWidgets import QDialog, QHeaderView, QLabel, QTreeWidget, QTreeWidgetItem, QVBoxLayout
import glob
import shutil
import qdarkstyle
import os

from settings import NAME_DELIMITER

class Process_dialog(QDialog):
    follow_signal = pyqtSignal()
    update_tree_signal = pyqtSignal(str, str, str, bool)
    update_count_siganl = pyqtSignal()

    def __init__(self, parent=None):
        super(Process_dialog, self).__init__(parent=parent)
        # self.setStyleSheet("QDialog{background-color: red;}")
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        # set QDialog size
        self.w_width = 400
        self.w_height = 600
        self.radius = 10
        self.resize(self.w_width, self.w_height)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), self.radius, self.radius, Qt.AbsoluteSize)
        # mask = QRegion(path.toFillPolygon().toPolygon())
        for polygon in path.toFillPolygons():
            mask = QRegion(polygon.toPolygon())
            self.setMask(mask)
        #
        self.q_layout = QVBoxLayout()
        self.q_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.q_layout)
        #
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.follow_signal.connect(self._setPosition)
        # timer
        self._timer = QTimer(self)
        # connect signal with slot func
        self.connect_signal_with_slot_func()
        # need a map represent the parent item
        self.map_name_item = {}
        self.listened_path = None
        # count
        self.success_count = 0
        self.fail_count = 0
        self.addUIWidget()

    def addUIWidget(self):
        self.timeLabel = QLabel("Not Start")
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.timeLabel.setStyleSheet('QLabel{font: 16px;}')
        self.q_layout.addWidget(self.timeLabel)
        # count label
        self.count_label = QLabel()
        self.count_label.setAlignment(Qt.AlignCenter)
        self.count_label.setStyleSheet('QLabel{font: 16px;}')
        self.count_label.setText(f"成功 {self.success_count}, 失败 {self.fail_count}")
        self.q_layout.addWidget(self.count_label)
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
        self.update_count_siganl.connect(self.update_label_slot_func)

    def update_tree_widget(self, name, status, company_name, modify):
        if modify:
            need_modify_item = self.map_name_item[company_name]['JSON-FILES'].get(name, None)
            if need_modify_item is None:
                print("没有这个节点")
                return
            old_status = need_modify_item.text(1)
            if old_status != status:
                if status == "DONE":
                    self.success_count += 1
                    self.update_count_siganl.emit()
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

    def update_label_slot_func(self):
        self.count_label.setText(f"成功 {self.success_count}, 失败 {self.fail_count}")
