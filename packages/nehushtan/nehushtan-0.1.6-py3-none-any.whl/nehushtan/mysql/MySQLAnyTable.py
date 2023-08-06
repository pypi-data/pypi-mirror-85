#  Copyright (c) 2020. Sinri Edogawa

from nehushtan.mysql.MySQLKit import MySQLKit
from nehushtan.mysql.MySQLTableMixin import MySQLTableMixin


class MySQLAnyTable(MySQLTableMixin):
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
