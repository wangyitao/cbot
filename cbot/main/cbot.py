# -*- coding: utf-8 -*-

import logging
from ..adapters import StorageAdapter
from ..adapters import InputAdapter
from ..adapters import OutputAdapter
from ..utils import utils
from ..adapters import MultiAdapter
from ..utils.constants import DEFAULT_STORAGE_ADAPTER, DEFAULT_NO_KNOWLEDGE_ADAPTER, DEFAULT_CORE_ADAPTER, \
    DEFAULT_INPUT_ADAPTER, DEFAULT_OUTPUT_ADAPTER, DEFAULT_TRAINER, IS_STUDY


class CBot(object):
    """
    对话聊天机器人。
    """

    def __init__(self, name, **kwargs):

        self.name = name
        kwargs['name'] = name
        kwargs['cbot'] = self

        self.default_session = None

        # 数据库适配器
        storage_adapter = kwargs.get('storage_adapter', DEFAULT_STORAGE_ADAPTER)

        # 找不到答案的时候使用的适配器
        no_knowledge_adapter = kwargs.get('no_knowledge_adapter', DEFAULT_NO_KNOWLEDGE_ADAPTER)
        core_adapters = kwargs.get('core_adapters', DEFAULT_CORE_ADAPTER)
        input_adapter = kwargs.get('input_adapter', DEFAULT_INPUT_ADAPTER)
        output_adapter = kwargs.get('output_adapter', DEFAULT_OUTPUT_ADAPTER)

        # 检查哥哥适配器是否是对应的子类
        utils.initialize_adapter_class(storage_adapter, StorageAdapter)
        utils.initialize_adapter_class(input_adapter, InputAdapter)
        utils.initialize_adapter_class(output_adapter, OutputAdapter)

        # 初始化各个适配器
        self.adapters = MultiAdapter(**kwargs)
        self.storage = utils.initialize_class(storage_adapter, **kwargs)
        self.input = utils.initialize_class(input_adapter, **kwargs)
        self.output = utils.initialize_class(output_adapter, **kwargs)

        # 过滤器
        filters = kwargs.get('filters', tuple())
        self.filters = tuple([utils.import_module(filter_)() for filter_ in filters])

        # 添加必要适配器
        self.adapters.system_adapters.append(
            utils.initialize_class(no_knowledge_adapter, **kwargs)
        )
        # 添加适配器
        self.adapters.add_adapter(core_adapters, **kwargs)

        # 将cbot绑定适配器
        self.adapters.set_cbot(self)
        self.input.set_cbot(self)
        self.output.set_cbot(self)

        # 除去空白
        preprocessors = kwargs.get(
            'preprocessors', [
                'cbot.utils.preprocessors.clean_whitespace'
            ]
        )
        self.preprocessors = []
        for preprocessor in preprocessors:
            self.preprocessors.append(utils.import_module(preprocessor))

        # 设置训练器
        trainer = kwargs.get('trainer', DEFAULT_TRAINER)
        TrainerClass = utils.import_module(trainer)
        self.trainer = TrainerClass(self.storage, **kwargs)
        self.training_data = kwargs.get('training_data')
        self.default_conversation_id = None
        self.logger = kwargs.get('logger', logging.getLogger(__name__))
        # 是否开启学习功能，将输入也存入数据库
        self.read_only = kwargs.get('read_only', not IS_STUDY)

        if kwargs.get('initialize', True):
            self.initialize()

    def initialize(self):
        """
        在结果获取之前需要的操作
        """
        self.adapters.initialize()

    def get_response(self, input_value, conversation_id=None, api='local'):
        """
        从数据库获取回复内容
        :param input_value: 输入值
        :param conversation_idji: 对话内容
        :return:
        """
        if api == 'turing':
            from ..api import Turing
            if hasattr(self, 'turing_key') and getattr(self,'turing_key').strip():
                turing = Turing(self.turing_key)
            else:
                raise AttributeError(
                    "'CBot' object has no attribute 'turing_key',And you can get key at 'http://www.tuling123.com/'")
            return turing.autochat(input_value, self.name)

        if not conversation_id:
            if not self.default_conversation_id:
                self.default_conversation_id = self.storage.create_conversation()
            conversation_id = self.default_conversation_id

        input_statement = self.input.process_input_statement(input_value)

        # 预处理输入语句
        for preprocessor in self.preprocessors:
            input_statement = preprocessor(self, input_statement)

        statement, response = self.generate_response(input_statement, conversation_id)

        # 根据之前用户输入的内容，并做出最新响应
        previous_statement = self.storage.get_latest_response(conversation_id)

        # cbot是否是学习状态，如果是学习状态根据将用户输入存入数据库
        if not self.read_only:
            self.learn_response(statement, previous_statement)
            self.storage.add_to_conversation(conversation_id, statement, response)

        # 使用输出适配器处理响应输出
        return self.output.process_response(response, conversation_id)

    def generate_response(self, input_statement, conversation_id):
        """
        根据输入返回响应
        """
        self.storage.generate_base_query(self, conversation_id)

        # 根据适配去返回合适的响应
        response = self.adapters.process(input_statement)

        return input_statement, response

    def learn_response(self, statement, previous_statement):
        """
        将对话内容添加到数据库，从对话中学习，将cbot预测内容当做问题，对话内容当做答案
        :param statement: 对话内容
        :param previous_statement: cbot预测内容
        :return:
        """
        from ..utils.conversation import Response

        if previous_statement:
            statement.add_response(
                Response(previous_statement.text)
            )
            self.logger.info('Adding "{}" as a response to "{}"'.format(
                statement.text,
                previous_statement.text
            ))

        # 更新
        self.storage.update(statement)

    def set_trainer(self, training_class, **kwargs):
        """
        设置训练器
        :param training_class: 训练器类
        :param kwargs:
        :return:
        """
        # 设置cbot
        if 'cbot' not in kwargs:
            kwargs['cbot'] = self

        self.trainer = training_class(self.storage, **kwargs)

    @property
    def train(self):
        """
        训练属性
        """
        return self.trainer.train
