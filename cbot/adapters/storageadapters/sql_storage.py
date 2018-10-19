from ..storageadapters import StorageAdapter


def get_response_table(response):
    from ...ext.sqlalchemy_app.models import Response
    return Response(text=response.text, occurrence=response.occurrence)


class SQLStorageAdapter(StorageAdapter):
    """
    该类允许聊天机器人存储会话数据
    默认使用SQLite数据库
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        # 　sqlite数据库默认路径
        default_uri = "sqlite:///db.sqlite3"

        database_name = self.kwargs.get("database", False)

        # 如果database_name未指定，使用默认的
        if database_name is None:
            default_uri = "sqlite://"

        self.database_uri = self.kwargs.get(
            "database_uri", default_uri
        )

        # 如果提供数据库名称，创建SQLite文件
        if database_name:
            self.database_uri = "sqlite:///" + database_name

        self.engine = create_engine(self.database_uri, convert_unicode=True)

        from re import search

        if search('^sqlite://', self.database_uri):
            from sqlalchemy.engine import Engine
            from sqlalchemy import event

            @event.listens_for(Engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                dbapi_connection.execute('PRAGMA journal_mode=WAL')
                dbapi_connection.execute('PRAGMA synchronous=NORMAL')

        self.read_only = self.kwargs.get(
            "read_only", False
        )

        if not self.engine.dialect.has_table(self.engine, 'Statement'):
            self.create()

        self.Session = sessionmaker(bind=self.engine, expire_on_commit=True)

        # 目前尚不支持内部查询
        self.adapter_supports_queries = False

    def get_statement_model(self):
        """
        返回语句
        """
        from ...ext.sqlalchemy_app.models import Statement
        return Statement

    def get_response_model(self):
        """
        返回响应
        """
        from ...ext.sqlalchemy_app.models import Response
        return Response

    def get_conversation_model(self):
        """
        返回会话
        """
        from ...ext.sqlalchemy_app.models import Conversation
        return Conversation

    def get_tag_model(self):
        """
        返回标签
        """
        from ...ext.sqlalchemy_app.models import Tag
        return Tag

    def count(self):
        """
        返回语句在数据库中的数目
        """
        Statement = self.get_model('statement')

        session = self.Session()
        statement_count = session.query(Statement).count()
        session.close()
        return statement_count

    def find(self, statement_text):
        """
        查询，如果存在，返回结果，否则，返回None
        """
        Statement = self.get_model('statement')
        session = self.Session()

        query = session.query(Statement).filter_by(text=statement_text)
        record = query.first()
        if record:
            statement = record.get_statement()
            session.close()
            return statement

        session.close()
        return None

    def remove(self, statement_text):
        """
        移除匹配的语句
        """
        Statement = self.get_model('statement')
        session = self.Session()

        query = session.query(Statement).filter_by(text=statement_text)
        record = query.first()

        session.delete(record)

        self._session_finish(session)

    def filter(self, **kwargs):
        """
        返回数据库中的对象列表
        """
        Statement = self.get_model('statement')
        Response = self.get_model('response')

        session = self.Session()

        filter_parameters = kwargs.copy()

        statements = []
        _query = None

        if len(filter_parameters) == 0:
            _response_query = session.query(Statement)
            statements.extend(_response_query.all())
        else:
            for i, fp in enumerate(filter_parameters):
                _filter = filter_parameters[fp]
                if fp in ['in_response_to', 'in_response_to__contains']:
                    _response_query = session.query(Statement)
                    if isinstance(_filter, list):
                        if len(_filter) == 0:
                            _query = _response_query.filter(
                                Statement.in_response_to == None  # NOQA Here must use == instead of is
                            )
                        else:
                            for f in _filter:
                                _query = _response_query.filter(
                                    Statement.in_response_to.contains(get_response_table(f)))
                    else:
                        if fp == 'in_response_to__contains':
                            _query = _response_query.join(Response).filter(Response.text == _filter)
                        else:
                            _query = _response_query.filter(Statement.in_response_to == None)  # NOQA
                else:
                    if _query:
                        _query = _query.filter(Response.statement_text.like('%' + _filter + '%'))
                    else:
                        _response_query = session.query(Response)
                        _query = _response_query.filter(Response.statement_text.like('%' + _filter + '%'))

                if _query is None:
                    return []
                if len(filter_parameters) == i + 1:
                    statements.extend(_query.all())

        results = []

        for statement in statements:
            if isinstance(statement, Response):
                if statement and statement.statement_table:
                    results.append(statement.statement_table.get_statement())
            else:
                if statement:
                    results.append(statement.get_statement())

        session.close()

        return results

    def update(self, statement):
        """
        修改数据库中的内容
        如果内容不存在，则创建一个条目
        """
        Statement = self.get_model('statement')
        Response = self.get_model('response')
        Tag = self.get_model('tag')

        if statement:
            session = self.Session()

            query = session.query(Statement).filter_by(text=statement.text)
            record = query.first()

            # 如果一个新的语句条目不存在，创建一个条目
            if not record:
                record = Statement(text=statement.text)

            record.extra_data = dict(statement.extra_data)

            for _tag in statement.tags:
                tag = session.query(Tag).filter_by(name=_tag).first()

                if not tag:
                    # 创建标签
                    tag = Tag(name=_tag)

                record.tags.append(tag)

            # 根据需要获取或者创建响应记录
            for response in statement.in_response_to:
                _response = session.query(Response).filter_by(
                    text=response.text,
                    statement_text=statement.text
                ).first()

                if _response:
                    _response.occurrence += 1
                else:
                    # 创建响应
                    _response = Response(
                        text=response.text,
                        statement_text=statement.text,
                        occurrence=response.occurrence
                    )

                record.in_response_to.append(_response)

            session.add(record)

            self._session_finish(session)

    def create_conversation(self):
        """
        创建一个新的会话。
        """
        Conversation = self.get_model('conversation')

        session = self.Session()
        conversation = Conversation()

        session.add(conversation)
        session.flush()

        session.refresh(conversation)
        conversation_id = conversation.id

        session.commit()
        session.close()

        return conversation_id

    def add_to_conversation(self, conversation_id, statement, response):
        """
        添加响应和语句
        """
        Statement = self.get_model('statement')
        Conversation = self.get_model('conversation')

        session = self.Session()
        conversation = session.query(Conversation).get(conversation_id)

        statement_query = session.query(Statement).filter_by(
            text=statement.text
        ).first()
        response_query = session.query(Statement).filter_by(
            text=response.text
        ).first()

        # 确保语句存在
        if not statement_query:
            self.update(statement)
            statement_query = session.query(Statement).filter_by(
                text=statement.text
            ).first()

        if not response_query:
            self.update(response)
            response_query = session.query(Statement).filter_by(
                text=response.text
            ).first()

        conversation.statements.append(statement_query)
        conversation.statements.append(response_query)

        session.add(conversation)
        self._session_finish(session)

    def get_latest_response(self, conversation_id):
        """
        如果存在会话，返回最新响应，否则返回None
        """
        Statement = self.get_model('statement')

        session = self.Session()
        statement = None

        statement_query = session.query(Statement).filter(
            Statement.conversations.any(id=conversation_id)
        ).order_by(Statement.id)

        if statement_query.count() >= 2:
            statement = statement_query[-2].get_statement()

        # 处理列表中第一条语句的情况
        elif statement_query.count() == 1:
            statement = statement_query[0].get_statement()

        session.close()

        return statement

    def get_random(self):
        """
        从数据库中返回一个随机语句
        """
        import random

        Statement = self.get_model('statement')

        session = self.Session()
        count = self.count()
        if count < 1:
            raise self.EmptyDatabaseException()

        rand = random.randrange(0, count)
        stmt = session.query(Statement)[rand]

        statement = stmt.get_statement()

        session.close()
        return statement

    def drop(self):
        """
        删除连接到指定数据库的适配器
        """
        from ...ext.sqlalchemy_app.models import Base
        Base.metadata.drop_all(self.engine)

    def create(self):
        """
        填充数据库
        """
        from ...ext.sqlalchemy_app.models import Base
        Base.metadata.create_all(self.engine)

    def _session_finish(self, session, statement_text=None):
        from sqlalchemy.exc import InvalidRequestError
        try:
            if not self.read_only:
                session.commit()
            else:
                session.rollback()
        except InvalidRequestError:
            # 记录语句文本和异常
            self.logger.exception(statement_text)
        finally:
            session.close()
