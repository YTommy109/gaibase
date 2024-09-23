# app.py
from datetime import datetime
from uuid import uuid4

import pandas as pd
import streamlit as st
from lib import Account
from lib import Application
from lib import Tool
from lib import Workspace
from repository.account import fetch_account_by_name
from repository.account import fetch_accounts
from repository.account import fetch_workspace_accounts_by_workspace
from repository.workspace import add_member_to_workspace
from repository.workspace import archive_workspace
from repository.workspace import fetch_owned_workspaces
from util.db import Database

Database.initialize('postgres://tokutomi@127.0.0.1:5432/gaibase_dev?sslmode=disable')

#
# 定数
#

APPLICATIONS: list[Application] = [
    Application(id=uuid4(), name='Excel シート 1'),
    Application(id=uuid4(), name='Excel シート 2'),
    Application(id=uuid4(), name='Excel シート 3'),
]


#
# セッションステートの初期化
#
def initialize(APPLICATIONS):
    if 'user' not in st.session_state:
        if 'user' in st.query_params:
            st.session_state.user = fetch_account_by_name(st.query_params['user'])

    if 'accounts' not in st.session_state:
        st.session_state.accounts = fetch_accounts()

    if 'workspaces' not in st.session_state:
        if 'user' in st.session_state:
            st.session_state.workspaces = fetch_owned_workspaces(st.session_state.user)
        else:
            st.session_state.workspaces = []

    if 'tools' not in st.session_state:
        st.session_state.tools = []

    if 'workspace' not in st.session_state:
        st.session_state.workspace = None

    if 'workspace_accounts' not in st.session_state:
        st.session_state.workspace_accounts = []

    if 'applications' not in st.session_state:
        st.session_state.applications = APPLICATIONS


def refresh_members():
    st.session_state.workspace_accounts = fetch_workspace_accounts_by_workspace(st.session_state.workspace)


initialize(APPLICATIONS)


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
        refresh_members()

    def click_freeze(workspace: Workspace):
        archive_workspace(workspace)
        st.session_state.workspaces = fetch_owned_workspaces(st.session_state.user)

    # アーカイブされていないワークスペースを表示
    for idx, workspace in enumerate(filter(lambda x: x.disabled_at is None, st.session_state.workspaces)):
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
        for idx, workspace in enumerate(filter(lambda x: x.disabled_at is not None, st.session_state.workspaces)):
            cols = st.columns(COLUMNS)
            cols[0].write(idx + 1)
            cols[1].write(workspace.title)
            cols[2].write(workspace.created_at.strftime('%Y-%m-%d %H:%M:%S'))
            cols[3].button('Go', key=f'go_{workspace.id}', on_click=click_workspace, kwargs={'workspace': workspace})


def pane_tool_list():
    """ツール一覧を表示する"""
    st.button('戻る', key='back', on_click=lambda: st.session_state.pop('workspace'))
    st.header(st.session_state.workspace.title)

    if st.session_state.workspace.disabled_at is None:
        if st.button('ツールを作成する'):
            create_asset()

    st.divider()

    COLUMNS = [1, 5, 3, 2]
    hds = st.columns(COLUMNS)
    hds[0].write('**No.**')
    hds[1].write('**Excel シート**')
    hds[2].write('**作成日時**')
    hds[3].write('')

    tools = filter(lambda x: x.workspace_id == st.session_state.workspace.id, st.session_state.tools)
    app_map = {app.id: app for app in st.session_state.applications}
    for idx, tool in enumerate(tools):
        cols = st.columns(COLUMNS)

        cols[0].write(idx + 1)
        cols[1].write(app_map[tool.application_id].name)
        cols[2].write(tool.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        if st.session_state.workspace.disabled_at is None:
            cols[3].button('Run', key=f'run_{tool.id}')

    st.divider()

    with st.expander('メンバー'):
        cols = st.columns([10, 2])
        if cols[1].button('Edit', use_container_width=True):
            manage_members()
        df = pd.DataFrame([{'name': it.name, 'role_name': it.role_name} for it in st.session_state.workspace_accounts])
        df.index = df.index + 1
        cols = st.columns(1)
        cols[0].dataframe(df, hide_index=False, use_container_width=True)


@st.dialog('メンバー管理')
def manage_members() -> None:
    """メンバー管理のダイアログ"""
    cols = st.columns([8, 4], vertical_alignment='bottom')
    temp: Account = cols[0].selectbox('メンバー', st.session_state.accounts, format_func=lambda x: x.name)
    if cols[1].button('追加', type='secondary', use_container_width=True):
        add_member_to_workspace(st.session_state.workspace, temp)
        refresh_members()

    st.divider()

    COLUMNS = [1, 5, 3, 2]
    hds = st.columns(COLUMNS)
    hds[0].write('**No.**')
    hds[1].write('**名前**')
    hds[2].write('**権限**')

    cols = st.columns(COLUMNS)
    for idx, account in enumerate(st.session_state.workspace_accounts):
        cols[0].text(idx + 1)
        cols[1].text(account.name)
        cols[2].text(account.role_name)

    cols = st.columns(3)
    if cols[1].button('キャンセル', type='secondary', use_container_width=True):
        st.rerun()
    if cols[2].button('保存', type='primary', use_container_width=True):
        st.rerun()


@st.dialog('Workspace 作成')
def create_workspace() -> None:
    """Workspace を作成するダイアログ"""
    title = st.text_input('名前')
    cols = st.columns(3)
    if cols[1].button('キャンセル', type='secondary', use_container_width=True):
        st.rerun()
    if cols[2].button('セットアップ', type='primary', use_container_width=True):
        workspace = Workspace(id=uuid4(), title=title, created_at=datetime.now())
        st.session_state.workspaces.append(workspace)
        st.rerun()


@st.dialog('新規ツール作成')
def create_asset() -> None:
    """ツールを作成するダイアログ"""
    workspace: Workspace = st.session_state.workspace
    title = st.text_input('名前')
    print(st.session_state.applications[0])
    app: Application = st.selectbox('Excel', st.session_state.applications, format_func=lambda x: x.name)

    cols = st.columns(3)
    if cols[1].button('キャンセル', type='secondary', use_container_width=True):
        st.rerun()
    if cols[2].button('作成', type='primary', use_container_width=True):
        st.session_state.tools.append(
            Tool(
                id=uuid4(),
                workspace_id=workspace.id,
                title=title,
                application_id=app.id,
                created_at=datetime.now(),
            )
        )
        st.rerun()


if 'user' not in st.session_state:
    st.write('ログインしていません')
else:
    st.write(st.session_state.user.email)
    if st.session_state.workspace:
        pane_tool_list()
    else:
        pane_workspaces()
