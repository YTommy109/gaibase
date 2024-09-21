from lib import Account
from util.db import CursorFromPool


def get_active_accounts() -> list[Account]:
    with CursorFromPool(Account) as cur:
        cur.execute('select * from accounts_active')
        return cur.fetchall()


def get_account_by_name(name: str) -> Account | None:
    with CursorFromPool(Account) as cur:
        cur.execute('select * from accounts_active where name = %s', (name,))
        return cur.fetchone()
