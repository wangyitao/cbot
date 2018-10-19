from . import InputAdapter
from ...utils.conversation import Statement


class VariableInputTypeAdapter(InputAdapter):
    TEXT = 'text'

    def detect_type(self, statement):

        if isinstance(statement, str):
            return self.TEXT

        raise self.UnrecognizedInputFormatException(
            'The type {} is not recognized as a valid input type.'.format(
                type(statement)
            )
        )

    def process_input(self, statement):
        input_type = self.detect_type(statement)

        # 将输入字符串转换为语句对象
        if input_type == self.TEXT:
            return Statement(statement)

    class UnrecognizedInputFormatException(Exception):
        """
        输入非字符串异常
        """

        def __init__(self, value='The input format was not recognized.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
