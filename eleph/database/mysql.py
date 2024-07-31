import mysql.connector

from .database import Database, Row


class MYSQLDatabase(Database):
    def __init__(
            self,
            host: str,
            user: str,
            password: str,
            database: str
    ):
        self._connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def select[T: Row](self, row: T) -> T:
        pass

    def insert[T: Row](self, row: T):
        pass

    def upsert[T: Row](self, row: T):
        pass
