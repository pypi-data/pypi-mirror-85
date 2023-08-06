from ewah.operators.sql_base_operator import EWAHSQLBaseOperator
from ewah.constants import EWAHConstants as EC

from airflow.hooks.base_hook import BaseHook

import pymysql

class EWAHMySQLOperator(EWAHSQLBaseOperator):

    _SQL_BASE = \
        'SELECT\n{columns}\nFROM `{schema}`.`{table}`\nWHERE {where_clause}'
    _SQL_BASE_SELECT = \
        'SELECT * FROM ({select_sql}) t WHERE {{0}}'
    _SQL_COLUMN_QUOTE = '`'
    _SQL_MINMAX_CHUNKS = 'SELECT MIN({column}), MAX({column}) FROM ({base}) t;'
    _SQL_CHUNKING_CLAUSE = '''
        AND {column} >= %(from_value)s
        AND {column} <{equal_sign} %(until_value)s
    '''
    _SQL_PARAMS = '%({0})s'

    def __init__(self, time_zone=None, *args, **kwargs):
        self.sql_engine = self._MYSQL
        super().__init__(*args, **kwargs)
        self.time_zone = time_zone


    def _get_data_from_sql(self, sql, params=None, return_dict=True):
        if return_dict:
            cursor_class = pymysql.cursors.DictCursor
        else:
            cursor_class = pymysql.cursors.Cursor
        conn_kwargs = {
            'host': self.connection.host,
            'user': self.connection.login,
            'passwd': self.connection.password,
            'port': self.connection.port,
            'database': self.connection.schema,
            'cursorclass': cursor_class,
        }
        if self.time_zone:
            conn_kwargs['init_command'] = "SET SESSION time_zone='{0}'".format(
                self.time_zone,
            )
        database_conn = pymysql.connect(**conn_kwargs)
        cursor = database_conn.cursor()
        self.log.info('Executing:\n{0}\n\nWith params:\n{1}'.format(
            sql,
            str(params),
        ))
        cursor.execute(sql, args=params)
        data = cursor.fetchall()
        cursor.close()
        database_conn.close()
        return data
