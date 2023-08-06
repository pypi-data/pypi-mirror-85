# -*- coding:utf-8 -*-
from peewee import SqliteDatabase, PostgresqlDatabase, MySQLDatabase
from elasticsearch import Elasticsearch
from impalet import ImpalaClient, ImpalaDatabase


class EnumDataBase:
    PG = 'PostgreSQL'
    MYSQL = 'MySql'
    SQLITE = 'SQLite'
    ES = 'Elasticsearch'
    IMPALA = 'Impala'


class RestSqlDb(object):

    def __init__(self, db_setting):
        db_type = db_setting.get('type', None)
        db = None
        if db_type == EnumDataBase.PG:
            # 初始化pg链接实例
            self._check_db_setting(setting=db_setting, check_fields=['db_name', 'name', 'type', 'host', 'port', 'schema', 'user', 'password'])
            db = PostgresqlDatabase(
                db_setting['db_name'],
                user=db_setting['user'],
                password=db_setting['password'],
                host=db_setting['host'],
                port=db_setting['port']
            )
        elif db_type == EnumDataBase.MYSQL:
            self._check_db_setting(setting=db_setting,
                                   check_fields=['db_name', 'name', 'host', 'port', 'user', 'tables',
                                                 'password'])
            db = MySQLDatabase(
                db_setting['db_name'],
                user=db_setting['user'],
                password=db_setting['password'],
                host=db_setting['host'],
                port=db_setting['port']
            )
        elif db_type == EnumDataBase.SQLITE:
            # 初始化sqlite实例
            self._check_db_setting(setting=db_setting, check_fields=['name', 'host', 'tables'])
            db = SqliteDatabase(db_setting['host'])
        elif db_type == EnumDataBase.ES:
            # 初始化es实例
            self._check_db_setting(setting=db_setting, check_fields=['name', 'host', 'tables'])
            db = Elasticsearch(db_setting['host'])
        elif db_type == EnumDataBase.IMPALA:
            self._check_db_setting(setting=db_setting, check_fields=['name', 'host', 'tables'])
            db = ImpalaDatabase("impala")
            self.impala_client = ImpalaClient(db_setting['host'], db_setting['port'], db_setting['db_name'])
        else:
            raise RuntimeError('db type is invalid')
        if db:
            self.type = db_type
            self.name = db_setting['name']
            self.tables = db_setting['tables']
            self.db = db
            self.schema = db_setting.get('schema', None)

    @staticmethod
    def _check_db_setting(setting, check_fields):
        for field in check_fields:
            if setting.get(field, None) is None:
                raise RuntimeError('db setting need field: {}'.format(field))






