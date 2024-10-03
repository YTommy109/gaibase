from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from typing_extensions import TypeAlias


#
# 型定義
#
class SystemRole(Enum):
    ADMIN = 'admin'
    USER = 'user'


class WorkspaceRole(Enum):
    MANAGER = 'manager'
    LEADER = 'leader'
    MEMBER = 'member'
    MAINTAINER = 'maintainer'


SYSTEM_ROLE_LABEL: dict[SystemRole, str] = {SystemRole.ADMIN: '運用', SystemRole.USER: '一般'}
WORKSPACE_ROLE_LABEL: dict[WorkspaceRole, str] = {
    WorkspaceRole.MANAGER: 'マネージャー',
    WorkspaceRole.LEADER: 'リーダー',
    WorkspaceRole.MEMBER: 'メンバー',
    WorkspaceRole.MAINTAINER: 'メンテナー',
}

ApplicationID: TypeAlias = UUID
WorkspaceID: TypeAlias = UUID
ToolID: TypeAlias = UUID
AccountID: TypeAlias = UUID


class Account(BaseModel, frozen=True):
    id: AccountID
    email: str
    name: str
    role: SystemRole

    @property
    def role_name(self) -> str:
        return SYSTEM_ROLE_LABEL[self.role]

    def __eq__(self, other:object) -> bool:
        if not isinstance(other, Account):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class Application(BaseModel, frozen=True):
    id: ApplicationID
    name: str


class Workspace(BaseModel, frozen=True):
    id: WorkspaceID
    title: str
    created_at: datetime
    disabled_at: Optional[datetime] = None


class WorkspaceMember(BaseModel, frozen=True):
    id: UUID
    workspace_id: WorkspaceID
    account_id: AccountID
    role: WorkspaceRole


class WorkspaceAccount(BaseModel, frozen=True):
    id: AccountID
    name: str
    role: WorkspaceRole

    @property
    def role_name(self) -> str:
        return WORKSPACE_ROLE_LABEL[self.role]


class Tool(BaseModel, frozen=True):
    id: ToolID
    workspace_id: WorkspaceID
    title: str
    application_id: ApplicationID
    created_at: datetime
    requested_at: Optional[datetime] = None  # リクエスト日時
    finished_at: Optional[datetime] = None  # 完了日時
