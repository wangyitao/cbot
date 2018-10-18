# -*- coding: utf-8 -*-

from sqlalchemy.types import TypeDecorator, Unicode


class UnicodeString(TypeDecorator):
    """
    保证字符串
    """
    impl = Unicode

    def process_bind_param(self, value, dialect):
        """
        返回字符串
        """
        return str(value)
