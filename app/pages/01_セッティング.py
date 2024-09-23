from uuid import uuid4

import pandas as pd
import streamlit as st
from lib import Application
from repository.account import create_account
from repository.account import fetch_accounts
from util.db import Database

Database.initialize('postgres://tokutomi@127.0.0.1:5432/gaibase_dev?sslmode=disable')


def initialize():
    if 'accounts' not in st.session_state:
        st.session_state.accounts = fetch_accounts()

    if 'applications' not in st.session_state:
        st.session_state.applications = []


def pane_account_list():
    with st.expander('アカウント'):
        cols = st.columns([6, 6, 2])
        email = cols[0].text_input('email')
        name = cols[1].text_input('name')
        if cols[2].button('追加', use_container_width=True):
            if len(email) > 0 and len(name) > 0:
                create_account(email, name)
                st.session_state.accounts = fetch_accounts()

        temp = [{'email': it.email, 'name': it.name, 'role_name': it.role_name} for it in st.session_state.accounts]
        df = pd.DataFrame(temp)
        df.index = df.index + 1
        cols = st.columns(1)
        cols[0].dataframe(df, hide_index=False, use_container_width=True)


def pane_excel_list():
    with st.expander('Excel シート'):
        cols = st.columns([3, 1])
        application = cols[0].text_input('Excel シート')
        if cols[1].button('追加', key='add_application', use_container_width=True):
            if len(application) > 0:
                st.session_state.applications.append(Application(**{'id': uuid4(), 'name': application}))

        cols = st.columns(1)
        df = pd.DataFrame([{'Excel 名': it.name} for it in st.session_state.applications])
        df.index = df.index + 1
        cols[0].dataframe(df, hide_index=False, use_container_width=True)


initialize()

st.title('システムセッティング')

pane_account_list()
pane_excel_list()
