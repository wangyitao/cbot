from ..baseadapters import Adapter


class NoKnowledgeAdapter(Adapter):
    """
    这个是必须要添加的适配器
    """

    def process(self, statement):
        """
        如果数据库中没有已知的响应，返回输入内容
        """

        if self.cbot.storage.count():
            statement.confidence = 0
        else:
            statement.confidence = 1

        return statement
