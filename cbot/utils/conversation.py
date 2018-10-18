# -*- coding: utf-8 -*-

class StatementMixin(object):
    """
    封装每个语句，用来规范
    """

    def __init__(self):
        self.tags = []

    def get_tags(self):
        """
        返回标签列表
        """
        return self.tags

    def add_tags(self, tags):
        """
        添加标签列表
        """

        if type(tags) == str:
            self.tags.append(tags)
        else:
            for tag in tags:
                self.tags.append(tag)


class Statement(StatementMixin):
    """
    句子或者说话断语
    """

    def __init__(self, text, **kwargs):
        super().__init__()

        # 保证输入是字符串
        text = str(text)

        self.text = text
        self.tags = kwargs.pop('tags', [])
        self.in_response_to = kwargs.pop('in_response_to', [])

        self.extra_data = kwargs.pop('extra_data', {})

        # 聊天机器人，语句置信度
        self.confidence = 0
        # 数据库
        self.storage = None

    def __str__(self):
        return self.text

    def __repr__(self):
        return '<Statement text:%s>' % (self.text)

    def __hash__(self):
        return hash(self.text)

    def __eq__(self, other):
        if not other:
            return False

        if isinstance(other, Statement):
            return self.text == other.text

        return self.text == other

    def save(self):
        """
        存入数据库
        """
        self.storage.update(self)

    def add_extra_data(self, key, value):
        """
        :param key: 额外数据的键
        :param value: 额外数据的值
        :return:
        """
        self.extra_data[key] = value

    def add_response(self, response):
        """
        将响应添加到数据库，如果已经存在，则增加次数
        :param response: 响应
        :return:
        """
        if not isinstance(response, Response):
            raise Statement.InvalidTypeException(
                'A {} was received when a {} instance was expected'.format(
                    type(response),
                    type(Response(''))
                )
            )

        updated = False
        for index in range(0, len(self.in_response_to)):
            if response.text == self.in_response_to[index].text:
                self.in_response_to[index].occurrence += 1
                updated = True

        if not updated:
            self.in_response_to.append(response)

    def remove_response(self, response_text):
        """
        删除响应
        :param response_text: 要删除的文本值
        :return:
        """
        for response in self.in_response_to:
            if response_text == response.text:
                self.in_response_to.remove(response)
                return True
        return False

    def get_response_count(self, statement):
        """
        获取响应的次数
        :param statement: 响应
        :return:
        """
        for response in self.in_response_to:
            if statement.text == response.text:
                return response.occurrence

        return 0

    def serialize(self):
        """
        将响应对象封装成字典并返回
        :return:  返回字典数据
        """
        data = {}

        data['text'] = self.text
        data['in_response_to'] = []
        data['extra_data'] = self.extra_data

        for response in self.in_response_to:
            data['in_response_to'].append(response.serialize())

        return data

    class InvalidTypeException(Exception):

        def __init__(self, value='Received an unexpected value type.'):
            self.value = value

        def __str__(self):
            return repr(self.value)


class Response(object):
    """
    响应语句对象
    """

    def __init__(self, text, **kwargs):
        from datetime import datetime
        from dateutil import parser as date_parser

        self.text = text
        self.created_at = kwargs.get('created_at', datetime.now())
        self.occurrence = kwargs.get('occurrence', 1)

        if not isinstance(self.created_at, datetime):
            self.created_at = date_parser.parse(self.created_at)

    def __str__(self):
        return self.text

    def __repr__(self):
        return '<Response text:%s>' % (self.text)

    def __hash__(self):
        return hash(self.text)

    def __eq__(self, other):
        if not other:
            return False

        if isinstance(other, Response):
            return self.text == other.text

        return self.text == other

    def serialize(self):
        data = {}

        data['text'] = self.text
        data['created_at'] = self.created_at.isoformat()

        data['occurrence'] = self.occurrence

        return data
