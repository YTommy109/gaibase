from datetime import datetime
from enum import Enum
from typing import TypeAlias
from uuid import UUID

from pydantic import BaseModel


#
# 型定義
#
class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'


ApplicationID: TypeAlias = UUID
WorkspaceID: TypeAlias = UUID
AssetID: TypeAlias = UUID
AccountID: TypeAlias = UUID


class Account(BaseModel):
    id: AccountID
    email: str
    name: str
    role: Role


class Application(BaseModel):
    id: ApplicationID
    name: str


class Workspace(BaseModel):
    id: WorkspaceID
    title: str
    created_at: datetime
    freezed_at: datetime | None = None


class Asset(BaseModel):
    id: AssetID
    workspace_id: WorkspaceID
    title: str
    application_id: ApplicationID
    created_at: datetime
    requested_at: datetime | None = None  # リクエスト日時
    finished_at: datetime | None = None  # 完了日時
