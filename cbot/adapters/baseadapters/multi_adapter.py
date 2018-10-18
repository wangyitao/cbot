from collections import Counter
from ...utils import utils
from .adapter import Adapter


class MultiAdapter(Adapter):
    """
    多适配器
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 适配器列表
        self.adapters = []

        # 必须的适配器列表
        self.system_adapters = []

    def get_initialization_functions(self):
        """
        初始化每个适配器
        """
        functions_dict = {}

        # 遍历每个适配器，并获需要初始化的所有函数
        for logic_adapter in self.get_adapters():
            functions = logic_adapter.get_initialization_functions()
            functions_dict.update(functions)

        return functions_dict

    def process(self, statement):
        """
        返回逻辑适配器对语句的响应
        :param statement: 需要处理的语句
        """
        results = []
        result = None
        max_confidence = -1

        for adapter in self.get_adapters():
            if adapter.can_process(statement):

                output = adapter.process(statement)
                results.append((output.confidence, output,))

                self.logger.info(
                    '{} selected "{}" as a response with a confidence of {}'.format(
                        adapter.class_name, output.text, output.confidence
                    )
                )

                if output.confidence > max_confidence:
                    result = output
                    max_confidence = output.confidence
            else:
                self.logger.info(
                    'Not processing the statement using {}'.format(adapter.class_name)
                )

        # 　如果多个适配器返回一样的响应则，这种回答更准确
        if len(results) >= 3:
            statements = [s[1] for s in results]
            count = Counter(statements)
            most_common = count.most_common()
            if most_common[0][1] > 1:
                result = most_common[0][0]
                max_confidence = self.get_greatest_confidence(result, results)

        result.confidence = max_confidence
        return result

    def get_greatest_confidence(self, statement, options):
        """
        返回一组语句的最大置信度

        :param statement: 语句对象
        :param options: 元组,比如： (confidence, statement).
        """
        values = []
        for option in options:
            if option[1] == statement:
                values.append(option[0])

        return max(values)

    def get_adapters(self):
        """
        获取所有的适配器
        """
        adapters = []
        adapters.extend(self.adapters)
        adapters.extend(self.system_adapters)
        return adapters

    def add_adapter(self, adapter, **kwargs):
        """
        添加逻辑适配器

        :param adapter: 需要添加的适配器
        :type adapter: `LogicAdapter`
        """
        utils.initialize_adapter_class(adapter, Adapter)
        adapter = utils.initialize_class(adapter, **kwargs)
        self.adapters.append(adapter)

    def insert_adapter(self, adapter, insert_index, **kwargs):
        """
        在指定索引处添加逻辑适配器

        :param logic_adapter: 适配器导入路径
        :type logic_adapter: str

        :param insert_index: 需要插入的位置
        :type insert_index: int
        """
        utils.initialize_adapter_class(adapter, Adapter)
        NewAdapter = utils.import_module(adapter)
        adapter_ = NewAdapter(**kwargs)
        self.adapters.insert(insert_index, adapter_)

    def remove_logic_adapter(self, adapter_name):
        """
        取消适配器的绑定

        :param adapter_name: 需要移除的适配器
        :type adapter_name: str
        """
        for index, adapter in enumerate(self.adapters):
            if adapter_name == type(adapter).__name__:
                del self.adapters[index]
                return True
        return False

    def set_cbot(self, cbot):
        """
        将适配器绑定cbot
        """
        super().set_cbot(cbot)

        for adapter in self.get_adapters():
            adapter.set_cbot(cbot)
