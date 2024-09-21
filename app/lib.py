from datetime import datetime
from enum import Enum
from typing import TypeAlias
from uuid import UUID

from pydantic import BaseModel


#
# 型定義
#
class SystemRole(Enum):
    ADMIN = 'admin'
    USER = 'user'


class MemberRole(Enum):
    MANAGER = 'manager'
    LEADER = 'leader'
    MEMBER = 'member'
    MAINTAINER = 'maintainer'


ROLE_LABEL = {SystemRole.ADMIN: '運用', SystemRole.USER: '一般'}

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
    def role_name(self):
        return ROLE_LABEL[self.role]


class Application(BaseModel, frozen=True):
    id: ApplicationID
    name: str


class Workspace(BaseModel):
    id: WorkspaceID
    title: str
    created_at: datetime
    freezed_at: datetime | None = None


class WorkspaceMember(BaseModel):
    id: UUID
    workspace_id: WorkspaceID
    account_id: AccountID
    role: MemberRole


class Tool(BaseModel, frozen=True):
    id: ToolID
    workspace_id: WorkspaceID
    title: str
    application_id: ApplicationID
    created_at: datetime
    requested_at: datetime | None = None  # リクエスト日時
    finished_at: datetime | None = None  # 完了日時
