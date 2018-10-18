import logging


class BaseAdapter(object):
    """
    所有适配器的基类
    """

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger', logging.getLogger(__name__))
        self.cbot = kwargs.get('cbot')

    def set_cbot(self, cbot):
        """
        给适配器绑定cbot实例
        :param cbot: cbot实例.
        :type cbot: CBot
        """
        self.cbot = cbot

    class AdapterMethodNotImplementedError(NotImplementedError):
        """
        没有实现适配器方法时引发异常
        """

        def __init__(self, message=None):
            """
            设置异常信息
            """
            if not message:
                message = 'This method must be overridden in a subclass method.'
            self.message = message

        def __str__(self):
            return self.message

    class InvalidAdapterTypeException(Exception):
        """
        接收到非适配器类型异常
        """
        pass
