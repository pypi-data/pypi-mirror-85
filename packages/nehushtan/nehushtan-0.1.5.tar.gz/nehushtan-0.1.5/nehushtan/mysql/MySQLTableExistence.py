#  Copyright (c) 2020. Sinri Edogawa

from abc import abstractmethod, ABC

from nehushtan.mysql.MySQLKit import MySQLKit


class MySQLTableExistence(ABC):
    _mysql_kit: MySQLKit

    def __init__(self):
        # Must initialize `_mysql_kit` in overriding method here
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
