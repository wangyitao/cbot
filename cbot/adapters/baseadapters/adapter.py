from .base_adapter import BaseAdapter
from ...utils.utils import import_module


class Adapter(BaseAdapter):
    """
    所有逻辑适配器都要实现的类
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from ...utils.comparisons import levenshtein_distance
        from ...utils.response_selection import get_first_response

        # 设置默认的适配器
        if 'statement_comparison_function' in kwargs:
            import_path = kwargs.get('statement_comparison_function')
            if isinstance(import_path, str):
                kwargs['statement_comparison_function'] = import_module(import_path)

        if 'response_selection_method' in kwargs:
            import_path = kwargs.get('response_selection_method')
            if isinstance(import_path, str):
                kwargs['response_selection_method'] = import_module(import_path)

        # 默认使用levenshtein_distance来比较相似度
        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            levenshtein_distance
        )

        # 默认使用置信度最高的对话
        self.select_response = kwargs.get(
            'response_selection_method',
            get_first_response
        )

    def get_initialization_functions(self):
        """
        当cbot运行以字典的形式返回需要执行的方法
        """
        return self.compare_statements.get_initialization_functions()

    def initialize(self):
        """
        初始化
        :return:
        """
        for function in self.get_initialization_functions().values():
            function()

    def can_process(self, statement):
        """
        判断适配器是否可以执行给定语句
        :rtype: 默认True
        """
        return True

    def process(self, statement):
        """
        实现逻辑，子类必须重写
        返回一个置信度和响应语句
        置信度在0-1之间

        :param statement: 需要处理的输入语句
        :type statement: Statement
        :rtype: Statement
        """
        raise self.AdapterMethodNotImplementedError()

    @property
    def class_name(self):
        """
        返回适配器的名称
        """
        return str(self.__class__.__name__)

    class EmptyDatasetException(Exception):

        def __init__(self, value='An empty set was received when at least one statement was expected.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
