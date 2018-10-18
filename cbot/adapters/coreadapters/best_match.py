from ..baseadapters import Adapter


class BestMatch(Adapter):
    """
    最佳匹配
    """

    def get(self, input_statement):
        """
        获取语句字符串和语句字符串列表
        从列表中返回最佳匹配语句
        """
        statement_list = self.cbot.storage.get_response_statements()

        if not statement_list:
            if self.cbot.storage.count():
                # 使用随机抽取语句
                self.logger.info(
                    'No statements have known responses. ' +
                    'Choosing a random response to return.'
                )
                random_response = self.cbot.storage.get_random()
                random_response.confidence = 0
                return random_response
            else:
                raise self.EmptyDatasetException()

        closest_match = input_statement
        closest_match.confidence = 0

        # 找到最接近的已知语句
        for statement in statement_list:
            confidence = self.compare_statements(input_statement, statement)

            if confidence > closest_match.confidence:
                statement.confidence = confidence
                closest_match = statement

        return closest_match

    def can_process(self, statement):
        """
        检查机器人的存储适配器是否可用
        """
        return self.cbot.storage.count()

    def process(self, input_statement):

        # 选择最佳输入语句匹配项
        closest_match = self.get(input_statement)
        self.logger.info('Using "{}" as a close match to "{}"'.format(
            input_statement.text, closest_match.text
        ))

        # 获取响应最佳匹配的所有语句
        response_list = self.cbot.storage.filter(
            in_response_to__contains=closest_match.text
        )

        if response_list:
            self.logger.info(
                'Selecting response from {} optimal responses.'.format(
                    len(response_list)
                )
            )
            response = self.select_response(input_statement, response_list)
            response.confidence = closest_match.confidence
            self.logger.info('Response selected. Using "{}"'.format(response.text))
        else:
            response = self.cbot.storage.get_random()
            self.logger.info(
                'No response to "{}" found. Selecting a random response.'.format(
                    closest_match.text
                )
            )

            # 设置置信度为０，因为是随机响应
            response.confidence = 0

        return response
