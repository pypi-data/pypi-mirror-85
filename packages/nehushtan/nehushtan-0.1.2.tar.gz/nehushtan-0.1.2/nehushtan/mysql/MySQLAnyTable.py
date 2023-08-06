#  Copyright (c) 2020. The Source Data Mining Group, Technology & Product Department, Leqee Ltd.

# VERSION 1.11.0, 2020-11-16
# WARNING: DO NOT MODIFY THIS FILE, JUST FOLLOW THE SHOVEL STANDARD!

from nehushtan.mysql import BaseShovelMySQLTableModelCore
from nehushtan.mysql.MySQLKit import MySQLKit


class MySQLAnyTable(BaseShovelMySQLTableModelCore):
    _table_name: str
    _schema_name: str

    def __init__(self, mysql_kit: MySQLKit, table_name: str, schema_name: str = ''):
        super().__init__()
        self._mysql_kit = mysql_kit
        self._table_name = table_name
        self._schema_name = schema_name

    def mapping_table_name(self):
        return self._table_name

    def mapping_schema_name(self):
        return self._schema_name
