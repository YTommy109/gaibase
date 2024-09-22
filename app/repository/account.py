from lib import Account
from util.db import CursorFromPool


def get_active_accounts() -> list[Account]:
    with CursorFromPool(Account) as cur:
        cur.execute(
            """
            SELECT * FROM accounts_active
            """
        )
        return cur.fetchall()


def get_account_by_name(name: str) -> Account | None:
    with CursorFromPool(Account) as cur:
        cur.execute(
            """
            SELECT * FROM accounts_active WHERE name = %s
            """,
            (name,),
        )
        return cur.fetchone()


def create_account(email: str, name: str) -> None:
    with CursorFromPool() as cur:
        cur.execute(
            """
            INSERT INTO accounts (email, name)
            VALUES (%s, %s)
            """,
            (email, name),
        )
