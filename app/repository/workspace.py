from lib import Account
from lib import Workspace
from util.db import CursorFromPool


def get_active_workspaces() -> list[Workspace]:
    with CursorFromPool(Workspace) as cur:
        cur.execute('select * from workspaces_active')
        return cur.fetchall()


def get_owned_workspaces(account: Account) -> list[Workspace]:
    with CursorFromPool(Workspace) as cur:
        cur.execute(
            'SELECT * FROM workspace_members JOIN workspaces ON workspaces.id = workspace_members.workspace_id where account_id = %s',
            (account.id,),
        )
        return cur.fetchall()
