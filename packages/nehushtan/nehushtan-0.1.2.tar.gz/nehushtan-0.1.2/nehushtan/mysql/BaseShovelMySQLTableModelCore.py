#  Copyright (c) 2020. The Source Data Mining Group, Technology & Product Department, Leqee Ltd.

# VERSION 1.11.1, 2020-11-16
# WARNING: DO NOT MODIFY THIS FILE, JUST FOLLOW THE SHOVEL STANDARD!

import time
from abc import ABC

import pymysql

from nehushtan.mysql import constant
from nehushtan.mysql import MySQLCondition
from nehushtan.mysql import MySQLQueryResult
from nehushtan.mysql.MySQLTableExistence import MySQLTableExistence
from nehushtan.mysql.MySQLTableSelection import MySQLTableSelection


class BaseShovelMySQLTableModelCore(MySQLTableExistence, ABC):

    @staticmethod
    def now() -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def select_in_table(self):
        return MySQLTableSelection(model=self)

    def insert_one_row(self, row_dict: dict, commit_immediately: bool = False):
        return self._write_one_row(row_dict, 'INSERT', commit_immediately)

    def replace_one_row(self, row_dict: dict, commit_immediately: bool = False):
        return self._write_one_row(row_dict, 'REPLACE', commit_immediately)

    def _write_one_row(self, row_dict: dict, write_type: str, commit_immediately: bool = False):
        fields = []
        values = []
        for k, v in row_dict.items():
            fields.append(k)
            values.append(self.get_mysql_kit().quote(v))
        fields = ",".join(fields)
        values = ",".join(values)
        sql = f"{write_type} INTO {self.get_table_expression()} ({fields}) VALUES ({values})"

        return self._modify_with_sql(sql, commit_immediately)

    def insert_many_rows_with_dicts(self, row_dicts: tuple or list, commit_immediately: bool = False):
        return self._write_many_rows_with_dicts(
            row_dict_array=row_dicts,
            write_type='INSERT',
            commit_immediately=commit_immediately
        )

    def replace_many_rows_with_dicts(self, row_dicts: tuple or list, commit_immediately: bool = False):
        return self._write_many_rows_with_dicts(
            row_dict_array=row_dicts,
            write_type='REPLACE',
            commit_immediately=commit_immediately
        )

    def insert_many_rows_with_matrix(self, fields: tuple, row_matrix: tuple or list, commit_immediately: bool = False):
        return self._write_many_rows_with_matrix(
            fields=fields,
            row_matrix=row_matrix,
            write_type='INSERT',
            commit_immediately=commit_immediately
        )

    def replace_many_rows_with_matrix(self, fields: tuple, row_matrix: tuple or list, commit_immediately: bool = False):
        return self._write_many_rows_with_matrix(
            fields=fields,
            row_matrix=row_matrix,
            write_type='REPLACE',
            commit_immediately=commit_immediately
        )

    def _write_many_rows_with_dicts(
            self,
            row_dict_array: (tuple or list),
            write_type: str,
            commit_immediately: bool = False
    ):
        if len(row_dict_array) <= 0:
            return MySQLQueryResult.create_error_result('Rows Empty')

        sample_row = row_dict_array[0]

        fields = []
        for k, v in sample_row.items():
            fields.append(k)
        fields = ",".join(fields)

        row_sql = []
        for row in row_dict_array:
            values = []
            for k, v in row.items():
                values.append(self.get_mysql_kit().quote(v))
            values = ",".join(values)
            row_sql.append(f'({values})')
        row_sql = ",".join(row_sql)

        sql = f"{write_type} INTO {self.get_table_expression()} ({fields}) VALUES {row_sql}"

        return self._modify_with_sql(sql, commit_immediately)

    def _write_many_rows_with_matrix(
            self,
            fields: tuple,
            row_matrix: (tuple or list),
            write_type: str,
            commit_immediately: bool = False
    ):
        fields_sql = ",".join(fields)
        row_sql = []
        for row in row_matrix:
            values = []
            for v in row:
                values.append(self.get_mysql_kit().quote(v))
            values = ",".join(values)
            row_sql.append(f'({values})')
        row_sql = ",".join(row_sql)

        sql = f"{write_type} INTO {self.get_table_expression()} ({fields_sql}) VALUES {row_sql}"

        return self._modify_with_sql(sql, commit_immediately)

    def _modify_with_sql(self, sql: str, commit_immediately: bool = False):
        result = MySQLQueryResult()
        cursor = None

        try:
            result.set_sql(sql)
            cursor = self.get_mysql_kit().get_raw_connection().cursor()
            cursor.execute(sql)
            result.set_status(constant.MYSQL_QUERY_STATUS_EXECUTED)
            result.set_last_inserted_id(cursor.lastrowid)
            result.set_affected_rows(cursor.rowcount)
            if commit_immediately:
                self.get_mysql_kit().get_raw_connection().commit()

        except pymysql.MySQLError as e:
            result.set_status(constant.MYSQL_QUERY_STATUS_ERROR)
            result.set_error(f"MySQL Error [{e.args[0]}] {e.args[1]}")

        except Exception as pe:
            result.set_status(constant.MYSQL_QUERY_STATUS_ERROR)
            result.set_error(f"Python Error: {pe}")

        finally:
            if cursor is not None:
                cursor.close()
            return result

    def update_rows(self, conditions: tuple or list, modifications: dict, commit_immediately: bool = False):
        condition_sql = MySQLCondition.build_sql_component(conditions)

        modify_pairs = []
        for k, v in modifications.items():
            modify_pairs.append(f'`{k}`=' + self.get_mysql_kit().quote(v))
        modify_pairs = ",".join(modify_pairs)

        sql = f"UPDATE {self.get_table_expression()} SET {modify_pairs} WHERE {condition_sql}"

        return self._modify_with_sql(sql, commit_immediately)

    def delete_rows(self, conditions: tuple or list, commit_immediately: bool = False):
        condition_sql = MySQLCondition.build_sql_component(conditions)

        sql = f"DELETE FROM {self.get_table_expression()} WHERE {condition_sql}"

        return self._modify_with_sql(sql, commit_immediately)
