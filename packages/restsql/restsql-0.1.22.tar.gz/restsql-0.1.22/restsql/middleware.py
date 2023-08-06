# -*- coding:utf-8 -*-


class RestSqlMiddleware(object):

    def __init__(self):
        pass

    @staticmethod
    def process_query(query):
        '''
        :param query: restsql query
        '''
        raise NotImplementedError("Please overwrite this method")