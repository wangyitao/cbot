# -*- coding: utf-8 -*-

"""
语句预处理
"""


def clean_whitespace(chatbot, statement):
    """
    删除空白
    """

    statement.text = statement.text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('  ', ' ')
    statement.text = statement.text.strip()
    return statement


def unescape_html(cbot, statement):
    """
    处理html中的空白
    如: "&lt;b&gt;" becomes "<b>".
    """

    import html
    statement.text = html.unescape(statement.text)
    return statement

