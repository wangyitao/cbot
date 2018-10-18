from ..baseadapters import BaseAdapter


class OutputAdapter(BaseAdapter):
    """
    所有输出适配器的基类
    """

    def process_response(self, statement, session_id=None):
        """
        在子类重写，以实现自定义功能

        :param statement: cbot响应输入
        :param session_id: 聊天会话的唯一id

        :returns: 响应语句
        """
        return statement
