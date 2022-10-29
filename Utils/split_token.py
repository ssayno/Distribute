#!/usr/bin/env python3
import os
from PyQt5.QtCore import QThread
import json
from Utils.config import Config
from settings import DELIMITER, TOKEN_SIZE


class Split_Token(QThread):
    def __init__(self, distribute_path, input_path, command, token_size=TOKEN_SIZE, delimiter=DELIMITER, parent=None):
        super(Split_Token, self).__init__(parent=parent)
        self.dp = distribute_path
        self.ip = input_path
        self.tk_size = token_size
        self.delimiter = delimiter
        self.command = command

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
        except Exception as e:
            print(e)
        finally:
            print('finished')
