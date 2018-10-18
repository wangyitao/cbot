# -*- coding: utf-8 -*-

import requests
import json


class Turing:
    def __init__(self, key):
        """
        图灵机器人api
        :param key: 图灵机器人官网获取
        """
        self.key = key

    # 与图灵机器人聊天
    def autochat(self, input_data, userid):
        api_url = 'http://www.tuling123.com/openapi/api'

        post_data = {
            'key': self.key,  # 这里的可以为图灵机器人的key
            'info': input_data,
            'userid': userid,
        }
        re_content = requests.post(url=api_url, data=post_data).text
        return json.loads(re_content)['text']
