# -*- coding:utf-8 -*-
from peewee import Database, Model, fn
from model import ModelMeta
from table import Table
from middleware import RestSqlMiddleware
from restsqldb import EnumDataBase, RestSqlDb
from impalet import ImpalaDatabase
import pandas as pd
import json
import re
import six
import copy

# from elasticsearch import Elasticsearch
# from elasticsearch_dsl import Search


class SubQuery(object):
    # 单个sql子句查询
    def __init__(self, query, join_type, database, on=None, export=None, limit=1000):
        self.query = query
        self.join_type = join_type
        self.database = database
        self.table = self._get_table()
        self.on = on
        self.export = export
        self.alias = self._get_alias(export)
        # self.schema = schema
        self._result = []
        self.query['from'] = self.query['from'].split('.', 1)[1]
        self.limit = limit

    @staticmethod
    def _get_alias(export):
        if export is None:
            return None
        else:
            alias_result = {}
            for item in export:
                raw = item.split('@')[0]
                alias = item.split('@')[1]
                alias_result[raw] = alias
            return alias_result

    def _get_table(self):
        table_name = self.query['from'].split(".", 1)[-1]
        for table in self.database.tables:
            if table_name == table.table_name:
                return table
        return None

    def _get_model(self):
        # if not isinstance(self.database.db, Database):
        #     raise RuntimeError('db is not Database instance')
        if self.table.__bases__[0] != Table:
            raise RuntimeError('schema is not Table class')

        class NewModel(six.with_metaclass(ModelMeta, Model)):

            class Meta:
                database = self.database.db
                table_name = self.table.table_name
                fields = self.table.fields
                schema = getattr(self.database, 'schema', None)
        return NewModel

    def _get_peewee_query(self):
        model = self._get_model()
        selects = self.query['fields'] + self.query['aggregation']
        filters = self.query.get('filter', {})
        groups = self.query.get('group_by', [])
        limit = self.query.get('limit', 1000)

        # get select params
        select_params = []
        for expression in selects:
            if '__' in expression:
                field, operator = expression.split('__')
                if operator in ['count', 'sum', 'avg', 'max', 'min']:
                    param = getattr(fn, operator)(getattr(model, field)).alias(expression)
                    select_params.append(param)
                elif operator == 'count_distinct':
                    # count_distinct需要特殊处理，peewee库中没有专门的处理方法
                    param = fn.Count(fn.Distinct(getattr(model, field))).alias(expression)
                    select_params.append(param)
                else:
                    raise RuntimeError('operator {} is invalid'.format(operator))

            else:
                select_params.append(getattr(model, expression))

        # get where params
        where_params = []
        for filter_k, filter_v in filters.items():
            if '__' in filter_k:
                field, operator = filter_k.split('__')
                if operator == 'gt':
                    # where_expression = (getattr(model, field) > filter_v)
                    where_params.append(getattr(model, field) > filter_v)
                elif operator == 'lt':
                    where_params.append(getattr(model, field) < filter_v)
                elif operator == 'gte':
                    where_params.append(getattr(model, field) >= filter_v)
                elif operator == 'lte':
                    where_params.append(getattr(model, field) <= filter_v)
                elif operator == 'contains':
                    where_params.append(getattr(model, field).contains(filter_v))
                elif operator == 'startswith':
                    where_params.append(getattr(model, field).startswith(filter_v))
                elif operator == 'endswith':
                    where_params.append(getattr(model, field).endswith(filter_v))
                elif operator == 'range':
                    if isinstance(filter_v, list) and len(filter_v) == 2:
                        where_params.append(getattr(model, field).between(*filter_v))
                    else:
                        if isinstance(filter_v, list):
                            raise RuntimeError('the length of Range list should be 2')
                        else:
                            raise RuntimeError('Range value should be a list')
                elif operator == 'in':
                    if isinstance(filter_v, list):
                        where_params.append(getattr(model, field).in_(filter_v))
                    else:
                        raise RuntimeError('In value should be list')
                else:
                    raise RuntimeError('filter {} is invalid'.format(operator))
            else:
                where_params.append(getattr(model, filter_k) == filter_v)

        # get group by params
        group_params = []
        for field in groups:
            group_params.append(getattr(model, field))
        # select
        results = model.select(*select_params)
        if len(where_params) > 0:
            # filter
            results = results.where(*where_params)
        if len(group_params) > 0:
            # group by
            results = results.group_by(*group_params)
        results = results.limit(limit)
        return results

    def _query_sql(self):
        query = self._get_peewee_query()
        selects = self.query['fields'] + self.query['aggregation']
        for result in query:
            record = {}
            for field in selects:
                if self.alias and field in self.alias.keys():
                    record[self.alias[field]] = getattr(result, field)
                else:
                    record[field] = getattr(result, field)
            self._result.append(record)

    def _query_impala(self):
        client = self.database.impala_client
        sql, params = self._get_peewee_query().sql()
        print("_query_impala, sql", sql)
        # impala_sql = re.sub("FROM \`(.*)\.([^\`]*)\`", "FROM \\1.\\2", sql)
        # print("_query_impala, impala_sql", impala_sql)
        # self._result = client.run_sql((impala_sql, params))
        self._result = client.run_sql((sql, params))
        print("_query_impala._result", self._result)

    def _query_es(self):
        es_client = self.database.db
        dsl = self._json_to_dsl()
        index = dsl['from']
        del dsl['from']
        raw_result = es_client.search(index=index, body=dsl)
        # result = {}
        if 'aggs' in raw_result or 'aggregations' in raw_result:
            if raw_result.get('aggregations'):
                self._result = raw_result['aggregations']['groupby']['buckets']
            else:
                self._result = raw_result['agg']['groupby']['buckets']
            for it in self._result:
                pair = it['key'].split(';')
                for pair_item in pair:
                    it.update({pair_item.split(':')[0]: pair_item.split(':')[1]})
                del it['key']
                del it['doc_count']  # TODO: 暂时没用的一个字段
                for field, value in it.items():
                    if isinstance(value, dict) and 'value' in value:
                        if self.alias is None:
                            it[field] = value['value']
                        else:
                            if field in self.alias.keys():
                                it[self.alias[field]] = value['value']
        elif 'hits' in raw_result and 'hits' in raw_result['hits']:
            if self.alias is None:
                self._result = list(map(lambda x: x['_source'], raw_result['hits']['hits']))
            # for it in self._result:
            else:
                for it in raw_result['hits']['hits']:
                    record = it['_source']
                    result = {}
                    for field in record.keys():
                        if field in self.alias.keys():
                            result[self.alias[field]] = record[field]
                    self._result.append(result)
        return self._result

    def _json_to_dsl(self):
        if self.query['from'] is None or self.query['from'] == '':
            raise SyntaxError('Check query whether contains the "from" field')
        limit = self.query.get("limit", 1000)
        dsl = {
            'size': limit,
            'query': {
                'bool': {
                    'must': []
                }
            },
            'sort': [],
            '_source': {
                'includes': []
            },
            'aggs': {
                'groupby': {
                    'terms': {
                        'script': {
                            'source': ''
                        }
                    },
                    'aggs': {}
                }
            },
            'from': self.query['from']
        }
        dsl['_source']['includes'] = self.query['fields']
        dsl_where = dsl['query']['bool']['must']
        dsl_group_by = ''
        dsl_aggs = dsl['aggs']['groupby']['aggs']
        dsl_sort = dsl['sort']

        # 处理filter
        for field, value in self.query['filter'].items():
            if '__' not in field:
                dsl_where.append({
                    'term': {
                        field: value
                    }
                })
            else:
                op = field.split('__')[1]
                field_name = field.split('__')[0]
                if op == 'gt':
                    dsl_where.append({
                        'range': {
                            field_name: {'gt': value}
                        }
                    })
                elif op == 'lt':
                    dsl_where.append({
                        'range': {
                            field_name: {'lt': value}
                        }
                    })
                elif op == 'gte':
                    dsl_where.append({
                        'range': {
                            field_name: {'gte': value}
                        }
                    })
                elif op == 'lte':
                    dsl_where.append({
                        'range': {
                            field_name: {'lte': value}
                        }
                    })
                elif op == 'contains':
                    """"
                    TODO: 本来想用match/match_phrase来进行模糊匹配，但是由于这两种查询由于分词的缘故，现有的
                          分词情况并不能完美的模拟sql中的like，所以暂时采用正则查询。正则查询的效率很低。
                    dsl_where.append({
                        'match_phrase': {
                            field_name: {
                                'query': value
                            }
                        }
                    })
                    """
                    dsl_where.append({
                        'wildcard': {field_name: ''.join(['*', value, '*'])}
                    })
                elif op == 'startswith':
                    dsl_where.append({
                        'prefix': {field_name: value}
                    })
                elif op == 'endswith':
                    dsl_where.append({
                        'wildcard': {field_name: ''.join(['*', value])}
                    })
                elif op == 'range':
                    if len(value) != 2:
                        raise SyntaxError('Check your "range" query')
                    dsl_where.append({
                        'range': {
                            field_name: {'gte': value[0], 'lte': value[1]}
                        }
                    })
                elif op == 'in':
                    dsl_where.append({
                        'terms': {field_name: value}
                    })
                else:
                    raise SyntaxError('cat not support op: {0}, field: {1}'.format(op, field))
        if self.query.get('group_by'):
            # 处理 group by
            """
            由于ES 6.x以下版本不支持 composite 语法，所以这里采用script方式来实现group by，用来兼容不同版本ES这部分语法的差异性
            script中source的格式：key:value;key:value
            定义成这个样子是方便后面从查询结果中提取数据
            """
            for field in self.query['group_by']:
                dsl_group_by = ''.join(
                    [dsl_group_by, "'", field, "'", " + ':' + ", "doc['", field, "'].value", " + ';' + "])
            dsl_group_by = dsl_group_by[:len(dsl_group_by) - len(" + ';' + ")]  # 去掉结尾的 " + ';' + "
            dsl['aggs']['groupby']['terms']['script']['source'] = dsl_group_by
            # 处理 aggregation
            for field in self.query['aggregation']:
                field_name, op = field.split('__')[0], field.split('__')[1]
                func_map = {'count': 'value_count', 'sum': 'sum', 'avg': 'avg', 'max': 'max', 'min': 'min',
                            'count_distinct': 'cardinality'}
                if op in func_map:
                    dsl_aggs[field] = {func_map[op]: {'field': field_name}}
                else:
                    raise SyntaxError('cat not support aggregation operation: {}'.format(op))
        else:
            del dsl['aggs']

        # 处理 sort
        if self.query.get('sort'):
            for sort_it in self.query['sort']:
                is_reverse = sort_it.find('-')
                if is_reverse != 0:
                    dsl_sort.append({
                        sort_it: {'order': 'asc'}
                    })
                else:
                    field = ''.join(sort_it.split('-')[1:])
                    dsl_sort.append({
                        field: {'order': 'desc'}
                    })
        else:
            del dsl['sort']
        return dsl

    def do_query(self):
        db_type = self.database.type
        if db_type in [EnumDataBase.SQLITE, EnumDataBase.MYSQL, EnumDataBase.PG]:
            self._query_sql()
        elif db_type == EnumDataBase.ES:
            self._query_es()
        elif db_type == EnumDataBase.IMPALA:
            self._query_impala()

    @property
    def complete(self):
        return len(self._result) > 0

    @property
    def result(self):
        return self._result

    @property
    def result_dataframe(self):
        return pd.DataFrame(self._result)


class RestSqlClient(object):

    def __init__(self, db_settings, middlewares=None):
        self._db_instances = []
        self._middleware_list = middlewares if middlewares is not None else []
        self.query_list = []
        for setting in db_settings:
            self._db_instances.append((RestSqlDb(setting)))

    def _get_db_from_table(self, table_name):
        try:
            db_name, table_name = table_name.split('.', 1)
        except ValueError:
            raise RuntimeError('table_name {} is not invalid'.format(table_name))
        for db in self._db_instances:
            if db_name == db.name:
                return db

    def _split_query(self, query):
        subquery_list = []
        main_subquery = query['select']
        main_db = self._get_db_from_table(main_subquery['from'])
        subquery_list.append(SubQuery(query=main_subquery, join_type='main', database=main_db))
        for join in query['join']:
            join_subquery = join['query']['select']
            join_db = self._get_db_from_table(join_subquery['from'])
            subquery_list.append(SubQuery(query=join_subquery, join_type=join['type'], database=join_db, on=join['on'], export=join['export']))
        return subquery_list

    def query(self, query):

        # 0、语法检查，以及必要的修改（例如添加必须的过滤条件）
        for middleware in self._middleware_list:
            # todo：类型检查
            middleware.process_query(query)

        # 1、拆分sql
        subquery_list = self._split_query(query)

        # 2、查询sql
        data_frame = None
        for subquery in subquery_list:
            subquery.do_query()
            if subquery.join_type == 'main':
                # 取出主查询结果，方便下一步合并
                data_frame = subquery.result_dataframe

        # 3、合并
        join_type_map = {
            'left_join': 'left',
            'inner_join': 'inner',
            'full_join': 'outer'
        }
        for subquery in subquery_list:
            if subquery.join_type in join_type_map.keys():
                df = subquery.result_dataframe
                data_frame = data_frame.merge(df, left_on=subquery.on.keys(),
                                              right_on=subquery.on.values(),
                                              how=join_type_map[subquery.join_type])

        # 4、sort
        sort_list = query.get('sort', None)
        if sort_list and data_frame.to_dict():
            sort_methods = []
            for index, value in enumerate(sort_list):
                if value.startswith('-'):
                    # it = value[1:]
                    sort_list[index] = value[1:]    # 去掉-
                    sort_methods.append(False)
                else:
                    sort_methods.append(True)
            data_frame = data_frame.sort_values(by=sort_list, ascending=sort_methods)

        # 5、合并后limit处理
        limit = query.get('limit', 1000)
        data_frame = data_frame[0:limit]
        data_frame = data_frame.fillna('null')

        # 6、整个语句的fields提取及alias处理
        alias_map = {}
        for field in query['fields']:
            if field.find('@') != -1:
                alias_map.update({field.split('@')[0]: field.split('@')[1]})
        data_list = json.loads(data_frame.to_json(orient='records'))

        results = []
        for data in data_list:  # 对每个data都处理得到最终展示结构
            record = copy.deepcopy(data)  # 这里必须深拷贝
            for raw, alias in alias_map.items():
                if alias == 'exclude' and raw in record:  # 作为exlcude剔除出record中
                    del record[raw]
                    continue
                if raw in data.keys():  # 将raw替换为alias并加入record
                    if raw != alias:  # 只有raw!=alias时才删除原raw并加入alias列
                        del record[raw]
                        record[alias] = data[raw]
                else:
                    var_list = self._extract_var(raw)  # 可能是个表达式，将表达式中的变量及数字全部提取出来
                    if not var_list:
                        raise RuntimeError('field {} is invalid'.format(raw))
                    for var in var_list:
                        if var not in data.keys() and not self._is_number(var):
                            raise RuntimeError('field {} is invalid'.format(raw))
                        if not self._is_number(var):
                            globals()[var] = data[var]
                    # 上面循环结束时未抛异常则认为这是一个表达式，直接计算结果即可
                    try:
                        # TODO: 不安全的代码 eval
                        record[alias] = eval(raw)
                    except ZeroDivisionError:
                        record[alias] = 0
            results.append(record)
        return results

    @staticmethod
    def _is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def _extract_var(expression):
        '''
        将计算表达式中的变量提取出来
        :param expression:  (a+b)*(c-d)
        :return: [a,b,c,d]
        '''
        return re.findall('[^\+,\-,\*,\/,(,)]+', expression)