# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr, declarative_base

from ...utils.constants import TAG_NAME_MAX_LENGTH, STATEMENT_TEXT_MAX_LENGTH
from ...ext.sqlalchemy_app.types import UnicodeString
from ...utils.conversation import StatementMixin


class ModelBase(object):
    """
    数据库模块的父类
    """

    @declared_attr
    def __tablename__(cls):
        """
        创建数据表名
        """
        return cls.__name__.lower()

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


# 创建对象的基类
Base = declarative_base(cls=ModelBase)

# 创建表
tag_association_table = Table(
    'tag_association',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id')),
    Column('statement_id', Integer, ForeignKey('statement.id'))
)


class Tag(Base):
    """
    创建描述标签
    """

    name = Column(UnicodeString(TAG_NAME_MAX_LENGTH))


class Statement(Base, StatementMixin):
    """
    语句类
    """

    # 文本
    text = Column(UnicodeString(STATEMENT_TEXT_MAX_LENGTH), unique=True)

    # 标签
    tags = relationship(
        'Tag',
        secondary=lambda: tag_association_table,
        backref='statements'
    )

    # 额外数据
    extra_data = Column(PickleType)

    in_response_to = relationship(
        'Response',
        back_populates='statement_table'
    )

    def get_tags(self):
        """
        获取标签列表
        """
        return [tag.name for tag in self.tags]

    def get_statement(self):
        """
        获取语句
        """
        from ...utils.conversation import Statement as StatementObject
        from ...utils.conversation import Response as ResponseObject

        statement = StatementObject(
            self.text,
            tags=[tag.name for tag in self.tags],
            extra_data=self.extra_data
        )

        for response in self.in_response_to:
            statement.add_response(
                ResponseObject(text=response.text, occurrence=response.occurrence)
            )

        return statement


class Response(Base):
    """
    对给定语句响应
    """

    text = Column(UnicodeString(STATEMENT_TEXT_MAX_LENGTH))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    occurrence = Column(Integer, default=1)

    statement_text = Column(UnicodeString(STATEMENT_TEXT_MAX_LENGTH), ForeignKey('statement.text'))

    statement_table = relationship(
        'Statement',
        back_populates='in_response_to',
        cascade='all',
        uselist=False
    )


conversation_association_table = Table(
    'conversation_association',
    Base.metadata,
    Column('conversation_id', Integer, ForeignKey('conversation.id')),
    Column('statement_id', Integer, ForeignKey('statement.id'))
)


class Conversation(Base):
    """
    会话对象
    """

    statements = relationship(
        'Statement',
        secondary=lambda: conversation_association_table,
        backref='conversations'
    )
