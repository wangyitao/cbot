from ..baseadapters import BaseAdapter


class InputAdapter(BaseAdapter):
    """
    所有输入适配器都要实现的接口
    """

    def process_input(self, *args, **kwargs):
        """
        基于输入源返回语句对象
        """
        raise self.AdapterMethodNotImplementedError()

    def process_input_statement(self, *args, **kwargs):
        """
        返回一个现有的语句对象（如果存在的话）
        """
        input_statement = self.process_input(*args, **kwargs)

        self.logger.info('Received input statement: {}'.format(input_statement.text))

        existing_statement = self.cbot.storage.find(input_statement.text)

        if existing_statement:
            self.logger.info('"{}" is a known statement'.format(input_statement.text))
            input_statement = existing_statement
        else:
            self.logger.info('"{}" is not a known statement'.format(input_statement.text))

        return input_statement
