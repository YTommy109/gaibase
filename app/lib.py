from dataclasses import dataclass
from uuid import UUID


#
# 型定義
#
@dataclass
class ApplicationID:
    id: UUID


@dataclass
class WorkspaceID:
    id: UUID


@dataclass
class AssetID:
    id: UUID


@dataclass
class Application:
    id: UUID
    name: str
