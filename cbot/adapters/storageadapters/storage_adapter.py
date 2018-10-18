import logging


class StorageAdapter(object):
    """
    所有存储数据都要实现的基类
    """

    def __init__(self, base_query=None, *args, **kwargs):
        """
        初始化公共属性
        """
        self.kwargs = kwargs
        self.logger = kwargs.get('logger', logging.getLogger(__name__))
        self.adapter_supports_queries = True
        self.base_query = None

    def get_model(self, model_name):
        """
        根据数据库名字返回数据库模型
        """

        # 数据库名必须小写
        model_name = model_name.lower()

        kwarg_model_key = '%s_model' % (model_name,)

        if kwarg_model_key in self.kwargs:
            return self.kwargs.get(kwarg_model_key)

        get_model_method = getattr(self, 'get_%s_model' % (model_name,))

        return get_model_method()

    def generate_base_query(self, chatterbot, session_id):
        """
        为存储数据库创建基本查询
        """
        if self.adapter_supports_queries:
            for filter_instance in chatterbot.filters:
                self.base_query = filter_instance.filter_selection(chatterbot, session_id)

    def count(self):
        """
        返回数据库中的条目数
        """
        raise self.AdapterMethodNotImplementedError(
            'The `count` method is not implemented by this adapter.'
        )

    def find(self, statement_text):
        """
        查询，如果存在返回查询对象
        """
        raise self.AdapterMethodNotImplementedError(
            'The `find` method is not implemented by this adapter.'
        )

    def remove(self, statement_text):
        """
        删除指定文本
        """
        raise self.AdapterMethodNotImplementedError(
            'The `remove` method is not implemented by this adapter.'
        )

    def filter(self, **kwargs):
        """
        返回数据库中的对象列表
        """
        raise self.AdapterMethodNotImplementedError(
            'The `filter` method is not implemented by this adapter.'
        )

    def update(self, statement):
        """
        更新数据库
        """
        raise self.AdapterMethodNotImplementedError(
            'The `update` method is not implemented by this adapter.'
        )

    def get_latest_response(self, conversation_id):
        """
        获取最新响应
        """
        raise self.AdapterMethodNotImplementedError(
            'The `get_latest_response` method is not implemented by this adapter.'
        )

    def create_conversation(self):
        """
        创建会话
        """
        raise self.AdapterMethodNotImplementedError(
            'The `create_conversation` method is not implemented by this adapter.'
        )

    def add_to_conversation(self, conversation_id, statement, response):
        """
        将新语句添加到会话
        """
        raise self.AdapterMethodNotImplementedError(
            'The `add_to_conversation` method is not implemented by this adapter.'
        )

    def get_random(self):
        """
        从数据库中随机获取对话
        """
        raise self.AdapterMethodNotImplementedError(
            'The `get_random` method is not implemented by this adapter.'
        )

    def drop(self):
        """
        删除连接到指定适配器的数据库
        """
        raise self.AdapterMethodNotImplementedError(
            'The `drop` method is not implemented by this adapter.'
        )

    def get_response_statements(self):
        """
        获取响应语句
        """
        statement_list = self.filter()

        responses = set()
        to_remove = list()
        for statement in statement_list:
            for response in statement.in_response_to:
                responses.add(response.text)
        for statement in statement_list:
            if statement.text not in responses:
                to_remove.append(statement)

        for statement in to_remove:
            statement_list.remove(statement)

        return statement_list

    class EmptyDatabaseException(Exception):

        def __init__(self,
                     value='The database currently contains no entries. At least one entry is expected. You may need to train your chat bot to populate your database.'):
            self.value = value

        def __str__(self):
            return repr(self.value)

    class AdapterMethodNotImplementedError(NotImplementedError):
        """
        适配器方法未实现错误
        """
        pass
