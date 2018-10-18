# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cbot import CBot

cbot = CBot('felix')

# 如果从0开始训练
# cbot.train()
# while True:
#     que = input('我：')
#     reponse = cbot.get_response(str(que))
#     print('大白：', reponse)


# 如果希望先训练一些数据,必须是列表类型
# 上一句话是下一句话的回答
trainList = [
    '早',
    '早上好',
    '早饭吃了么',
    '还没呢！，你呢？',
    '我也没吃',
    '我们一起吃早饭去吧',
    '好呀'
]

cbot.train(trainList)
while True:
    que = input('我：')
    reponse = cbot.get_response(str(que))
    print('大白：', reponse)
