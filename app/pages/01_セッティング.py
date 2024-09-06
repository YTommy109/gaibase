from dataclasses import asdict
from uuid import uuid4

import pandas as pd
import streamlit as st
from lib import Application

if 'accounts' not in st.session_state:
    st.session_state.accounts = []

if 'applications' not in st.session_state:
    st.session_state.applications = []

st.title('セッティング')

with st.expander('アカウント'):
    cols = st.columns([3, 1])
    account = cols[0].text_input('アカウント')
    if cols[1].button('追加', use_container_width=True):
        if len(account) > 0:
            st.session_state.accounts.append(account)

    cols = st.columns(1)
    cols[0].dataframe(
        pd.DataFrame({'アカウント': st.session_state.accounts}), hide_index=True, use_container_width=True
    )

with st.expander('業務 Excel シート'):
    cols = st.columns([3, 1])
    application = cols[0].text_input('業務 Excel シート')
    if cols[1].button('追加', key='add_application', use_container_width=True):
        if len(application) > 0:
            st.session_state.applications.append(Application(uuid4(), application))

    cols = st.columns(1)
    df = pd.DataFrame([asdict(it) for it in st.session_state.applications])
    df = df.rename(columns={'id': 'ID', 'name': '業務 Excel シート'})
    cols[0].dataframe(df, hide_index=True, use_container_width=True)

st.markdown("""
- [ ] アーカイブワークスペース
""")
