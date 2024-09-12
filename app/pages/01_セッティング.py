from uuid import uuid4

import pandas as pd
import streamlit as st
from lib import Account, Application, Role

ROLE_MAP = {Role.ADMIN: '運用', Role.USER: '一般'}

if 'accounts' not in st.session_state:
    st.session_state.accounts = [
        Account(**{'id': uuid4(), 'email': 'gy@pwc.com', 'name': 'Yoshi', 'role': Role.ADMIN}),
        Account(**{'id': uuid4(), 'email': 'yt@pwc.com', 'name': 'Toku', 'role': Role.ADMIN}),
    ]

if 'applications' not in st.session_state:
    st.session_state.applications = []

st.title('セッティング')

with st.expander('アカウント'):
    cols = st.columns([6, 6, 2])
    email = cols[0].text_input('email')
    name = cols[1].text_input('name')
    if cols[2].button('追加', use_container_width=True):
        if len(email) > 0 and len(name) > 0:
            st.session_state.accounts.append(
                Account(**{'id': uuid4(), 'email': email, 'name': name, 'role': Role.USER})
            )

    temp = [it.dict() for it in st.session_state.accounts]
    # temp2 = [it.update({'role': ROLE_MAP[it['role']]}) for it in temp]
    df = pd.DataFrame([it.dict() for it in st.session_state.accounts])
    df2 = pd.concat([df['email'], df['name'], df['role']], axis=1)
    df2.index = df2.index + 1
    cols = st.columns(1)
    cols[0].dataframe(df2, hide_index=False, use_container_width=True)

with st.expander('業務 Excel シート'):
    cols = st.columns([3, 1])
    application = cols[0].text_input('業務 Excel シート')
    if cols[1].button('追加', key='add_application', use_container_width=True):
        if len(application) > 0:
            st.session_state.applications.append(Application(**{'id': uuid4(), 'name': application}))

    cols = st.columns(1)
    df = pd.DataFrame([it.dict() for it in st.session_state.applications])
    df = df.rename(columns={'id': 'ID', 'name': '業務 Excel シート'})
    cols[0].dataframe(df, hide_index=True, use_container_width=True)
