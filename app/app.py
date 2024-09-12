# app.py
from datetime import datetime
from uuid import uuid4

import pandas as pd
import streamlit as st
from lib import Application
from lib import Asset
from lib import Workspace

#
# 定数
#

APPLICATIONS: list[Application] = [
    Application(**{'id': uuid4(), 'name': '業務 Excel シート 1'}),
    Application(**{'id': uuid4(), 'name': '業務 Excel シート 2'}),
    Application(**{'id': uuid4(), 'name': '業務 Excel シート 3'}),
]

#
# セッションステートの初期化
#
if 'workspaces' not in st.session_state:
    st.session_state.workspaces = [
        Workspace(**{'id': uuid4(), 'title': 'Workspace1', 'created_at': datetime.now()}),
        Workspace(**{'id': uuid4(), 'title': 'Workspace2', 'created_at': datetime.now()}),
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

    COLUMNS = [1, 5, 3, 3]
    hds = st.columns(COLUMNS)
    hds[0].write('**No.**')
    hds[1].write('**名前**')
    hds[2].write('**作成日時**')

    def click_workspace(workspace: Workspace):
        st.session_state.workspace = workspace

    def click_freeze(workspace: Workspace):
        workspace.freezed_at = datetime.now()

    # アーカイブされていないワークスペースを表示
    for idx, workspace in enumerate(filter(lambda x: x.freezed_at is None, st.session_state.workspaces)):
        cols = st.columns(COLUMNS)
        cols[0].write(idx + 1)
        cols[1].write(workspace.title)
        cols[2].write(workspace.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        left, right = cols[3].columns(2)
        left.button('Go', key=f'go_{workspace.id}', on_click=click_workspace, kwargs={'workspace': workspace})
        right.button('Arc', key=f'freeze_{workspace.id}', on_click=click_freeze, kwargs={'workspace': workspace})

    st.divider()

    # アーカイブされたワークスペースを表示
    with st.expander('アーカイブ'):
        for idx, workspace in enumerate(filter(lambda x: x.freezed_at is not None, st.session_state.workspaces)):
            cols = st.columns(COLUMNS)
            cols[0].write(idx + 1)
            cols[1].write(workspace.title)
            cols[2].write(workspace.created_at.strftime('%Y-%m-%d %H:%M:%S'))
            cols[3].button('Go', key=f'go_{workspace.id}', on_click=click_workspace, kwargs={'workspace': workspace})


def pane_assets():
    """アセット一覧を表示する"""
    st.button('戻る', key='back', on_click=lambda: st.session_state.pop('workspace'))
    st.header(st.session_state.workspace.title)

    if st.session_state.workspace.freezed_at is None:
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
    app_map = {app.id: app for app in st.session_state.applications}
    for idx, asset in enumerate(assets):
        cols = st.columns(COLUMNS)

        cols[0].write(idx + 1)
        cols[1].write(app_map[asset.application_id].name)
        cols[2].write(asset.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        if st.session_state.workspace.freezed_at is None:
            cols[3].button('Run', key=f'run_{asset.id}')

    st.divider()

    with st.expander('アカウント'):
        df = pd.DataFrame([it.dict() for it in st.session_state.accounts])
        df2 = pd.concat([df['email'], df['name'], df['role']], axis=1)
        df2.index = df2.index + 1
        cols = st.columns(1)
        cols[0].dataframe(df2, hide_index=False, use_container_width=True)


@st.dialog('Workspace 作成')
def create_workspace() -> None:
    """Workspace を作成するダイアログ"""
    title = st.text_input('名前')
    cols = st.columns(3)
    if cols[1].button('キャンセル', type='secondary', use_container_width=True):
        st.rerun()
    if cols[2].button('セットアップ', type='primary', use_container_width=True):
        workspace = Workspace(**{'id': uuid4(), 'title': title, 'created_at': datetime.now()})
        st.session_state.workspaces.append(workspace)
        st.rerun()


@st.dialog('新規アセット作成')
def create_asset() -> None:
    """アセットを作成するダイアログ"""
    workspace: Workspace = st.session_state.workspace
    title = st.text_input('名前')
    print(st.session_state.applications[0])
    app: Application = st.selectbox('業務 Excel', st.session_state.applications, format_func=lambda x: x.name)

    cols = st.columns(3)
    if cols[1].button('キャンセル', type='secondary', use_container_width=True):
        st.rerun()
    if cols[2].button('作成', type='primary', use_container_width=True):
        asset = Asset(
            **{
                'id': uuid4(),
                'workspace_id': workspace.id,
                'title': title,
                'application_id': app.id,
                'created_at': datetime.now(),
            }
        )
        st.session_state.assets.append(asset)
        st.rerun()


if st.session_state.workspace:
    pane_assets()
else:
    pane_workspaces()
