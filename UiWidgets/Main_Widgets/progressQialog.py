#!/usr/bin/env python3
from PyQt5.QtCore import QDateTime, QEvent, QPoint, QPropertyAnimation, QRectF, QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QPainterPath, QRegion
from PyQt5.QtWidgets import (QDesktopWidget, QDialog, QGridLayout, QHeaderView, QLabel,
                             QTreeWidget, QTreeWidgetItem, QVBoxLayout)
import glob
import shutil
import os
import re
from settings import NAME_DELIMITER, TIMER_GAP, STATIC

qss_style_file = os.path.join(STATIC, 'Qss', 'qdialog.qss')
with open(qss_style_file, 'r', encoding='U8') as f:
    qdialog_style = f.read()
class Process_dialog(QDialog):
    update_tree_signal = pyqtSignal(str, str, str, bool)
    update_count_siganl = pyqtSignal()

    def __init__(self, parent=None):
        super(Process_dialog, self).__init__(parent=parent)
        # set position
        self.desktop = QDesktopWidget()
        #
        self.limit_width = 2
        self.hide_width = self.desktop.width() - self.limit_width
        self.setStyleSheet(qdialog_style)
        self._setPosition()
        # create animation
        self.create_animation()
        #
        self.q_layout = QVBoxLayout()
        self.q_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.q_layout)
        #
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        # timer
        self._timer = QTimer(self)
        # connect signal with slot func
        self.connect_signal_with_slot_func()
        # need a map represent the parent item
        self.map_name_item = {}
        self.listened_path = None
        # count
        self.all_count = 0
        self.success_count = 0
        self.fail_count = 0
        #
        self.running_bg_color = QBrush(QColor('blue'))
        self.done_bg_color = QBrush(QColor("green"))
        self.addUIWidget()

    def addUIWidget(self):
        self.timeLabel = QLabel("Not Start")
        self.timeLabel.setObjectName('time-label')
        self.q_layout.addWidget(self.timeLabel)
        # count label
        # count layout
        count_layout = QGridLayout()
        count_layout.setHorizontalSpacing(0)
        count_layout.setContentsMargins(0, 0, 0, 0)
        self.all_name_label = QLabel("总数")
        self.success_name_label = QLabel("成功的数量")
        self.fail_name_label = QLabel("失败的数量")
        #
        self.all_count_label = QLabel("0")
        self.all_count_label.setFixedHeight(50)
        self.all_count_label.setObjectName("count-label")
        self.success_count_label = QLabel("0")
        self.success_count_label.setObjectName("count-label")
        self.success_count_label.setFixedHeight(50)
        self.fail_count_label = QLabel("0")
        self.fail_count_label.setObjectName("count-label")
        self.fail_count_label.setFixedHeight(50)
        count_layout.addWidget(self.all_name_label, 0, 0, 1, 1)
        count_layout.addWidget(self.success_name_label, 0, 1, 1, 1)
        count_layout.addWidget(self.fail_name_label, 0, 2, 1, 1)
        count_layout.addWidget(self.all_count_label, 1, 0, 1, 1)
        count_layout.addWidget(self.success_count_label, 1, 1, 1, 1)
        count_layout.addWidget(self.fail_count_label, 1, 2, 1, 1)
        self.q_layout.addLayout(count_layout)
        # tree show
        self.dir_tree = QTreeWidget(self)
        # basic configuration for tree dir
        self.dir_tree.setHeaderLabels(["Dir Or File", "Status"])
        self.dir_tree.header().setDefaultAlignment(Qt.AlignCenter)
        self.dir_tree.header().setSectionResizeMode(QHeaderView.Stretch)
        self.dir_tree.itemChanged.connect(self.status_column_changed)
        self.q_layout.addWidget(self.dir_tree)

    def _setPosition(self):
        d_width = self.desktop.width()
        d_height = self.desktop.height()
        width = 600
        self.setGeometry(
            d_width - width, 3, width, d_height - 3
        )
        radius = 10
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), radius, radius, Qt.AbsoluteSize)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)


    def update_time_func(self):
        time_ = QDateTime.currentDateTime()
        format_time_ = time_.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.timeLabel.setText(f'{format_time_}')

    def connect_signal_with_slot_func(self):
        print('connect slot func')
        self.update_tree_signal.connect(self.update_tree_widget)
        self._timer.timeout.connect(self.listen_dir)
        self._timer.start(TIMER_GAP)
        self.update_count_siganl.connect(self.update_label_slot_func)

    def update_tree_widget(self, name, status, company_name, modify):
        if modify:
            need_modify_item = self.map_name_item[company_name]['JSON-FILES'].get(name, None)
            if need_modify_item is None:
                return
            old_status = need_modify_item.text(1)
            if old_status != status:
                need_modify_item.setText(1, status)
                if status == "DONE":
                    # need_modify_item.setBackground(0, self.done_bg_color)
                    # need_modify_item.setBackground(1, self.done_bg_color)
                    self.success_count += 1
                # elif status == "Running":
                    # need_modify_item.setBackground(0, self.running_bg_color)
                    # need_modify_item.setBackground(1, self.running_bg_color)
        else:
            if company_name not in self.map_name_item:
                header_item = QTreeWidgetItem(self.dir_tree)
                header_item.setTextAlignment(0, Qt.AlignLeft)
                header_item.setTextAlignment(1, Qt.AlignCenter)
                header_item.setText(0, company_name)
                header_item.setText(1, "Processing")
                self.map_name_item[company_name] = {"company_name": header_item}
            if name in self.map_name_item[company_name].get('JSON-FILES', []):
                return
            parent = self.map_name_item[company_name]["company_name"]
            name_item_widget = QTreeWidgetItem(parent)
            name_item_widget.setTextAlignment(0, Qt.AlignCenter)
            name_item_widget.setTextAlignment(1, Qt.AlignCenter)
            name_item_widget.setText(0, name)
            name_item_widget.setText(1, status)
            if self.map_name_item[company_name].get("JSON-FILES", None) is None:
                self.map_name_item[company_name]['JSON-FILES'] = {
                    name: name_item_widget
                }
            else:
                self.map_name_item[company_name]['JSON-FILES'][name] = name_item_widget

    def listen_dir(self):
        # update time, time gap: 1s
        self.update_time_func()
        self.all_count = 0
        if self.listened_path is None or not os.path.isdir(self.listened_path):
            print('Listen Dir is invalid')
            return
        all_json_file_path = glob.glob(self.listened_path+ "/**/*.json", recursive=True)
        # sort all json file with their number
        all_json_file_path.sort(key=lambda x: int(re.search(r'(\d+)', x).groups(1)[0]))
        for json_file in all_json_file_path:
            temp_list = json_file.split(os.sep)
            company_name = temp_list[-2]
            self.all_count += 1
            if 'done' in company_name:
                continue
            json_file_name = temp_list[-1]
            if 'DONE' in json_file_name:
                origin_name = f"{json_file_name.split(NAME_DELIMITER)[0]}.json"
                company_done_path = os.path.join(os.sep.join(temp_list[:-3]), 'Distribute-DONE', f'{company_name}-done')
                if not os.path.exists(company_done_path):
                    os.makedirs(company_done_path, exist_ok=True)
                target_path_name = os.path.normpath(os.path.join(company_done_path, json_file_name))
                if os.path.exists(target_path_name):
                    print('||目标目录存在||')
                    os.remove(target_path_name)
                shutil.move(json_file, company_done_path)
                if company_name in self.map_name_item:
                    self.update_tree_signal.emit(origin_name, "DONE", company_name, True)
                else:
                    self.update_tree_signal.emit(origin_name, "DONE", company_name, False)
            elif NAME_DELIMITER in json_file_name:
                origin_name = f"{json_file_name.split(NAME_DELIMITER)[0]}.json"
                if origin_name in self.map_name_item[company_name].get('JSON-FILES', []):
                    self.update_tree_signal.emit(origin_name, "Running", company_name, True)
                else:
                    self.update_tree_signal.emit(origin_name, "Running", company_name, False)
            else:
                self.update_tree_signal.emit(json_file_name, "Waiting", company_name, False)
        self.update_count_siganl.emit()
        self.check_if_done()

    def update_label_slot_func(self):
        if self.all_count >= int(self.all_count_label.text()):
            self.all_count_label.setText(f'{self.all_count}')
        self.success_count_label.setText(f'{self.success_count}')
        self.fail_count_label.setText(f'{self.fail_count}')

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not hasattr(self, 'oldPos'):
            self.oldPos = event.globalPos()
        else:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.oldPos = event.globalPos()
            self.move(self.x() + delta.x(), self.y() + delta.y())
        return super().mouseMoveEvent(event)

    def leaveEvent(self, a0: QEvent) -> None:
        self.hide_dialog()
        return super().enterEvent(a0)

    def enterEvent(self, a0: QEvent) -> None:
        self.show_dialog()
        return super().leaveEvent(a0)

    def show_dialog(self) -> bool:
        if self.x() == self.hide_width:
            self.show_animation.start()
            return True
        return False

    def hide_dialog(self) -> bool:
        if self.isVisible():
            if self.x() >= (self.desktop.width() - self.width()):
                if self.x() != self.hide_width:
                    self.hide_animation.start()
                return True
            return False
        return True

    def create_animation(self):
        # show animation
        self.hide_animation = QPropertyAnimation(self, b'pos', self)
        self.hide_animation.setStartValue(QPoint(self.x(), self.y()))
        # 自己实现退出，最小化操作，就设置为0，不然干不掉了
        self.hide_animation.setEndValue(QPoint(self.desktop.width() - self.limit_width, self.y()))
        self.hide_animation.setDuration(300)
        # hide animation
        self.show_animation = QPropertyAnimation(self, b'pos', self)
        self.show_animation.setStartValue(QPoint(self.x(), self.y()))
        self.show_animation.setEndValue(QPoint(self.desktop.width() - self.width(), self.y()))
        # self.hide_animation.setEndValue(QPoint(0, self.y()))
        # 倒过来的动画有问题

    def check_if_done(self):
        for dir_item in self.map_name_item.values():
            header_item = dir_item['company_name']
            json_items = dir_item['JSON-FILES']
            for json_item in json_items.values():
                if json_item.text(1) != "DONE":
                    old_status = header_item.text(1)
                    if old_status == "DONE":
                        header_item.setText(1, "Processing")
                    break
            else:
                header_item.setText(1, "DONE")


    def status_column_changed(self, item: QTreeWidgetItem, column: int):
        if column == 1:
            status_text = item.text(column)
            if status_text == "Running":
                item.setBackground(0, self.running_bg_color)
                item.setBackground(1, self.running_bg_color)
            elif status_text == "DONE":
                item.setBackground(0, self.done_bg_color)
                item.setBackground(1, self.done_bg_color)
