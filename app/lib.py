from dataclasses import dataclass
from uuid import UUID
from pydantic import BaseModel
from typing import TypeAlias
from datetime import datetime

#
# 型定義
#
ApplicationID: TypeAlias = UUID
WorkspaceID: TypeAlias = UUID
AssetID: TypeAlias = UUID
ApplicationID: TypeAlias = UUID

class Application(BaseModel):
    id: ApplicationID
    name: str

class Workspace(BaseModel):
    id: WorkspaceID
    title: str
    created_at: datetime
    freezed_at: datetime | None = None
