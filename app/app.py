# app.py
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from uuid import uuid4

import streamlit as st


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
    input_file: str
    application: Application
    output_file: str | None
    created_at: datetime
    requested_at: datetime | None = None # リクエスト日時
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


def pane_workspaces():
    """ Workspace 一覧を表示する """
    st.title('管理システム')

    if st.button('Workspace を作成する'):
        create_workspace()

    st.divider()

    hd1, hd2, hd3, hd4 = st.columns(4)
    hd1.write('**No.**')
    hd2.write('**名前**')
    hd3.write('**作成日時**')

    def click_workspace(workspace: Workspace):
        st.session_state.workspace = workspace

    for idx, workspace in enumerate(st.session_state.workspaces):
        col1, col2, col3, col4 = st.columns(4)
        col1.write(idx + 1)
        col2.write(workspace.title)
        col3.write(workspace.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        col4.button('Go', key=workspace.id, on_click=click_workspace, kwargs={'workspace': workspace})


def pane_assets():
    """アセット一覧を表示する"""
    st.button('戻る', key='back', on_click=lambda: st.session_state.pop('workspace'))
    st.header(st.session_state.workspace.title)

    if st.button('アセットを作成する'):
        create_asset()

    st.divider()

    hd1, hd2, hd3, hd4, hd5, hd6 = st.columns(6)
    hd1.write('**No.**')
    hd2.write('**入力ファイル**')
    hd3.write('**業務 Excel シート**')
    hd4.write('**出力ファイル**')
    hd5.write('**作成日時**')
    hd6.write('')

    assets = filter(lambda x: x.workspace_id == st.session_state.workspace.id, st.session_state.assets)
    for idx, asset in enumerate(assets):
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.write(idx + 1)
        col2.write(asset.input_file)
        col3.write(asset.application.name)
        col4.write(asset.output_file)
        col5.write(asset.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        col6.button('Rerun')
        # Excel の中で実行するなら Rerun はいらんか…
        # でも、アーカイブはどうするんやろか…?


@st.dialog('Workspace 作成')
def create_workspace() -> None:
    """ Workspace を作成するダイアログ"""
    title = st.text_input('名前')
    c1, c2 = st.columns(2)
    if c1.button('作成', type='primary'):
        workspace = Workspace(uuid4(), title, datetime.now())
        st.session_state.workspaces.append(workspace)
        st.rerun()
    if c2.button('キャンセル', type='secondary'):
        st.rerun()


@st.dialog('新規アセット作成')
def create_asset() -> None:
    """アセットを作成するダイアログ"""
    file = st.text_input('入力ファイル')
    app = st.selectbox('アプリケーション', APPLICATIONS, format_func=lambda x: x.name)
    c1, c2 = st.columns(2)
    if c1.button('作成', type='primary'):
        asset = Asset(uuid4(), st.session_state.workspace.id, file, app, None, datetime.now(), None, None)
        st.session_state.assets.append(asset)
        st.rerun()
    if c2.button('キャンセル', type='secondary'):
        st.rerun()


if st.session_state.workspace:
    pane_assets()
else:
    pane_workspaces()
