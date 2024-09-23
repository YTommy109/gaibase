from datetime import datetime

from lib import Account
from lib import Workspace
from util.db import CursorFromPool


def fetch_active_workspaces() -> list[Workspace]:
    with CursorFromPool(Workspace) as cur:
        cur.execute(
            """
            SELECT *
            FROM   workspaces_active
            """
        )
        return cur.fetchall()


def fetch_owned_workspaces(account: Account) -> list[Workspace]:
    with CursorFromPool(Workspace) as cur:
        cur.execute(
            """
            SELECT *
            FROM   workspace_members
            JOIN   workspaces ON workspaces.id = workspace_members.workspace_id
            WHERE  account_id = %s
            """,
            (account.id,),
        )
        return cur.fetchall()


def add_member_to_workspace(workspace: Workspace, account: Account) -> Workspace:
    with CursorFromPool() as cur:
        cur.execute(
            """
            INSERT INTO workspace_members (workspace_id, account_id)
            VALUES (%s, %s)
            """,
            (workspace.id, account.id),
        )
    return workspace


def archive_workspace(workspace: Workspace) -> Workspace:
    disabled_workspace = workspace.model_copy(deep=True, update={'disabled_at': datetime.now()})
    with CursorFromPool() as cur:
        cur.execute(
            """
            UPDATE workspaces
            SET disabled_at = %s
            WHERE id = %s
            """,
            (disabled_workspace.disabled_at, disabled_workspace.id),
        )
    return disabled_workspace
