# app.py
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from uuid import uuid4

import streamlit as st
from lib import Application


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
class Workspace:
    id: UUID
    title: str
    created_at: datetime
    freezed_at: datetime | None = None


@dataclass
class Asset:
    id: UUID
    workspace_id: UUID
    title: str
    application: Application
    created_at: datetime
    requested_at: datetime | None = None  # リクエスト日時
    finished_at: datetime | None = None  # 完了日時


#
# 定数
#

APPLICATIONS: list[Application] = [
    Application(uuid4(), '業務 Excel シート 1'),
    Application(uuid4(), '業務 Excel シート 2'),
    Application(uuid4(), '業務 Excel シート 3'),
]

#
# セッションステートの初期化
#
if 'workspaces' not in st.session_state:
    st.session_state.workspaces = [
        Workspace(uuid4(), 'Workspace1', datetime.now()),
        Workspace(uuid4(), 'Workspace2', datetime.now()),
    ]

if 'assets' not in st.session_state:
    st.session_state.assets = []

if 'workspace' not in st.session_state:
    st.session_state.workspace = None

if 'applications' not in st.session_state:
    st.session_state.applications = APPLICATIONS


def pane_workspaces():
    """Workspace 一覧を表示する"""
    st.title('管理システム')

    if st.button('Workspace を作成する'):
        create_workspace()

    st.divider()

    COLUMNS = [1, 6, 3, 1]
    hds = st.columns(COLUMNS)
    hds[0].write('**No.**')
    hds[1].write('**名前**')
    hds[2].write('**作成日時**')

    def click_workspace(workspace: Workspace):
        st.session_state.workspace = workspace

    for idx, workspace in enumerate(st.session_state.workspaces):
        cols = st.columns(COLUMNS)
        cols[0].write(idx + 1)
        cols[1].write(workspace.title)
        cols[2].write(workspace.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        cols[3].button('Go', key=workspace.id, on_click=click_workspace, kwargs={'workspace': workspace})


def pane_assets():
    """アセット一覧を表示する"""
    st.button('戻る', key='back', on_click=lambda: st.session_state.pop('workspace'))
    st.header(st.session_state.workspace.title)

    if st.button('アセットを作成する'):
        create_asset()

    st.divider()

    COLUMNS = [1, 5, 3, 2]
    hds = st.columns(COLUMNS)
    hds[0].write('**No.**')
    hds[1].write('**業務 Excel シート**')
    hds[2].write('**作成日時**')
    hds[3].write('')

    assets = filter(lambda x: x.workspace_id == st.session_state.workspace.id, st.session_state.assets)
    for idx, asset in enumerate(assets):
        cols = st.columns(COLUMNS)

        cols[0].write(idx + 1)
        cols[1].write(asset.application.name)
        cols[2].write(asset.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        cols[3].button('Run')


@st.dialog('Workspace 作成')
def create_workspace() -> None:
    """Workspace を作成するダイアログ"""
    title = st.text_input('名前')
    cols = st.columns(3)
    if cols[1].button('キャンセル', type='secondary', use_container_width=True):
        st.rerun()
    if cols[2].button('セットアップ', type='primary', use_container_width=True):
        workspace = Workspace(uuid4(), title, datetime.now())
        st.session_state.workspaces.append(workspace)
        st.rerun()


@st.dialog('新規アセット作成')
def create_asset() -> None:
    """アセットを作成するダイアログ"""
    title = st.text_input('名前')
    app: Application = st.selectbox('業務 Excel', st.session_state.applications, format_func=lambda x: x.name)
    cols = st.columns(3)
    if cols[1].button('キャンセル', type='secondary', use_container_width=True):
        st.rerun()
    if cols[2].button('作成', type='primary', use_container_width=True):
        asset = Asset(uuid4(), st.session_state.workspace.id, title, app, datetime.now())
        st.session_state.assets.append(asset)
        st.rerun()


if st.session_state.workspace:
    pane_assets()
else:
    pane_workspaces()
