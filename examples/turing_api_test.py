# -*- coding: utf-8 -*-

from cbot import CBot

cbot = CBot('felix')
cbot.turing_key = ''  # 从图灵官网获取 http://www.tuling123.com/
while True:
    que = input('我：')
    reponse = cbot.get_response(str(que), api='turing')
    print('CBot：', reponse)
