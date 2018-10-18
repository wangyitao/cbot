# -*- coding: utf-8 -*-

"""
比较算法
"""

# 如果可能使用 python-Levenshtein库比较
try:
    from Levenshtein.StringMatcher import StringMatcher as SequenceMatcher
except ImportError:
    from difflib import SequenceMatcher


class Comparator:

    def __call__(self, statement_a, statement_b):
        return self.compare(statement_a, statement_b)

    def compare(self, statement_a, statement_b):
        return 0

    def get_initialization_functions(self):
        """
        获得所有的初始化方法
        """
        initialization_methods = [
            (
                method,
                getattr(self, method),
            ) for method in dir(self) if method.startswith('initialize_')
        ]

        return {
            key: value for (key, value) in initialization_methods
        }

# 编辑距离
class LevenshteinDistance(Comparator):
    """
    Compare two statements based on the Levenshtein distance
    of each statement's text.

    For example, there is a 65% similarity between the statements
    "where is the post office?" and "looking for the post office"
    based on the Levenshtein distance algorithm.
    """

    def compare(self, statement, other_statement):
        """
        比较两个输入

        :return: 返回两个句子之间的相似度
        :rtype: 浮点型
        """

        # Return 0 if either statement has a falsy text value
        if not statement.text or not other_statement.text:
            return 0

        statement_text = str(statement.text.lower())
        other_statement_text = str(other_statement.text.lower())

        similarity = SequenceMatcher(
            None,
            statement_text,
            other_statement_text
        )

        # Calculate a decimal percent of the similarity
        percent = round(similarity.ratio(), 2)

        return percent


# ---------------------------------------- #
levenshtein_distance = LevenshteinDistance()
