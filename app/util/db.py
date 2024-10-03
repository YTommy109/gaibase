from types import TracebackType
from typing import Any
from typing import Optional
from typing import Type

from psycopg import Connection
from psycopg import Cursor
from psycopg.rows import class_row
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool


def init_db() -> None:
    Database.initialize('postgres://tokutomi@127.0.0.1:5432/gaibase_dev?sslmode=disable')


class Database:
    __connection_pool: Optional[ConnectionPool] = None

    @classmethod
    def initialize(cls, conninfo: str) -> None:
        if not cls.__connection_pool:
            cls.__connection_pool = ConnectionPool(min_size=1, max_size=10, conninfo=conninfo)

    @classmethod
    def get_connection(cls) -> Optional[Connection]:
        return cls.__connection_pool.getconn() if cls.__connection_pool else None

    @classmethod
    def return_connection(cls, connection: Connection) -> None:
        cls.__connection_pool.putconn(connection) if cls.__connection_pool else None

    @classmethod
    def close_all_connections(cls) -> None:
        cls.__connection_pool.close() if cls.__connection_pool else None


class CursorFromPool:
    def __init__(self, model: Any = None) -> None:
        self.con: Any = None
        self.cur: Optional[Cursor] = None
        self.factory: Any = class_row(model) if model else dict_row

    def __enter__(self) -> Optional[Cursor]:
        """with ブロックの入り口"""
        self.con = Database.get_connection()
        self.cur = self.con.cursor(row_factory=self.factory) if self.con else None
        return self.cur

    def __exit__(
        self,
        _exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        _exc_tb: Optional[TracebackType],
    ) -> None:
        """with ブロックの出口"""
        if exc_val is not None and self.con is not None:
            # エラーならロールバック
            self.con.rollback()
        else:
            self.cur.close() if self.cur else None
            self.con.commit() if self.con else None

        # 常にコネクションをプールに戻す。
        Database.return_connection(self.con)
