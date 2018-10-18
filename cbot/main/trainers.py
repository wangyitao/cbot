# -*- coding: utf-8 -*-

import logging
from ..utils.conversation import Statement, Response
from ..utils import utils


class Trainer(object):
    """
    其他训练相关类的父类
    """

    def __init__(self, storage, **kwargs):
        self.cbot = kwargs.get('cbot')
        self.storage = storage
        self.logger = logging.getLogger(__name__)
        self.show_training_progress = kwargs.get('show_training_progress', True)

    def get_preprocessed_statement(self, input_statement):
        """
        对输入语句进行预处理
        """

        # 如果cbot为空，直接返回输入数据
        if not self.cbot:
            return input_statement
        # 预处理
        for preprocessor in self.cbot.preprocessors:
            input_statement = preprocessor(self, input_statement)

        return input_statement

    def train(self, *args, **kwargs):
        """
        给子类提供接口
        """
        raise self.TrainerInitializationException()

    def get_or_create(self, statement_text):
        """
        获取一个语句，如果存在，否则创建一个，并返回
        """
        # 预处理
        temp_statement = self.get_preprocessed_statement(
            Statement(text=statement_text)
        )
        # 从数据库中查找
        statement = self.storage.find(temp_statement.text)

        # 如果找不到，创建并返回用户输入的内容
        if not statement:
            statement = Statement(temp_statement.text)

        return statement

    class TrainerInitializationException(Exception):
        """
        如果没有重写父类的方法，返回这个错误
        """

        def __init__(self, value=None):
            default = (
                    'A training class must be specified before calling train(). '
            )
            self.value = value or default

        def __str__(self):
            return repr(self.value)

    def _generate_export_data(self):
        """
        生成输出数据
        :return: 生成的数据
        """
        result = []
        # 从数据库中获取
        for statement in self.storage.filter():
            for response in statement.in_response_to:
                result.append([response.text, statement.text])

        return result

    def export_for_training(self, file_path='./export.json'):
        """
        输出之前训练好的数据，用来训练其他cbot
        """
        import json
        export = {'conversations': self._generate_export_data()}
        with open(file_path, 'w+') as jsonfile:
            json.dump(export, jsonfile, ensure_ascii=False)


class ListTrainer(Trainer):
    """
    列表数据训练器，默认使用该训练器
    """

    def train(self, conversation=None):
        """
        根据提供的列表训练聊天机器人。默认为空
        """
        previous_statement_text = None
        if type(conversation) != list:
            conversation = []

        for conversation_count, text in enumerate(conversation):
            # 显示训练进度
            if self.show_training_progress:
                utils.print_progress_bar(
                    'Training',
                    conversation_count + 1, len(conversation)
                )

            statement = self.get_or_create(text)

            if previous_statement_text:
                statement.add_response(
                    Response(previous_statement_text)
                )

            previous_statement_text = statement.text
            # 更新数据库
            self.storage.update(statement)
