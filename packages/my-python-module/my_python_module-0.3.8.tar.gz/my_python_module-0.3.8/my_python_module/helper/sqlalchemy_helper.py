#!/usr/bin/env python
# -*-coding:utf-8-*-
import copy
import logging

from sqlalchemy.engine.url import URL
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.engine import reflection

logger = logging.getLogger(__name__)


class NoSuchTableError(Exception):
    pass


class SQLDataBase(object):
    def __init__(self, dburl, loadtables='ALL', orm=True, **kwargs):
        """
        创建连接 db 的连接对象, 数据库不存在时自动创建

        self._engine
        self._conn
        self._meta
        self._session
        self.execute  执行
        self.all_tables 所有table name
        self.get_table(table_name) 返回sqlalchemy的Table对象，内省，会更加健壮，也更加底层


        :param dburl: 连接数据库的 URL, 格式为:
                    dialect[+driver]://user:password@host/  # 注意需要以斜杠结尾
        :param kw:
        :return:
        """
        self._orm = orm
        self._engine = create_engine(dburl)
        self._conn = self._engine.connect()
        self._meta = MetaData(bind=self._engine)
        self._session = Session(self._engine)

        if self._orm:
            self._AutoBase = automap_base(metadata=self._meta)

            if loadtables == 'ALL':
                self._meta.reflect()
            elif loadtables:
                self.reflect(loadtables)

            self._AutoBase.prepare()

    def all_tables(self):
        """
        当前sql数据库实际有的表格名列表。
        """
        if self._orm:
            return list(self._AutoBase.classes)
        else:
            self.insp = reflection.Inspector.from_engine(self._engine)
            return self.insp.get_table_names()

    def get_table(self, table_name):
        """
        获取sqlalchemy的Table对象
        :param table_name:
        :return:
        """
        if self._orm:
            self.reflect(table_name)
            return self._AutoBase.classes.get(table_name)
        else:
            try:
                return Table(table_name, self._meta, autoload=True)
            except NoSuchTableError:
                raise ValueError('No Such table name.')

    def reflect(self, only):
        """
        如果已经reflect了的将会pass掉
        """
        if isinstance(only, (list, tuple, set)):
            self._meta.reflect(only=only)
        elif isinstance(only, str):
            self._meta.reflect(only=[only])
        else:
            raise Exception("wrong type {}".format(type(only)))

    def create_table(self, table_name, columns):
        """
        创建 table, 如果 table 已存在, 则无任何动作
        :param table_name:
        :param columns:
        :return:
        """
        if table_name not in self._meta.tables:
            # deepcopy 的原因: 一个 Column object 引用的只能用于创建一个表, 这是 sqlalchemy 的机制
            table = Table(table_name, self._meta, *copy.deepcopy(columns))
            table.create(checkfirst=True)

    def insert_data(self, table_name, data):
        """
        往指定表插入数据

        当表不存在时, self.tables[table_name] 会报 KeyError 错误,
        其中 KeyError.message 为表名字, 可以捕捉这个错误来动态创建需要的表
        :param table_name:
        :param data: data 为数组形式的字典
        :return:
        """
        _table = self._meta.tables[table_name]
        self._conn.execute(_table.insert_child(), data)

    def execute(self, statement, *multiparams, **params):
        """
        执行 sql 语句
        :param statement:
        :return:
        """
        return self._conn.execute(statement, *multiparams, **params)

    def close(self):
        """
        关闭 proxy conn
        :return:
        """
        self._conn.close()

    @property
    def session(self):
        return self._session


def create_sqlalchemy_url(drivername, username=None, password=None, host=None,
                          port=None, database=None, **kwargs):
    """
    输出一个 sqlalchemy的 url，有一些额外的优化。

    :param drivername:
    :param username:
    :param password:
    :param host:
    :param port:
    :param database:
    :param kwargs:
    :return:
    """
    if drivername.startswith('mysql') and 'charset' not in kwargs:
        kwargs['charset'] = 'utf8mb4'

    dburl = URL(drivername, username=username, password=password, host=host,
                port=port, database=database, query=kwargs)

    return dburl


def insert_or_ignore(session, orm, item, unique_key, return_key=None):
    """
    sql常用操作  插入或者忽略

    unique_key 指定判断记录唯一性的字段

    return_key 指定返回记录的字段 默认None，对返回记录没有特别的要求，或者指定一个字段名来返回
    :param session:
    :param orm:
    :param item:
    :param unique_key:
    :param return_key:
    :return: True inserted False ignore
    """
    key = {}
    if isinstance(unique_key, list):
        for k in unique_key:
            key[k] = item[k]
    else:
        key[unique_key] = item[unique_key]

    q = session.query(orm).filter_by(**key).first()

    if not q:  # insert or ignore
        session.add(orm(**item))
        session.commit()

        # fluentd_logger.send('sqldb_{0}'.format(orm.__tablename__), {'op_name': 'insert', 'op_data': item })

        if not return_key:
            logger.debug('insert a record to sql database.')
            return True, None
        else:
            first = session.query(orm).filter_by(**key).first()

            return_key = getattr(first, return_key)
            logger.debug('insert {0} to sql database.'.format(return_key))
            return True, return_key
    else:
        if not return_key:
            logger.debug('record already exist in sql database.')
            return False, None  # True表示记录已存在，有的时候有用
        else:
            return_key = getattr(q, return_key)
            logger.debug(
                'record {0} already exist in sql database.'.format(return_key))
            return False, return_key


def insert_or_update(session, orm, item, unique_key,
                     update_check=lambda target, item: True):
    """
    sql 常用操作 插入或者更新逻辑

    update_check 默认把匹配到的记录作为第一个参数传过去，方便进行一些逻辑判断，然后决定是否更新记录

    返回 None,info
    或者 True, 'updated'
    :param session:
    :param orm:
    :param item:
    :param unique_key:
    :return: True 表示已经插入或者更新了 None 表示什么都没有 info updated 有更详细的信息
    """
    key = {}
    if isinstance(unique_key, list):
        for k in unique_key:
            key[k] = item[k]
    else:
        key[unique_key] = item[unique_key]

    q = session.query(orm).filter_by(**key).first()

    if not q:
        session.add(orm(**item))
        session.commit()

        # fluentd_logger.send('sqldb_{0}'.format(orm.__tablename__), {'op_name': 'insert', 'op_data': item})
        logger.debug('insert a record to sql database.')
        return True, 'inserted'
    else:
        if update_check(q, item):
            for k, v in item.items():
                setattr(q, k, v)
            session.commit()

            # fluentd_logger.send('sqldb_{0}'.format(orm.__tablename__), {'op_name': 'update', 'op_data': item})
            logger.debug('updated a record in sql database.')
            return True, 'updated'
        else:
            logger.debug('update_check is not satisfied.')
            return None, 'passed'


def update_one(session, orm, item, unique_key):
    """
    更新一条记录
    :param session:
    :param orm:
    :param unique_key:
    :return:
    """
    key = {}
    if isinstance(unique_key, list):
        for k in unique_key:
            key[k] = item[k]
    else:
        key[unique_key] = item[unique_key]

    q = session.query(orm).filter_by(**key).first()

    if not q:
        return None
    else:
        for k, v in item.items():
            setattr(q, k, v)
        session.commit()

        logger.debug('updated a record in sql database.')
        return True
