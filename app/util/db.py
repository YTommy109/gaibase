from psycopg.rows import class_row
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool


class Database:
    __connection_pool = None

    @classmethod
    def initialize(cls, conninfo) -> None:
        if not cls.__connection_pool:
            cls.__connection_pool = ConnectionPool(min_size=1, max_size=10, conninfo=conninfo)

    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn() if cls.__connection_pool else None

    @classmethod
    def return_connection(cls, connection) -> None:
        cls.__connection_pool.putconn(connection) if cls.__connection_pool else None

    @classmethod
    def close_all_connections(cls) -> None:
        cls.__connection_pool.close() if cls.__connection_pool else None


class CursorFromPool:
    def __init__(self, model=None):
        self.con = None
        self.cur = None
        self.factory = class_row(model) if model else dict_row

    def __enter__(self):
        """with ブロックの入り口"""
        self.con = Database.get_connection()
        self.cur = self.con.cursor(row_factory=self.factory)
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        """with ブロックの出口"""
        if exc_val is not None and self.con is not None:
            # エラーならロールバック
            self.con.rollbak()
        else:
            self.cur.close() if self.cur else None
            self.con.commit() if self.con else None

        # 常にコネクションをプールに戻す。
        Database.return_connection(self.con)
