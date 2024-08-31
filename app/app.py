# app.py
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

import streamlit as st


#
# 型定義
#
@dataclass
class Project:
  id: UUID
  title: str
  created_at: datetime

#
# セッションステートの初期化
#
if "projects" not in st.session_state:
  st.session_state.projects = [
    Project(uuid4(), "プロジェクト1", datetime.now()),
    Project(uuid4(), "プロジェクト2", datetime.now())
    ]

def pane_projects():
  """ プロジェクト一覧を表示する
  """
  header1, header2, header3 = st.columns(3)
  header1.write("**ID**")
  header2.write("**プロジェクト名**")
  header3.write("**作成日時**")

  for idx, project in enumerate(st.session_state.projects):
    col1, col2, col3 = st.columns(3)
    col1.write(idx+1)
    col2.write(project.title)
    col3.write(project.created_at.strftime("%Y-%m-%d %H:%M:%S"))


@st.dialog("新規プロジェクト作成")
def create_project() -> None:
  """ プロジェクトを作成するダイアログ
  """
  title = st.text_input("プロジェクト名")
  if st.button("作成"):
    project = Project(uuid4(), title, datetime.now())
    st.session_state.projects.append(project)
    st.rerun()
  if st.button("キャンセル"):
    st.rerun()


if st.button("プロジェクトを作成する"):
  create_project()
st.divider()
pane_projects()
