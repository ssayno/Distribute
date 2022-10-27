#!/usr/bin/env python3
import os
STATIC = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__), 'static'
    )
)
COOKIES = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__), 'Data', 'Cookies'
    )
)
TIMER_GAP = 1000
DELIMITER = '''||'''
TOKEN_SIZE = 90
COMMAND = '''python translate_simple-v3.py --use-ctd --filter-keywords "佛山,赤语,chiy,服装店,伊山,售后,含税,拿样,是否定制,选择我们,义乌,加工,定制,开票价格,我们的优势,实力商家,招牌,清仓,分销,现货,贴牌,定制,1688,taobao,ODM,工厂,.com" --use-inpainting --use-cuda --force-horizontal  --manga2eng --translator deepl --mode distributed'''
DISTRIBUTE_PATH = '''/Users/guoliang/Desktop/佛山市赤语服饰有限公司/'''
INPUT_PATH = '''/Users/guoliang/Desktop/blacklist_pic/'''
