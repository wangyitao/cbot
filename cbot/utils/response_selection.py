# -*- coding: utf-8 -*-

"""
选择以哪种方式返回响应结果
"""
import logging


def get_most_frequent_response(input_statement, response_list):
    """
    返回频率最高的回复
    :param input_statement: 输入语句
    :param response_list: 回复列表
    :return: 回复结果
    """
    matching_response = None
    occurrence_count = -1

    logger = logging.getLogger(__name__)
    logger.info(u'Selecting response with greatest number of occurrences.')

    # 可以优化
    for statement in response_list:
        count = statement.get_response_count(input_statement)  # 返回次数
        if count >= occurrence_count:
            matching_response, occurrence_count = statement, count

    return matching_response


def get_first_response(input_statement, response_list):
    """
    选择匹配的第一项
    :param input_statement:
    :param response_list:
    :return:
    """
    logger = logging.getLogger(__name__)
    logger.info(u'Selecting first response from list of {} options.'.format(
        len(response_list)
    ))
    return response_list[0]


def get_random_response(input_statement, response_list):
    """
    随机选择返回值
    :param input_statement: 输入
    :param response_list: 回复列表
    :return:
    """
    from random import choice
    logger = logging.getLogger(__name__)
    logger.info(u'Selecting a response from list of {} options.'.format(
        len(response_list)
    ))
    return choice(response_list)
