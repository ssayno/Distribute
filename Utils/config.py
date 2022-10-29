#!/usr/bin/env python3
import os
from settings import TOKEN_SIZE
class Config:
    def __init__(self, company_path, command, token_size=TOKEN_SIZE):
        self.company_name = os.path.basename(company_path)
        print(self.company_name)
        self.distination = f'{company_path}-translated'
        self.command =command
        self.token_size = token_size
        self.file_path_list = [
            {
                'command': self.command,
                'distination': self.distination,
                'file_list': []
            }
        ]
        self.index = 0

    def _append(self, value):
        if len(self.file_path_list[self.index].get('file_list')) >= self.token_size:
            self.index += 1
            self.file_path_list.append(
                {
                    'command': self.command,
                    'distination': self.distination,
                    'file_list': [value]
                }
            )
        else:
            self.file_path_list[self.index]['file_list'].append(value)
