#  Copyright (c) 2020. The Source Data Mining Group, Technology & Product Department, Leqee Ltd.

# VERSION 1.11.0, 2020-11-16
# WARNING: DO NOT MODIFY THIS FILE, JUST FOLLOW THE SHOVEL STANDARD!

from abc import abstractmethod, ABC

from nehushtan.mysql.MySQLKit import MySQLKit


class MySQLTableExistence(ABC):
    _mysql_kit: MySQLKit or None

    def __init__(self):
        pass

    def get_mysql_kit(self) -> MySQLKit:
        if self._mysql_kit is None:
            raise Exception("MySQLKit is not available for querying...")
        return self._mysql_kit

    @abstractmethod
    def mapping_table_name(self) -> str:
        pass

    # noinspection PyMethodMayBeStatic
    def mapping_schema_name(self) -> str:
        return ''

    def get_table_expression(self) -> str:
        e = ''
        if self.mapping_schema_name() != '':
            e += f'`{self.mapping_schema_name()}`.'
        e += self.mapping_table_name()
        return e
