# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cbot import CBot

cbot = CBot('felix')
cbot.turing_key = ''  # 从图灵官网获取 http://www.tuling123.com/
while True:
    que = input('我：')
    reponse = cbot.get_response(str(que), api='turing')
    print('CBot：', reponse)
