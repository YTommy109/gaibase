from typing import Optional

from lib import Account
from lib import AccountID
from lib import Workspace
from lib import WorkspaceAccount
from util.db import CursorFromPool


def fetch_accounts() -> list[Account]:
    with CursorFromPool(Account) as cur:
        cur.execute(
            """
            SELECT * FROM accounts_active
            """
        )
        return cur.fetchall()


def fetch_account_by_name(name: str) -> Optional[Account]:
    with CursorFromPool(Account) as cur:
        cur.execute(
            """
            SELECT * FROM accounts_active WHERE name = %s
            """,
            (name,),
        )
        return cur.fetchone()


def fetch_account_by_id(id: AccountID) -> Optional[Account]:
    with CursorFromPool(Account) as cur:
        cur.execute(
            """
            SELECT * FROM accounts_active WHERE id = %s
            """,
            (id,),
        )
        return cur.fetchone()


def fetch_workspace_accounts_by_workspace(workspace: Workspace) -> list[WorkspaceAccount]:
    with CursorFromPool(WorkspaceAccount) as cur:
        cur.execute(
            """
            SELECT accounts_active.id as id
            , accounts_active.name as name
            , workspace_members_active.role as role
            FROM workspace_members_active
            JOIN accounts_active ON workspace_members_active.account_id = accounts_active.id
            WHERE workspace_id = %s
            """,
            (workspace.id,),
        )
        return cur.fetchall()


def create_account(email: str, name: str) -> None:
    with CursorFromPool() as cur:
        cur.execute(
            """
            INSERT INTO accounts (email, name)
            VALUES (%s, %s)
            """,
            (email, name),
        )
