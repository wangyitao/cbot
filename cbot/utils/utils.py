# -*- coding: utf-8 -*-

"""
cbot常用工具
"""


def import_module(path):
    """
    基于指定的模块导入
    点分割模块的导入路径。
    """
    import importlib

    module_path, module = str(path).rsplit('.', maxsplit=1)
    return getattr(importlib.import_module(module_path), module)


def initialize_class(data, **kwargs):
    """
    :param data: 类的路径
    """
    if isinstance(data, dict):
        import_path = data.get('import_path')
        data.update(kwargs)
        class_ = import_module(import_path)

        return class_(**data)
    else:
        class_ = import_module(data)

        return class_(**kwargs)


def initialize_adapter_class(initialize_class, adapter_class):
    """
    初始化适配器
    :param initialize_class: 初始化
    :param adapter_class: 适配器类
    :return:
    """
    from ..adapters import BaseAdapter

    # 如果是字典，并且存在import_part，则导入
    if isinstance(initialize_class, dict):

        if 'import_path' not in initialize_class:
            raise BaseAdapter.InvalidAdapterTypeException(
                'The dictionary {} must contain a value for "import_path"'.format(
                    str(initialize_class)
                )
            )

        # Set the class to the import path for the next check
        initialize_class = initialize_class.get('import_path')

    if not issubclass(import_module(initialize_class), adapter_class):
        raise BaseAdapter.InvalidAdapterTypeException(
            '{} must be a subclass of {}'.format(
                initialize_class,
                adapter_class.__name__
            )
        )


def input_function():
    """
    输入
    """
    return input().strip()


def remove_stopwords(tokens, language):
    """
    去除中文结束词
    """
    from .stopwords import stopwords

    # 删除结束词
    tokens = set(tokens) - set(stopwords)

    return tokens


def get_response_time(cbot):
    """
    获取响应时间
    """
    import time

    start_time = time.time()

    cbot.get_response('Hello')

    return time.time() - start_time


def print_progress_bar(description, iteration_counter, total_items, progress_bar_length=20):
    """
    输出进度条程序
    """
    import sys

    percent = float(iteration_counter) / total_items
    hashes = '>' * int(round(percent * progress_bar_length))
    spaces = ' ' * (progress_bar_length - len(hashes))
    sys.stdout.write("\r{0}: [{1}] {2}%".format(description, hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()
    if total_items == iteration_counter:
        print("\r")
